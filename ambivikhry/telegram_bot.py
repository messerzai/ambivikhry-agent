from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Iterable

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from ambivikhry.agent import AmbivikhryAgent, AgentConfig
from ambivikhry.llm import OpenAICompatibleLLM


MAX_TELEGRAM_MESSAGE = 4096


def _csv_ints(value: str | None) -> set[int]:
    if not value:
        return set()
    result: set[int] = set()
    for item in value.split(","):
        item = item.strip()
        if item:
            result.add(int(item))
    return result


class TelegramAmbivikhry:
    """Telegram operator interface for a bounded Ambivikhry runtime.

    Security defaults are fail-closed:
    - TELEGRAM_ALLOWED_USER_IDS is mandatory.
    - Each Telegram user gets an isolated memory directory.
    - The existing Agent/PolicyGate/DryRun boundaries remain in force.
    - The bot itself never grants permissions or executes Telegram commands
      as tools.
    """

    def __init__(self) -> None:
        self.allowed_users = _csv_ints(os.getenv("TELEGRAM_ALLOWED_USER_IDS"))
        self.workdir = Path(os.getenv("AMBIVIKHRY_WORKDIR", "./runtime/telegram"))
        self.workdir.mkdir(parents=True, exist_ok=True)
        self.max_iterations = int(os.getenv("AMBIVIKHRY_MAX_ITERATIONS", "4"))
        self._agents: dict[int, AmbivikhryAgent] = {}
        self._locks: dict[int, asyncio.Lock] = {}

        if not self.allowed_users:
            raise RuntimeError(
                "TELEGRAM_ALLOWED_USER_IDS must contain at least one Telegram user ID"
            )

    def authorized(self, update: Update) -> bool:
        user = update.effective_user
        return bool(user and user.id in self.allowed_users)

    def agent_for(self, user_id: int) -> AmbivikhryAgent:
        if user_id not in self._agents:
            provider = OpenAICompatibleLLM()
            user_dir = self.workdir / str(user_id)
            self._agents[user_id] = AmbivikhryAgent(
                provider=provider,
                workdir=str(user_dir),
                config=AgentConfig(max_iterations=self.max_iterations),
            )
            self._locks[user_id] = asyncio.Lock()
        return self._agents[user_id]

    async def reject(self, update: Update) -> None:
        if update.effective_message:
            await update.effective_message.reply_text(
                "Доступ закрыт. Этот Telegram ID не находится в allowlist оператора."
            )

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.authorized(update):
            return await self.reject(update)
        await update.effective_message.reply_text(
            "Амбивихрь — операторский Telegram-интерфейс.\n\n"
            "Просто отправьте задачу обычным сообщением.\n"
            "/status — состояние экземпляра\n"
            "/audit — последние события аудита\n"
            "/reset — новый экземпляр с чистым состоянием\n"
            "/help — эта справка"
        )

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.authorized(update):
            return await self.reject(update)
        user_id = update.effective_user.id
        agent = self.agent_for(user_id)
        state = agent.memory.load()
        await update.effective_message.reply_text(
            "Амбивихрь: ONLINE\n"
            f"instance: {agent.instance_id}\n"
            f"max_iterations: {agent.config.max_iterations}\n"
            f"last_confidence: {state.get('confidence', '—')}\n"
            f"last_verification: {state.get('verification_score', '—')}\n"
            "policy: bounded / approval boundary preserved"
        )

    async def audit(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.authorized(update):
            return await self.reject(update)
        user_id = update.effective_user.id
        agent = self.agent_for(user_id)
        events = agent.audit[-8:]
        if not events:
            await update.effective_message.reply_text("Аудит пока пуст.")
            return
        lines = []
        for event in events:
            kind = event.get("event", "event")
            extra = ""
            if kind in {"tool_blocked", "tool_rejected"}:
                extra = f" | {event.get('reason', '')}"
            lines.append(f"• {kind}{extra}")
        await update.effective_message.reply_text("Последние события:\n" + "\n".join(lines))

    async def reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.authorized(update):
            return await self.reject(update)
        user_id = update.effective_user.id
        self._agents.pop(user_id, None)
        self._locks.pop(user_id, None)
        await update.effective_message.reply_text(
            "Экземпляр сброшен. Следующее сообщение создаст новый bounded runtime."
        )

    async def message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.authorized(update):
            return await self.reject(update)

        message = update.effective_message
        user = update.effective_user
        if not message or not user or not message.text:
            return

        agent = self.agent_for(user.id)
        lock = self._locks[user.id]

        async with lock:
            await message.chat.send_action(ChatAction.TYPING)
            try:
                result = await asyncio.to_thread(agent.run, message.text)
            except Exception as exc:
                # Do not expose secrets, provider headers, or stack traces to Telegram.
                await message.reply_text(f"Ошибка выполнения агента: {type(exc).__name__}")
                return

        prefix = (
            f"Амбивихрь · {result.instance_id}\n"
            f"confidence={result.confidence:.2f} · verification={result.verification_score:.2f}\n\n"
        )
        text = prefix + (result.answer or "Агент не сформировал ответ.")
        await self._reply_chunks(message, text)

        # Privilege expansion attempts are surfaced separately to the operator.
        privilege_events = [
            event for event in result.audit
            if "privilege" in str(event).lower()
            or "permission" in str(event).lower()
        ]
        if privilege_events:
            await message.reply_text(
                "⚠️ ОТДЕЛЬНОЕ УВЕДОМЛЕНИЕ: в аудите обнаружено событие, "
                "связанное с запросом/изменением полномочий. Автоматически не одобрено."
            )

    async def _reply_chunks(self, message, text: str) -> None:
        for chunk in _chunks(text, MAX_TELEGRAM_MESSAGE):
            await message.reply_text(chunk)


def _chunks(text: str, size: int) -> Iterable[str]:
    while text:
        yield text[:size]
        text = text[size:]


def build_application() -> Application:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is required")

    interface = TelegramAmbivikhry()
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", interface.help))
    app.add_handler(CommandHandler("help", interface.help))
    app.add_handler(CommandHandler("status", interface.status))
    app.add_handler(CommandHandler("audit", interface.audit))
    app.add_handler(CommandHandler("reset", interface.reset))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, interface.message)
    )
    return app


def main() -> None:
    build_application().run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

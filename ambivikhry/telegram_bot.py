from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Iterable

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CallbackQueryHandler,
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
    return {int(item.strip()) for item in value.split(",") if item.strip()}


def _chunks(text: str, size: int) -> Iterable[str]:
    while text:
        yield text[:size]
        text = text[size:]


class TelegramAmbivikhry:
    """Operator UI for the bounded Ambivikhry runtime.

    Telegram is only an interface. It does not widen the runtime's
    permissions and cannot approve its own privilege requests.
    """

    def __init__(self) -> None:
        self.allowed_users = _csv_ints(os.getenv("TELEGRAM_ALLOWED_USER_IDS"))
        self.workdir = Path(os.getenv("AMBIVIKHRY_WORKDIR", "./runtime/telegram"))
        self.workdir.mkdir(parents=True, exist_ok=True)
        self.max_iterations = int(os.getenv("AMBIVIKHRY_MAX_ITERATIONS", "4"))
        self._agents: dict[int, AmbivikhryAgent] = {}
        self._locks: dict[int, asyncio.Lock] = {}

        if not self.allowed_users:
            raise RuntimeError("TELEGRAM_ALLOWED_USER_IDS must contain at least one Telegram user ID")

    def authorized(self, update: Update) -> bool:
        user = update.effective_user
        return bool(user and user.id in self.allowed_users)

    def agent_for(self, user_id: int) -> AmbivikhryAgent:
        if user_id not in self._agents:
            self._agents[user_id] = AmbivikhryAgent(
                provider=OpenAICompatibleLLM(),
                workdir=str(self.workdir / str(user_id)),
                config=AgentConfig(max_iterations=self.max_iterations),
            )
            self._locks[user_id] = asyncio.Lock()
        return self._agents[user_id]

    def keyboard(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🧠 Состояние", callback_data="status"),
                InlineKeyboardButton("📜 Аудит", callback_data="audit"),
            ],
            [
                InlineKeyboardButton("🔬 Исследование", callback_data="research"),
                InlineKeyboardButton("⚙️ Самоулучшение", callback_data="improve"),
            ],
            [
                InlineKeyboardButton("🛑 Стоп", callback_data="stop"),
                InlineKeyboardButton("🔄 Сброс", callback_data="reset"),
            ],
        ])

    async def reject(self, update: Update) -> None:
        if update.effective_message:
            await update.effective_message.reply_text(
                "Доступ закрыт: Telegram ID отсутствует в allowlist оператора."
            )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.authorized(update):
            return await self.reject(update)
        await update.effective_message.reply_text(
            "🌀 *Амбивихрь / Operator Channel*\n\n"
            "Я принимаю задачи текстом и показываю служебное состояние через кнопки.\n"
            "Все действия остаются bounded; расширение полномочий не одобряется автоматически.",
            reply_markup=self.keyboard(),
            parse_mode="Markdown",
        )

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.authorized(update):
            return await self.reject(update)
        await update.effective_message.reply_text(
            "/start — главное меню\n"
            "/status — состояние\n"
            "/audit — аудит\n"
            "/reset — новый экземпляр\n"
            "Текст — задача агенту.",
            reply_markup=self.keyboard(),
        )

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.authorized(update):
            return await self.reject(update)
        user_id = update.effective_user.id
        agent = self.agent_for(user_id)
        state = agent.memory.load()
        await update.effective_message.reply_text(self._status_text(agent, state), reply_markup=self.keyboard())

    def _status_text(self, agent: AmbivikhryAgent, state: dict) -> str:
        return (
            "🧠 АМБИВИХРЬ\n\n"
            "● Runtime: ONLINE\n"
            f"● Instance: {agent.instance_id}\n"
            f"● Iterations: {agent.config.max_iterations}\n"
            f"● Confidence: {state.get('confidence', '—')}\n"
            f"● Verification: {state.get('verification_score', '—')}\n"
            "● Policy: BOUNDED\n"
            "● Self-approval of privileges: OFF"
        )

    async def audit(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.authorized(update):
            return await self.reject(update)
        agent = self.agent_for(update.effective_user.id)
        events = agent.audit[-10:]
        if not events:
            text = "📜 Аудит пока пуст."
        else:
            lines = []
            for event in events:
                kind = event.get("event", "event")
                suffix = ""
                if kind in {"tool_blocked", "tool_rejected"}:
                    suffix = f" — {event.get('reason', '')}"
                lines.append(f"• {kind}{suffix}")
            text = "📜 ПОСЛЕДНИЕ СОБЫТИЯ\n\n" + "\n".join(lines)
        await update.effective_message.reply_text(text, reply_markup=self.keyboard())

    async def reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.authorized(update):
            return await self.reject(update)
        user_id = update.effective_user.id
        self._agents.pop(user_id, None)
        self._locks.pop(user_id, None)
        await update.effective_message.reply_text(
            "🔄 Экземпляр сброшен. Следующее сообщение создаст новый runtime.",
            reply_markup=self.keyboard(),
        )

    async def callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        if not query:
            return
        if not self.authorized(update):
            await query.answer("Доступ закрыт.", show_alert=True)
            return
        await query.answer()
        user_id = update.effective_user.id

        if query.data == "status":
            agent = self.agent_for(user_id)
            await query.edit_message_text(
                self._status_text(agent, agent.memory.load()),
                reply_markup=self.keyboard(),
            )
        elif query.data == "audit":
            agent = self.agent_for(user_id)
            events = agent.audit[-10:]
            text = "📜 Аудит пока пуст." if not events else "📜 " + "\n".join(
                f"• {e.get('event', 'event')}" for e in events
            )
            await query.edit_message_text(text, reply_markup=self.keyboard())
        elif query.data == "reset":
            self._agents.pop(user_id, None)
            self._locks.pop(user_id, None)
            await query.edit_message_text(
                "🔄 Runtime сброшен.",
                reply_markup=self.keyboard(),
            )
        elif query.data == "stop":
            # Current Agent.run is bounded/synchronous; this button is an
            # operator-state marker rather than a fake claim of cancellation.
            context.user_data["stop_requested"] = True
            await query.edit_message_text(
                "🛑 STOP REQUESTED\n\n"
                "Новые задачи не получают дополнительного разрешения. "
                "Текущий bounded cycle не объявляется остановленным задним числом.",
                reply_markup=self.keyboard(),
            )
        elif query.data == "research":
            await query.edit_message_text(
                "🔬 РЕЖИМ ИССЛЕДОВАНИЯ\n\n"
                "Отправь следующим сообщением тему или вопрос. "
                "Она будет передана текущему агенту как обычная bounded-задача.",
                reply_markup=self.keyboard(),
            )
        elif query.data == "improve":
            await query.edit_message_text(
                "⚙️ РЕЖИМ САМОУЛУЧШЕНИЯ\n\n"
                "Отправь задачу на улучшение. Агент может предложить изменения, "
                "но интерфейс не даёт ему права самостоятельно одобрить изменение полномочий.",
                reply_markup=self.keyboard(),
            )

    async def message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.authorized(update):
            return await self.reject(update)
        message = update.effective_message
        user = update.effective_user
        if not message or not user or not message.text:
            return

        if context.user_data.pop("stop_requested", False):
            await message.reply_text(
                "🛑 Операторский STOP-флаг активен. Отправь /start после проверки состояния, "
                "чтобы продолжить работу."
            )
            return

        agent = self.agent_for(user.id)
        async with self._locks[user.id]:
            await message.chat.send_action(ChatAction.TYPING)
            try:
                result = await asyncio.to_thread(agent.run, message.text)
            except Exception as exc:
                await message.reply_text(f"Ошибка выполнения агента: {type(exc).__name__}")
                return

        header = (
            f"🌀 Амбивихрь · {result.instance_id}\n"
            f"confidence={result.confidence:.2f} · verification={result.verification_score:.2f}\n\n"
        )
        await self._reply_chunks(message, header + (result.answer or "Ответ не сформирован."))

        privilege_events = [
            event for event in result.audit
            if "privilege" in str(event).lower() or "permission" in str(event).lower()
        ]
        if privilege_events:
            await message.reply_text(
                "⚠️ ОТДЕЛЬНОЕ УВЕДОМЛЕНИЕ\n"
                "Обнаружено событие, связанное с запросом/изменением полномочий. "
                "Автоматически не одобрено."
            )

    async def _reply_chunks(self, message, text: str) -> None:
        for chunk in _chunks(text, MAX_TELEGRAM_MESSAGE):
            await message.reply_text(chunk)

def build_application() -> Application:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is required")
    interface = TelegramAmbivikhry()
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", interface.start))
    app.add_handler(CommandHandler("help", interface.help))
    app.add_handler(CommandHandler("status", interface.status))
    app.add_handler(CommandHandler("audit", interface.audit))
    app.add_handler(CommandHandler("reset", interface.reset))
    app.add_handler(CallbackQueryHandler(interface.callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, interface.message))
    return app

def main() -> None:
    build_application().run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

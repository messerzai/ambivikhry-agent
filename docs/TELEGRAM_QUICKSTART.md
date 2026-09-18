# Запуск Амбивихря в Telegram

## Важно

Telegram-интерфейс уже реализован в экспериментальной ветке `experiment/telegram-interface`.

Сам агент **не может сам создать себе Telegram-бота**: Telegram требует токен BotFather, а токен является секретом оператора. Поэтому запуск состоит из одного действия человека — создать бота и передать секреты окружению. После этого процесс можно настроить на автоматический перезапуск.

## 1. Создать Telegram-бота

В Telegram откройте официального `@BotFather` и выполните:

1. `/newbot`
2. задайте имя;
3. задайте username, заканчивающийся на `bot`;
4. сохраните выданный токен.

Токен **не добавляйте в GitHub, исходники или сообщения**.

## 2. Узнать свой Telegram user ID

Используйте любого доверенного бота, который показывает numeric Telegram ID, либо получите ID через первый тестовый запуск и журнал обновлений. В переменную `TELEGRAM_ALLOWED_USER_IDS` записывается именно числовой ID пользователя, например:

```text
TELEGRAM_ALLOWED_USER_IDS=123456789
```

Allowlist обязателен: без него бот намеренно не запускается.

## 3. Подготовить Python

Требуется Python 3.10+.

```bash
git clone https://github.com/messerzai/ambivikhry-agent.git
cd ambivikhry-agent
git checkout experiment/telegram-interface
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Для Windows PowerShell:

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

## 4. Задать секреты

Linux/macOS:

```bash
export TELEGRAM_BOT_TOKEN="ТОКЕН_ОТ_BOTFATHER"
export TELEGRAM_ALLOWED_USER_IDS="ВАШ_NUMERIC_TELEGRAM_ID"

export AMBIVIKHRY_API_KEY="КЛЮЧ_LLM"
export AMBIVIKHRY_MODEL="ИМЯ_МОДЕЛИ"
# Необязательно:
# export AMBIVIKHRY_BASE_URL="https://api.openai.com/v1"
# export AMBIVIKHRY_MAX_ITERATIONS="4"
# export AMBIVIKHRY_WORKDIR="./runtime/telegram"
```

Windows PowerShell:

```powershell
$env:TELEGRAM_BOT_TOKEN="ТОКЕН_ОТ_BOTFATHER"
$env:TELEGRAM_ALLOWED_USER_IDS="ВАШ_NUMERIC_TELEGRAM_ID"
$env:AMBIVIKHRY_API_KEY="КЛЮЧ_LLM"
$env:AMBIVIKHRY_MODEL="ИМЯ_МОДЕЛИ"
```

## 5. Запустить

```bash
ambivikhry-telegram
```

После запуска откройте своего бота и отправьте:

```text
/start
```

Появится операторское меню.

## 6. Быстрый тест

Отправьте:

```text
Проведи короткий тест своей текущей архитектуры и перечисли неизвестные.
```

Затем проверьте:

- **🧠 Состояние** — runtime и метрики;
- **📜 Аудит** — события;
- **🔬 Исследование** — bounded research-задачи;
- **⚙️ Самоулучшение** — bounded задачи на улучшение;
- **🛑 Стоп** — операторский stop-флаг;
- **🔄 Сброс** — новый runtime-экземпляр.

## Автозапуск

После ручной проверки процесс можно сделать сервисом. Например, на Linux с systemd:

```ini
[Unit]
Description=Ambivikhry Telegram Operator Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/opt/ambivikhry-agent
EnvironmentFile=/etc/ambivikhry/telegram.env
ExecStart=/opt/ambivikhry-agent/.venv/bin/ambivikhry-telegram
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Сохраните unit как `/etc/systemd/system/ambivikhry-telegram.service`, затем:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now ambivikhry-telegram
sudo systemctl status ambivikhry-telegram
```

Секреты храните только в `/etc/ambivikhry/telegram.env` с правами доступа для нужного пользователя.

## Что агент не делает сам

- не получает Telegram token самостоятельно;
- не добавляет пользователей в allowlist;
- не расширяет свои права через Telegram;
- не получает права на merge/deploy автоматически;
- не считает сообщение из Telegram разрешением на опасное действие.

Это сделано намеренно: запуск можно автоматизировать, но **выдача полномочий остаётся у оператора**.

## 24/7

Для постоянной работы нужен постоянно работающий хост: VPS, домашний сервер, cloud VM или другой сервис, где можно держать Python-процесс. После первоначальной настройки systemd автоматически перезапустит процесс после сбоя и поднимет его после перезагрузки.

GitHub Actions не следует использовать как постоянный Telegram polling-сервис: workflow не предназначен для бесконечного процесса.

## Текущие ограничения

Кнопка STOP в текущей версии не прерывает уже выполняющийся синхронный `Agent.run` посреди итерации. Она не лжёт о состоянии: отмена становится кооперативной на границах следующего задания. Полноценный Task Manager с task IDs, очередью и cooperative cancellation — следующий этап.

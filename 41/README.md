# Telegram Bot с локальной ИИ-моделью

Telegram-бот на `aiogram`, который использует OpenAI-совместимый API для подключения к локальной модели (например, Ollama). Бот сохраняет историю диалога в SQLite и поддерживает команду для очистки истории.

## Возможности

- Работа с OpenAI-совместимым API локальных моделей (Ollama, LM Studio и др.)
- Сохранение истории диалога в SQLite (таблица `history`: `user_id`, `role`, `content`)
- Загрузка последних 10 сообщений перед каждым запросом к ИИ
- Команда `/clear` для очистки истории диалога

## Требования

- Python 3.8+
- Локальная модель с OpenAI-совместимым API (например, [Ollama](https://ollama.ai/))
- Токен Telegram-бота от [@BotFather](https://t.me/BotFather)

## Установка

1. Клонируйте репозиторий или скопируйте файлы проекта.

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Конфигурация

Настройте переменные окружения или измените их в файле `bot.py`:

| Переменная | Описание | Значение по умолчанию |
|------------|----------|----------------------|
| `BOT_TOKEN` | Токен Telegram-бота | `YOUR_BOT_TOKEN_HERE` |
| `OPENAI_API_BASE` | URL OpenAI-совместимого API | `http://localhost:11434/v1` |
| `OPENAI_API_KEY` | Ключ API | `ollama` |
| `MODEL_NAME` | Название модели | `llama3` |

### Установка переменных окружения в Windows (PowerShell):

```powershell
$env:BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
$env:OPENAI_API_BASE="http://localhost:11434/v1"
$env:OPENAI_API_KEY="ollama"
$env:MODEL_NAME="llama3"
```

### Установка переменных окружения в Windows (cmd):

```cmd
set BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
set OPENAI_API_BASE=http://localhost:11434/v1
set OPENAI_API_KEY=ollama
set MODEL_NAME=llama3
```

## Запуск бота

```bash
python bot.py
```

## Команды бота

| Команда | Описание |
|---------|----------|
| `/start` | Приветственное сообщение |
| `/clear` | Очистка истории диалога |
| *текстовое сообщение* | Отправка сообщения ИИ и получение ответа |

## Структура проекта

- `bot.py` — основной код бота на `aiogram` с интеграцией OpenAI API
- `memory_db.py` — класс `MemoryDB` для работы с SQLite базой истории диалогов
- `history.db` — база данных SQLite (создается автоматически)
- `requirements.txt` — зависимости проекта

## Локальные модели

### Ollama

Если вы используете Ollama, убедитесь, что:
1. Ollama запущен и слушает на `http://localhost:11434`
2. Модель загружена (например, `ollama pull llama3`)
3. API Ollama доступен по адресу `http://localhost:11434/v1`

Для проверки API можно отправить запрос:
```bash
curl -X POST http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### llama.cpp (llama-server)

Если вы используете llama.cpp с сервером `llama-server`, убедитесь, что:
1. `llama-server` запущен и слушает на `http://localhost:8080` (или другом порту)
2. Модель загружена (например, `Qwen-AgentWorld-35B-A3B-UD-IQ3_S.gguf`)
3. API llama-server доступен по адресу `http://localhost:8080/v1`

Настройки для llama.cpp:
- `OPENAI_API_BASE=http://localhost:8080/v1`
- `OPENAI_API_KEY=none`
- `MODEL_NAME=Qwen-AgentWorld-35B-A3B-UD-IQ3_S.gguf`

Для запуска `llama-server` с моделью:
```bash
llama-server --model path/to/Qwen-AgentWorld-35B-A3B-UD-IQ3_S.gguf --port 8080 --host 127.0.0.1
```

# run_bot.py
import os
import sys
import logging

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

def get_bot_token():
    """Запрашивает токен бота у пользователя, если он не задан в переменных окружения."""
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("Введите токен Telegram-бота:")
        token = input().strip()
    
    if not token:
        print("Ошибка: Токен бота не введён!")
        sys.exit(1)
    
    return token

def run_telegram_bot():
    # Запрашиваем параметры
    bot_token = get_bot_token()
    os.environ["BOT_TOKEN"] = bot_token
    
    # Инициализируем базу данных
    import db
    db.init_db()
    
    # Запускаем бота
    import bot
    bot.main()

if __name__ == "__main__":
    run_telegram_bot()

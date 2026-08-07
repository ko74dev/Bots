import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import OpenAI

from memory_db import MemoryDB

# Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "http://127.0.0.1:8080/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "none")  # Default for local models like Ollama
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen-AgentWorld-35B-A3B-UD-IQ3_S.gguf")

# Initialize database
db = MemoryDB("history.db")


async def get_ai_response(user_id: int, user_message: str) -> str:
    """Get response from OpenAI-compatible API and update history."""
    # Add user message to database
    db.add_message(user_id, "user", user_message)
    
    # Get last 10 messages from database
    messages = db.get_last_messages(user_id, limit=10)
    
    # Convert to OpenAI format
    messages_list = [{"role": msg["role"], "content": msg["content"]} for msg in messages]
    
    # Initialize OpenAI client
    client = OpenAI(
        base_url=OPENAI_API_BASE,
        api_key=OPENAI_API_KEY,
    )
    
    # Get response from AI
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages_list
    )
    
    ai_response = response.choices[0].message.content
    
    # Add AI response to database
    db.add_message(user_id, "assistant", ai_response)
    
    return ai_response


# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот с локальной ИИ-моделью. Напишите мне сообщение, и я отвечу.")


@dp.message(Command("clear"))
async def cmd_clear(message: types.Message):
    db.clear_history(message.from_user.id)
    await message.answer("История диалога очищена.")


@dp.message()
async def handle_message(message: types.Message):
    if message.text.startswith("/"):
        return
        
    try:
        # Get AI response
        response = await get_ai_response(message.from_user.id, message.text)
        
        # Send response to user
        await message.answer(response)
    except Exception as e:
        await message.answer(f"Ошибка при обработке запроса: {str(e)}")


async def main():
    # Start the bot
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

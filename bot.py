import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import openai

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Получаем токены из переменных окружения
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

openai.api_key = OPENAI_API_KEY

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply("👋 Привет! Я DocFlyura Assistant Bot. Задай мне вопрос по косметологии, пептидам или anti-age!")

@dp.message_handler()
async def handle_message(message: types.Message):
    user_text = message.text
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Ты DocFlyura Assistant – эксперт в косметологии, пептидологии и превентивной медицине."},
                      {"role": "user", "content": user_text}]
        )
        answer = response.choices[0].message["content"]
        await message.reply(answer)
    except Exception as e:
        await message.reply("⚠️ Ошибка запроса к OpenAI API.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

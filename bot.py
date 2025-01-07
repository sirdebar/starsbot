from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config import BOT_TOKEN
from handlers import setup_handlers

async def set_commands(bot: Bot):
    """
    Устанавливает команды бота.
    """
    commands = [
        BotCommand(command="/start", description="Запуск бота"),
        BotCommand(command="/help", description="Помощь"),
    ]
    await bot.set_my_commands(commands)

async def main():
    try:
        # Инициализация бота с указанием HTML как формат разметки
        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher()
        
        # Настройка обработчиков
        setup_handlers(dp)
        
        # Установка команд
        await set_commands(bot)
        
        # Запуск опроса
        await dp.start_polling(bot, allowed_updates=["message", "callback_query"])
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

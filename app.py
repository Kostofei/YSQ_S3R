import asyncio
import os

from aiogram import Bot, Dispatcher, types

from dotenv import find_dotenv, load_dotenv

from common.bot_cmds_list import private
from handlers.user_private import user_private_router, complete_survey

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'))
complete_survey.bot = bot

dp = Dispatcher()

dp.include_router(user_private_router)


async def main():
    print('Бот запущен')
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeDefault())
    await dp.start_polling(bot)


asyncio.run(main())

from aiogram.types import BotCommand

private = [
    BotCommand(command='start', description='Старт выполнения теста'),
    BotCommand(command='info', description='Информация о боте'),
    BotCommand(command='stop', description='Остановить тест (все данные будут потеряны)'),
]

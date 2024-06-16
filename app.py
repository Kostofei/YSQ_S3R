import asyncio
import logging
import os
import time

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, BotCommand, FSInputFile

from data_file.answers_list import answers
from data_file.questions_list import questions
from data_file.schemes_list import schemes

from tabulate import tabulate

bot = Bot(token='7343816434:AAE8FgLLOAyGTq_RMssHgl30x9bbbjYhsEw')

dp = Dispatcher()

private = [
    BotCommand(command='start', description='Старт выполнения теста'),
    BotCommand(command='info', description='Информация о боте'),
]


class QuestionList(StatesGroup):
    # Шаги состояний
    question01 = State()
    question02 = State()
    question03 = State()
    question04 = State()
    question05 = State()
    question06 = State()
    question07 = State()
    question08 = State()
    question09 = State()
    question10 = State()
    question11 = State()
    question12 = State()
    question13 = State()
    question14 = State()
    question15 = State()
    question16 = State()
    question17 = State()
    question18 = State()
    question19 = State()
    question20 = State()
    question21 = State()
    question22 = State()
    question23 = State()
    question24 = State()
    question25 = State()
    question26 = State()
    question27 = State()
    question28 = State()
    question29 = State()
    question30 = State()
    question31 = State()
    question32 = State()
    question33 = State()
    question34 = State()
    question35 = State()
    question36 = State()
    question37 = State()
    question38 = State()
    question39 = State()
    question40 = State()
    question41 = State()
    question42 = State()
    question43 = State()
    question44 = State()
    question45 = State()
    question46 = State()
    question47 = State()
    question48 = State()
    question49 = State()
    question50 = State()
    question51 = State()
    question52 = State()
    question53 = State()
    question54 = State()
    question55 = State()
    question56 = State()
    question57 = State()
    question58 = State()
    question59 = State()
    question60 = State()
    question61 = State()
    question62 = State()
    question63 = State()
    question64 = State()
    question65 = State()
    question66 = State()
    question67 = State()
    question68 = State()
    question69 = State()
    question70 = State()
    question71 = State()
    question72 = State()
    question73 = State()
    question74 = State()
    question75 = State()
    question76 = State()
    question77 = State()
    question78 = State()
    question79 = State()
    question80 = State()
    question81 = State()
    question82 = State()
    question83 = State()
    question84 = State()
    question85 = State()
    question86 = State()
    question87 = State()
    question88 = State()
    question89 = State()
    question90 = State()


@dp.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    print('Я сработал', time.strftime("%H:%M", time.localtime()), message.from_user.first_name)
    for s in schemes:
        s[3] = 0
    await message.answer(f"1. {questions[1]}",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[
                                 [KeyboardButton(text=answers[str(i)]) for i in range(1, 3)],
                                 [KeyboardButton(text=answers[str(i)]) for i in range(3, 5)],
                                 [KeyboardButton(text=answers[str(i)]) for i in range(5, 7)],
                             ],
                             resize_keyboard=False,
                         ),
                         )
    await state.set_state(QuestionList.question01)


@dp.message(F.text.lower() == "информация")
@dp.message(Command("info"))
async def start_cmd(message: types.Message):
    await message.answer(
        'Данный бот предназначен для (текст описания бота). Отвечайте на вопросы исключительно с помощью кнопок выбора.',
        reply_markup=ReplyKeyboardRemove())


@dp.message(lambda message: message.text in [i for i in answers.values()])
async def handle_question(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        current_question_number = int(current_state.split(':')[1][-2:])
        await state.update_data({f'question{current_question_number:02}': message.text})
        next_question_number = current_question_number + 1
        if next_question_number <= 90:
            await message.answer(f"{next_question_number}. {questions[next_question_number]}")
            await state.set_state(getattr(QuestionList, f'question{next_question_number:02}'))
        else:
            await complete_survey(message, state)
    else:
        await message.answer("Тест не запущен, для запуска введите /start",
                             reply_markup=ReplyKeyboardRemove())


@dp.message(lambda message: message.text)
async def error_message_text(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await message.answer('Вводите ответы с помощью клавиатуры')
    else:
        await message.answer("Для получения информации введите /info\nДля старта теста введите /start",
                             reply_markup=ReplyKeyboardRemove())


# @dp.message(QuestionList.question01, F.text)
# async def start_cmd(message: types.Message, state: FSMContext):
#     await state.update_data(question01=message.text)
#     key = 2
#     value = questions[key]
#     await message.answer(f"{key}. {value}")
#     await state.set_state(QuestionList.question02)
#
#
# @dp.message(QuestionList.question02, F.text)
# async def start_cmd(message: types.Message, state: FSMContext):
#     await state.update_data(question02=message.text)
#     key = 3
#     value = questions[key]
#     await message.answer(f"{key}. {value}")
#     await state.set_state(QuestionList.question03)
#
#
# @dp.message(QuestionList.question03, F.text)
# async def start_cmd(message: types.Message, state: FSMContext):
#     await state.update_data(question03=message.text)
#     key = 4
#     value = questions[key]
#     await message.answer(f"{key}. {value}")
#     await state.set_state(QuestionList.question04)
#
#
# @dp.message(QuestionList.question04, F.text)
# async def start_cmd(message: types.Message, state: FSMContext):
#     await state.update_data(question04=message.text)
#     key = 5
#     value = questions[key]
#     await message.answer(f"{key}. {value}")
#     await state.set_state(QuestionList.question05)
#
#
# @dp.message(QuestionList.question05, F.text)
# async def start_cmd(message: types.Message, state: FSMContext):
#     await state.update_data(question05=message.text)
#     key = 6
#     value = questions[key]
#     await message.answer(f"{key}. {value}")
#     await state.set_state(QuestionList.question06)
#
#
# @dp.message(QuestionList.question06, F.text)
# async def start_cmd(message: types.Message, state: FSMContext):
#     await state.update_data(question06=message.text)
#     key = 7
#     value = questions[key]
#     await message.answer(f"{key}. {value}")
#     await state.set_state(QuestionList.question07)
#
#
# @dp.message(QuestionList.question07, F.text)
# async def start_cmd(message: types.Message, state: FSMContext):
#     await state.update_data(question07=message.text)
#     key = 8
#     value = questions[key]
#     await message.answer(f"{key}. {value}")
#     await state.set_state(QuestionList.question08)
#
#
# @dp.message(QuestionList.question08, F.text)
# async def start_cmd(message: types.Message, state: FSMContext):
#     await state.update_data(question08=message.text)
#     key = 9
#     value = questions[key]
#     await message.answer(f"{key}. {value}")
#     await state.set_state(QuestionList.question09)
#
#
# @dp.message(QuestionList.question09, F.text)
# async def start_cmd(message: types.Message, state: FSMContext):
#     await state.update_data(question09=message.text)
#     key = 10
#     value = questions[key]
#     await message.answer(f"{key}. {value}")
#     await state.set_state(QuestionList.question10)


# @dp.message(QuestionList.question10, F.text)
# async def start_cmd(message: types.Message, state: FSMContext):
#     await state.update_data(question10=message.text)
#     await message.answer('Вы ответили на все вопросы, вот Ваш результат:', reply_markup=ReplyKeyboardRemove(), )
#     data = await state.get_data()
#
#     for key, value in data.items():
#         for s in schemes:
#             if int(key[-2:]) in s[2]:
#                 s[3] += int(value[0])
#
#     text = ''
#     for s in schemes:
#         text += f"{s[0]} {s[1]} - {s[3]}%\n"
#     await message.answer(text, parse_mode=ParseMode.MARKDOWN)
#
#     await state.clear()
#
#     document = FSInputFile('text_test/Краткое_описание_Ранних_Дезадаптивных_Схем.docx')
#     await bot.send_document(message.chat.id, document)

async def complete_survey(message: types.Message, state: FSMContext):
    await message.answer('Вы ответили на все вопросы, вот Ваш результат:', reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()

    for key, value in data.items():
        for scheme in schemes:
            if int(key[-2:]) in scheme[2]:
                scheme[3] += int(value[0])

    result_text = '\n'.join([f"{scheme[0]} {scheme[1]} - {scheme[3]}%" for scheme in schemes])
    await message.answer(result_text, parse_mode=ParseMode.MARKDOWN)

    await state.clear()

    document = FSInputFile('data_file/Краткое_описание_Ранних_Дезадаптивных_Схем.docx')
    await bot.send_document(message.chat.id, document)


async def handle_exceptions(update, error):
    logging.exception(f"Exception: {error}")
    return True


async def main():
    print('Бот запущен')
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeDefault())
    await dp.start_polling(bot)


asyncio.run(main())

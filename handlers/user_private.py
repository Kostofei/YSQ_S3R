import time

from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from data_file.answers_list import answers
from data_file.questions_list import questions
from data_file.schemes_list import schemes

from filters.chat_types import ChatTypeFilter
from kbds.reply import del_keyboard, answer_keyboard, answer_keyboard_extended

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))

# Словарь для хранения временных меток последних сообщений
last_message_time = {}

# Время в секундах, которое должно пройти перед следующей отправкой сообщения
TIME_LIMIT = 1

# Словарь для данных теста
data_test = {}

class QuestionList(StatesGroup):
    """ Класс QuestionList представляет группу состояний для определения
    последовательности вопросов или этапов диалога с пользователем. """
    for i in range(1, 91):
        locals()[f"question{i:02d}"] = State()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    """ Функция для старта теста """
    print('Я сработал', time.strftime("%H:%M", time.localtime()), message.from_user.first_name) # удалить
    for scheme in schemes:
        scheme[3] = 0
    await message.answer(f"1. {questions[1]}", reply_markup=answer_keyboard)
    await state.set_state(QuestionList.question01)


@user_private_router.message(F.text.lower() == "информация")
@user_private_router.message(Command("info"))
async def info_cmd(message: types.Message):
    """ Функция вывода информация о тесте """
    await message.answer(
        'Данный бот предназначен для (текст описания бота).'
        '\nОтвечайте на вопросы исключительно с помощью кнопок выбора.'
        '\nКоманда /start запускает тест.'
        '\nКоманда /stop останавливает тест, все данные будут потеряны.',
        reply_markup=del_keyboard)


@user_private_router.message(F.text.lower() == "стоп")
@user_private_router.message(Command("stop"))
async def stop_cmd(message: types.Message, state: FSMContext):
    """ Функция остановки теста """
    current_state = await state.get_state()
    if current_state:
        await state.clear()
        await message.answer("Тест остановлен", reply_markup=del_keyboard)
    else:
        await message.answer("Тест не запущен, для запуска теста введите /start", reply_markup=del_keyboard)


@user_private_router.message(F.text.casefold() == 'назад')
async def handle_question_backward(message: types.Message, state: FSMContext):
    """ Функция отмены последнего ответа на вопрос """
    current_state = await state.get_state()
    if current_state == QuestionList.question01:
        await message.answer('Предидущего шага нет, или введите название товара или напишите "отмена"')
        return
    previous = None
    for step in QuestionList.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            current_question_number = int(current_state.split(':')[1][-2:]) - 1
            await message.answer(f"Вы вернулись к прошлому вопросу\n"
                                 f"{current_question_number}. {questions[current_question_number]}",
                                 reply_markup=answer_keyboard)
            return
        previous = step


@user_private_router.message(lambda message: message.text in [i for i in answers.values()])
async def handle_question(message: types.Message, state: FSMContext):
    """ Функция записываем ответы на вопросы по тесту """
    current_state = await state.get_state()
    user_id = message.from_user.id
    current_time = time.time()

    if user_id in last_message_time:
        last_message = last_message_time[user_id]
        if current_time - last_message < TIME_LIMIT:
            await message.delete()
            return

    last_message_time[user_id] = current_time
    if current_state:
        current_question_number = int(current_state.split(':')[1][-2:])
        await state.update_data({f'question{current_question_number:02}': message.text})
        next_question_number = current_question_number + 1
        if next_question_number <= 90:
            last_message_time[user_id] = current_time
            await message.answer(f"{next_question_number}. {questions[next_question_number]}",
                                 reply_markup=answer_keyboard_extended)
            await state.set_state(getattr(QuestionList, f'question{next_question_number:02}'))
        else:
            await complete_survey(message, state)
    else:
        await message.answer("Тест не запущен, для запуска введите /start", reply_markup=del_keyboard)


@user_private_router.message(F.text)
async def error_message_text(message: types.Message, state: FSMContext):
    """ Функция проверяет введенные данные """
    current_state = await state.get_state()
    if current_state:
        await message.answer('Вводите ответы с помощью клавиатуры')
    else:
        await message.answer("Для получения информации введите /info\nДля старта теста введите /start",
                             reply_markup=del_keyboard)


async def complete_survey(message: types.Message, state: FSMContext):
    """ Функция вывода данный по тесту """
    bot = complete_survey.bot
    await message.answer('Вы ответили на все вопросы, вот Ваш результат:', reply_markup=del_keyboard)
    data = await state.get_data()

    print(message.from_user.first_name)  # удалить
    for key, value in data.items():  # удалить
        print(key, ':', value)  # удалить

    for key, value in data.items():
        for scheme in schemes:
            if int(key[-2:]) in scheme[2]:
                scheme[3] += int(value[0])

    result_text = '\n'.join([f"{scheme[0]} {scheme[1]} - {(scheme[3] - 5) / 25 * 100:.0f}%" for scheme in schemes])
    await message.answer(result_text, parse_mode=ParseMode.MARKDOWN)

    await state.clear()

    document = FSInputFile('data_file/Краткое_описание_Ранних_Дезадаптивных_Схем.docx')
    await bot.send_document(message.chat.id, document)

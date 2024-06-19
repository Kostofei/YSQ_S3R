import copy
import logging
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
TIME_LIMIT = 0.5

# Словарь для данных теста
users_test_data = {}


class QuestionList(StatesGroup):
    """ Класс QuestionList представляет группу состояний для определения
    последовательности вопросов или этапов диалога с пользователем. """
    for i in range(1, 91):
        locals()[f"question{i:02d}"] = State()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    """ Функция для старта теста """
    user_id = message.from_user.id

    print('Я сработал', time.strftime("%H:%M", time.localtime()), message.from_user.first_name)  # удалить

    # Инициализация данных пользователя
    if user_id not in users_test_data:
        users_test_data[user_id] = copy.deepcopy(schemes)
    else:
        del users_test_data[user_id]
        users_test_data[user_id] = copy.deepcopy(schemes)

    # Отправка первого вопроса и установка состояния
    await message.answer(f"1. {questions[1]}", reply_markup=answer_keyboard)
    await state.set_state(QuestionList.question01)


@user_private_router.message(F.text.lower() == "информация")
@user_private_router.message(Command("info"))
async def info_cmd(message: types.Message):
    """ Функция вывода информация о тесте """

    info_text = (
        'Данный бот предназначен для прохождения тестов.\n'
        'Пользователи должны отвечать на вопросы, используя предложенные кнопки выбора.\n'
        'Основные команды:\n'
        '- /start: Запуск теста.\n'
        '- /stop: Остановка теста, все данные будут потеряны.'
    )

    await message.answer(info_text, reply_markup=del_keyboard)


@user_private_router.message(F.text.lower() == "стоп")
@user_private_router.message(Command("stop"))
async def stop_cmd(message: types.Message, state: FSMContext):
    """
    Функция остановки теста.

    Останавливает текущий тест и очищает состояние пользователя. Если тест не запущен,
    уведомляет пользователя о необходимости запуска.
    """

    current_state = await state.get_state()
    if current_state:
        await state.clear()
        stop_message = "Тест остановлен"
    else:
        stop_message = "Тест не запущен, для запуска теста введите /start"

    await message.answer(stop_message, reply_markup=del_keyboard)

@user_private_router.message(F.text.casefold() == 'назад')
async def handle_question_backward(message: types.Message, state: FSMContext):
    """
    Функция для отмены последнего ответа и возвращения к предыдущему вопросу.

    Проверяет текущее состояние пользователя и переводит его на предыдущий шаг.
    """

    current_state = await state.get_state()

    if current_state == QuestionList.question01:
        await message.answer('Предыдущего шага нет, или ответьте на вопрос или напишите "/stop"')
        return

    previous = None
    all_states = QuestionList.__all_states__

    for step in all_states:
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
    """
    Функция записываем ответы на вопросы по тесту
    """

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
    """
    Функция проверяет введенные данные
    """

    current_state = await state.get_state()
    if current_state:
        await message.answer('Вводите ответы с помощью клавиатуры')
    else:
        await message.answer("Для получения информации введите /info\nДля старта теста введите /start",
                             reply_markup=del_keyboard)


async def complete_survey(message: types.Message, state: FSMContext):
    """
    Функция вывода данный по тесту
    """

    bot = complete_survey.bot

    await message.answer('Вы ответили на все вопросы, вот Ваш результат:', reply_markup=del_keyboard)

    try:
        data = await state.get_data()
        user_id = message.from_user.id

        for key, value in data.items():
            question_id = int(key[-2:])
            answer_score = int(value[0])

            for user_test_data in users_test_data[user_id]:
                if question_id in user_test_data[2]:
                    user_test_data[3] += answer_score
                    break

        result_text = '\n'.join(
            [f"{user_test_data[0]} {user_test_data[1]} - "
             f"{(user_test_data[3] - 5) / 25 * 100:.0f}%"
             for user_test_data in users_test_data[user_id]]
        )
        await message.answer(result_text, parse_mode=ParseMode.MARKDOWN)

        await state.clear()
        del users_test_data[user_id]

        document = FSInputFile('data_file/Краткое_описание_Ранних_Дезадаптивных_Схем.docx')
        await bot.send_document(message.chat.id, document)

    except Exception as e:
        await message.answer("Произошла ошибка при обработке ваших данных. Пожалуйста, попробуйте позже.")
        logging.exception("Error while completing survey: ", exc_info=e)

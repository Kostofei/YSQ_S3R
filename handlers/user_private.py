import time

from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

# from app import bot
from data_file.answers_list import answers
from data_file.questions_list import questions
from data_file.schemes_list import schemes

from filters.chat_types import ChatTypeFilter
from kbds.reply import del_keyboard, answer_keyboard

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private', 'group']))


class QuestionList(StatesGroup):
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


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    print('Я сработал', time.strftime("%H:%M", time.localtime()), message.from_user.first_name)
    for s in schemes:
        s[3] = 0
    await message.answer(f"1. {questions[1]}", reply_markup=answer_keyboard)
    await state.set_state(QuestionList.question01)


@user_private_router.message(F.text.lower() == "информация")
@user_private_router.message(Command("info"))
async def start_cmd(message: types.Message):
    await message.answer(
        'Данный бот предназначен для (текст описания бота). Отвечайте на вопросы исключительно с помощью кнопок выбора.',
        reply_markup=del_keyboard)

@user_private_router.message(F.text.lower() == "стоп")
@user_private_router.message(Command("stop"))
async def start_cmd(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.clear()
        await message.answer("Тест остановлен",
                                 reply_markup=del_keyboard)

@user_private_router.message(lambda message: message.text in [i for i in answers.values()])
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
                             reply_markup=del_keyboard)


@user_private_router.message(F.text)
async def error_message_text(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await message.answer('Вводите ответы с помощью клавиатуры')
    else:
        await message.answer("Для получения информации введите /info\nДля старта теста введите /start",
                             reply_markup=del_keyboard)


async def complete_survey(message: types.Message, state: FSMContext):
    bot = complete_survey.bot
    await message.answer('Вы ответили на все вопросы, вот Ваш результат:', reply_markup=del_keyboard)
    data = await state.get_data()

    for key, value in data.items():
        for scheme in schemes:
            if int(key[-2:]) in scheme[2]:
                scheme[3] += int(value[0])

    result_text = '\n'.join([f"{scheme[0]} {scheme[1]} - {(scheme[3]-5)/25*100}%" for scheme in schemes])
    await message.answer(result_text, parse_mode=ParseMode.MARKDOWN)

    await state.clear()

    document = FSInputFile('data_file/Краткое_описание_Ранних_Дезадаптивных_Схем.docx')
    await bot.send_document(message.chat.id, document)

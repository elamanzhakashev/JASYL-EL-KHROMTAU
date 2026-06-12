import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Включаем логирование, чтобы видеть ошибки в консоли
logging.basicConfig(level=logging.INFO)

# Получаем токен из переменных окружения (в коде прописан твой токен как дефолт)
BOT_TOKEN = os.getenv("BOT_TOKEN", "8856434739:AAHkIWnfN5yZXhv-CIU4GYUu_dAyX9QVQMI")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- СОСТОЯНИЯ ДЛЯ РЕГИСТРАЦИИ (FSM) ---
class Form(StatesGroup):
    name = State()
    age = State()
    phone = State()

# --- КЛАВИАТУРЫ ---
def get_main_keyboard():
    buttons = [
        [KeyboardButton(text="О нас"), KeyboardButton(text="Направления")],
        [KeyboardButton(text="Жасыл ел 🌿 (Заявка)"), KeyboardButton(text="Документы для Жасыл ел")],
        [KeyboardButton(text="Контакты")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_cancel_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Отмена")]], 
        resize_keyboard=True
    )

# --- ХЕНДЛЕРЫ ---

# Команда /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    welcome_text = (
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Добро пожаловать в бот Молодёжного ресурсного центра! 🚀\n"
        "Это твоя точка сборки, хаб возможностей и свежих идей.\n\n"
        "Через этого бота ты можешь узнать всё о нашем движе, "
        "а также подать заявку в ряды бойцов «Жасыл ел» Хромтау! 🌿"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

# Кнопка "О нас"
@dp.message(F.text == "О нас")
async def about_center(message: types.Message):
    text = (
        "⚡ *МРЦ LIVE — Точка сборки креативного поколения!*\n\n"
        "Мы создали пространство, свободное от стереотипов и скучных лекций. "
        "Здесь ты можешь собрать команду для стартапа, найти единомышленников, "
        "получить поддержку или просто поработать в технологичном коворкинге.\n\n"
        "🔥 *Наша статистика:* 5000+ ребят нашли себя здесь за прошлый год!"
    )
    await message.answer(text, parse_mode="Markdown")

# Кнопка "Направления"
@dp.message(F.text == "Направления")
async def directions_center(message: types.Message):
    text = (
        "🚀 *Что тут можно делать?*\n\n"
        "🔹 *Бизнес и Стартапы:* Акселераторы идей, основы финграмотности и встречи с предпринимателями.\n"
        "🔹 *Креативные индустрии:* Школа мобилографии, подкастинг, дизайн и стрит-арт.\n"
        "🔹 *PRO-Волонтерство:* Участие в масштабных городских и международных проектах.\n"
        "🔹 *Психология & Soft Skills:* Тренинги уверенности и анонимная психологическая помощь."
    )
    await message.answer(text, parse_mode="Markdown")

# Кнопка "Контакты"
@dp.message(F.text == "Контакты")
async def contacts_center(message: types.Message):
    text = (
        "📍 *Залетай в гости! Мы всегда открыты:*\n\n"
        "🏢 Адрес: ул. Молодежная, д. 24\n"
        "📧 Email: hello@mrc-live.ru\n"
        "📞 Телефон: +7 (999) 123-45-67\n\n"
        "📲 *Наш Instagram:* [@hromtay_jastary](https://instagram.com/hromtay_jastary)\n"
        "Подписывайся на Хромтау Жастары, чтобы быть в курсе всех новостей!"
    )
    await message.answer(text, parse_mode="Markdown", disable_web_page_preview=True)

# Кнопка "Документы для Жасыл ел"
@dp.message(F.text == "Документы для Жасыл ел")
async def jasylyl_docs(message: types.Message):
    text = (
        "🌿 *Список документов для бойцов «Жасыл ел» Хромтау:*\n\n"
        "1️⃣ Копия удостоверения личности (или свидетельство о рождении).\n"
        "2️⃣ **Для лиц от 16 до 18 лет:** Письменное согласие от родителей или законных представителей (в свободной форме).\n"
        "3️⃣ Медицинская справка по форме № 075/у.\n"
        "4️⃣ Справка о наличии 20-значного банковского счета (IBAN счет на имя самого бойца).\n"
        "5️⃣ Выписка/договор из ЕНПФ (пенсионный фонд).\n\n"
        "⚠️ *Важно:* Прием строго с 16 лет! Подготовь документы заранее перед заполнением анкеты."
    )
    await message.answer(text, parse_mode="Markdown")


# --- СЦЕНАРИЙ АНКЕТИРОВАНИЯ (ЖАСЫЛ ЕЛ) ---

# Кнопка "Отмена" для выхода из FSM
@dp.message(F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Заполнение анкеты отменено.", reply_markup=get_main_keyboard())

# Старт анкеты
@dp.message(F.text == "Жасыл ел 🌿 (Заявка)")
async def start_jasylyl_form(message: types.Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer(
        "Начинаем заполнение анкеты в «Жасыл ел» Хромтау! 📝\n"
        "Вы можете прервать процесс в любой момент, написав 'Отмена'.\n\n"
        "Введите ваши *Фамилию и Имя*:", 
        reply_markup=get_cancel_keyboard(),
        parse_mode="Markdown"
    )

# Получаем Имя
@dp.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer("Укажите ваш полный возраст (цифрами, например: 17):")

# Получаем и проверяем Возраст
@dp.message(Form.age)
async def process_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите возраст цифрами!")
        return
    
    age = int(message.text)
    
    if age < 16:
        await message.answer(
            "🛑 К сожалению, набор в отряды «Жасыл ел» производится строго с 16 лет. "
            "Будем ждать тебя в следующем году!", 
            reply_markup=get_main_keyboard()
        )
        await state.clear()
        return

    await state.update_data(age=age)
    await state.set_state(Form.phone)
    await message.answer("Введите ваш контактный номер телефона для связи:")

# Получаем Телефон и финализируем
@dp.message(Form.phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    user_data = await state.get_data()
    await state.clear()

    # Здесь данные выводятся пользователю. 
    # В реальном проекте тут можно сделать отправку данных в админ-чат или Google Таблицу.
    success_text = (
        "🎉 *Заявка успешно принята!*\n\n"
        f"👤 *Боец:* {user_data['name']}\n"
        f"🔞 *Возраст:* {user_data['age']} лет\n"
        f"📞 *Контакты:* {user_data['phone']}\n\n"
        "Штаб «Жасыл ел» Хромтау свяжется с тобой в ближайшее время. "
        "Обязательно начни собирать пакет документов! 🌿"
    )
    await message.answer(success_text, parse_mode="Markdown", reply_markup=get_main_keyboard())


# Функция запуска бота
async def main():
    print("Бот успешно запущен и готов к работе...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
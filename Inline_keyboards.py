from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

API_TOKEN = ''

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# Главное меню
@dp.message_handler(Command("start"))
async def start_menu(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_calculate = types.KeyboardButton("Рассчитать")
    btn_info = types.KeyboardButton("Информация")
    keyboard.add(btn_calculate, btn_info)
    await message.answer("Выберите опцию:", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Информация")
async def main_menu(message: types.Message):
    await message.answer("Я бот помогающий твоему здоровью")

# Inline кнопки
@dp.message_handler(lambda message: message.text == "Рассчитать")
async def main_menu(message: types.Message):
    inline_keyboard = types.InlineKeyboardMarkup()
    btn_calories = types.InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
    btn_formulas = types.InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
    inline_keyboard.add(btn_calories, btn_formulas)
    await message.answer("Выберите опцию:", reply_markup=inline_keyboard)


# Обработка кнопки 'Формулы расчёта'
@dp.callback_query_handler(lambda call: call.data == 'formulas')
async def get_formulas(call: types.CallbackQuery):
    await call.answer()  # Убираем кружок загрузки
    formula_text = "Формула Миффлина-Сан Жеора: BMR = 10 * вес(кг) + 6.25 * рост(см) - 5 * возраст(лет) + 5 (для мужчин)."
    await call.message.answer(formula_text)


# Обработка кнопки 'Рассчитать норму калорий'
@dp.callback_query_handler(lambda call: call.data == 'calories')
async def set_age(call: types.CallbackQuery):
    await UserState.age.set()  # Устанавливаем состояние
    await call.message.answer("Введите свой возраст:")


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))  # Сохраняем возраст
    await UserState.growth.set()  # Переходим к следующему состоянию
    await message.answer("Введите свой рост (в см):")


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))  # Сохраняем рост
    await UserState.weight.set()  # Переходим к следующему состоянию
    await message.answer("Введите свой вес (в кг):")


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))  # Сохраняем вес
    data = await state.get_data()  # Получаем данные
    age = data['age']
    growth = data['growth']
    weight = data['weight']

    # Рассчитываем норму калорий
    bmr = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f"Ваша норма калорий: {bmr:.2f} ккал в день.")
    await state.finish()  # Завершаем состояние


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

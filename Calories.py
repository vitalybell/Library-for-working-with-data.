from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor


api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(Command("start"))
async def welcome(message: types.Message):
    await message.answer("Привет!Я бот помогающий твоему здоровью. Напишите 'Calories', "
                         "чтобы начать.")


@dp.message_handler(lambda message: message.text == 'Calories')
async def set_age(message: types.Message):
    await UserState.age.set()  # Sets the state to UserState.age
    await message.answer("Введите свой возраст:")


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))  # Update age in state data
    await UserState.growth.set()  # Set the next state
    await message.answer("Введите свой рост (в см):")


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))  # Update growth in state data
    await UserState.weight.set()  # Set the next state
    await message.answer("Введите свой вес (в кг):")


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))  # Update weight in state data
    data = await state.get_data()  # Get all stored data
    age = data['age']
    growth = data['growth']
    weight = data['weight']

    # Формула для расчета нормы калорий (Мифлин — Сан Жеор)
    # Пример для женщин:
    # BMR = 10 * weight + 6.25 * growth - 5 * age + 5
    # Если у вас нужный тип пола - измените коэффициенты в формуле
    bmr = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f"Ваша норма калорий: {bmr:.2f} ккал в день.")
    await state.finish()  # Finish the state machine


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands='start')
async def start_messege(message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Рады вас видеть в нашем боте! Напишите свой вопрос.')


@dp.message_handler()
async def all_messege(message):
    print('Введите команду /start, чтобы начать общение')
    await message.answer('Введите команду /start чтобы начать обшение')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asymcio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands='start')
async def start_messege(message):
    print('У вас сообщение')
    await message.answer('Привет! Я бот помогающий твоему здоровью.')


@dp.message_handler()
async def all_messege(message):
    print('Новое сообщение')
    await message.answer('Введите команду /start чтобы начать обшение')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

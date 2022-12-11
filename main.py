import logging
import csv

from aiogram import *  # Bot, Dispatcher, executor, types

API_TOKEN = '5818911256:AAGuz_QL2ILR5iMcWRT7cls3M0m4irwe1Wo'
CSV_MIME_TYPE = 'text/csv'
# Configure logging
logging.basicConfig(level=logging.INFO)
# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """

    await message.reply("Hi!\nI'm CSV parser bot!\nSend me your .csv file below👇.")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer('Send me your .csv file below👇')


@dp.message_handler(content_types=['document'])
async def echo(message: types.Message):
    if message.document.mime_type == CSV_MIME_TYPE:
        # todo
        await message.answer(message.document.mime_type)
    else:
        await message.answer('Expected .CSV file format, try again')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

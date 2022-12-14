import logging
import csv
import config

from plugins.execute_db_queries import Executor
from plugins.process_requests import get_response
from aiogram import *

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm CSV parser bot!\nSend me your .csv file below👇.")


@dp.message_handler()
async def process_message(message: types.Message):
    await message.answer('Send me your .csv file below👇')


@dp.message_handler(content_types=['document'])
async def process_documents(message: types.Message):
    if message.document.mime_type == config.CSV_MIME_TYPE:
        response = get_response(message)
        reader = csv.reader(response.text.split('\n'), delimiter=';')
        await message.answer('Adding parsed data from CSV file to database...')
        query = Executor(reader)
        query.execute()
        await message.answer(f'Success. {len(query.getRowData())} rows added to database.')
    else:
        await message.answer('Expected .CSV file format, try again')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

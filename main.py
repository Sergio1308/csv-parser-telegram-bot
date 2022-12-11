import logging
import csv

import aiogram.types.document
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
        print(message.document.file_id, message.document.file_name)
        src = 'documents/' + message.document.file_name
        print(bot.get_file(message.document.file_id))
        # with open(src) as csv_file:
        #     csv_reader = csv.reader(src, delimiter=',')
        #     line_count = 0
        #     for row in csv_reader:
        #         if line_count == 0:
        #             print(f'Column names are {", ".join(row)}')
        #             line_count += 1
        #         else:
        #             print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
        #             line_count += 1
        #     print(f'Processed {line_count} lines.')
        await message.answer(message.document.mime_type)
    else:
        await message.answer('Expected .CSV file format, try again')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

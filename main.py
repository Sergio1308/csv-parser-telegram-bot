import logging
import csv
import requests
import json
import db.database as db
import config

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
async def echo(message: types.Message):
    await message.answer('Send me your .csv file below👇')


@dp.message_handler(content_types=['document'])
async def echo(message: types.Message):
    if message.document.mime_type == config.CSV_MIME_TYPE:
        get_file_api_url = f'https://api.telegram.org/bot{config.API_TOKEN}/getFile'
        get_file_content_api_url = f'https://api.telegram.org/file/bot{config.API_TOKEN}/' + '{file_path}'
        response = requests.post(url=get_file_api_url, params={'file_id': message['document']['file_id']})
        json_response = json.loads(response.content)
        if response.status_code != 200 or not json_response.get('ok'):
            raise FileNotFoundError()
        response = requests.get(url=get_file_content_api_url.format(file_path=json_response['result']['file_path']))
        if response.status_code != 200:
            raise FileNotFoundError()
        reader = csv.reader(response.text.split('\n'), delimiter=';')
        # filling lists
        csv_text = []
        table_names = []
        for row in reader:
            csv_text.append(row)
        for name in csv_text[0]:
            table_names.append(name)
        # working with db
        await message.answer('Adding parsed data from CSV file to database...')
        db.create_tables(table_names)
        row_data = csv_text[1:-1]
        for fields in row_data:
            db.add_new_columns(table_names, fields)
        await message.answer(f'Success. {len(row_data)} rows added to database.')
    else:
        await message.answer('Expected .CSV file format, try again')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

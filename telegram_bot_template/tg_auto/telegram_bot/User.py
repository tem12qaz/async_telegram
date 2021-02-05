import asyncio
import logging
from aiogram import Bot
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from .Message import Message
from .database import Database

logging.basicConfig(level=logging.INFO)


class User:

    def __init__(self, telegram_id, message):
        self.telegram_id = telegram_id
        self.message = message

    def __str__(self):
        return ('User '+ str((self.telegram_id, self.message)))

    async def create_user(self):
        await Database.create_user(telegram_id=self.telegram_id, message_id=self.message)

    async def get_user_from_db(telegram_id):
        row = tuple((await Database.get_user(telegram_id=telegram_id)))
        user = User(row[1], row[2])
        return(user)

    async def update_user_in_db(self):
        await Database.update_user(telegram_id = self.telegram_id, message_id=self.message)

    async def send_message(self, bot, next_message, is_default=False):
        messages = next_message.message
        for message in messages:

            type = message.get('type')
            if type == None:
                raise TypeError(f'Не указан тип сообщения Message id{next_message[0]}')
            args = (self.telegram_id, message.get('content'))

            if not is_default:
                keyboard = ReplyKeyboardRemove()

                if message == messages[-1]:
                    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                    for answer in next_message.answers.values():
                        if answer['button']:
                            keyboard.add(KeyboardButton(answer['text']))
            else:
                keyboard = None


            if type == 'text':
                await bot.send_message(*args, reply_markup=keyboard)

            elif type == 'image':
                await bot.send_photo(*args, reply_markup=keyboard)

            elif type == 'video':
                await bot.send_video(*args, reply_markup=keyboard)

            elif type == 'audio':
                await bot.send_audio(*args, reply_markup=keyboard)

            elif type == 'document':
                await bot.send_document(*args, reply_markup=keyboard)

            else:
                raise TypeError(f'Содержимое сообщения {next_message.id} имеет неизвестный формат "{type}"')

    async def process_response_and_send_message(self, bot, message):

        old_message = Message.all.get(self.message)
        if old_message == None:
            raise IndexError(f'Сообщения с индексом {self.message} не существует')

        next_message = old_message.get_next_or_def(message.text)

        if next_message.id == old_message.default:
            await self.send_message(bot, next_message, True)
            return


        if next_message.func != None:
            next_message = next_message.execute_func_and_get_new(message)

        await self.send_message(bot, next_message)

        self.message = next_message.id
        await self.update_user_in_db()

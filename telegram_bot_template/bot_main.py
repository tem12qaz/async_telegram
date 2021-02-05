import logging
from aiogram import Bot, Dispatcher, types, executor

from tg_auto.telegram_bot.Message import Message
from tg_auto.telegram_bot.User import User
from tg_auto.telegram_bot.database import Database
from tg_auto.telegram_bot.config import API_TOKEN, WEBHOOK_HOST, WEBHOOK_PATH, WEBAPP_PORT, SECRET_KEY_2

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.executor import start_webhook

from aiohttp import web

WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    try:
        await User.get_user_from_db(message.chat.id)
    except IndexError as e:
        print(e)
        logging.info('new_user')
        new_user = User(message.chat.id, 1)
        await new_user.create_user()
        await new_user.send_message(bot, Message.all[1])
    else:
        logging.info('not_new')


@dp.message_handler()
async def main(message: types.Message):
    try:
        user = await User.get_user_from_db(message.chat.id)
    except IndexError:
        await new_user.create_user()
        await new_user.send_message(bot, Message.all[1])
    else:
        await user.process_response_and_send_message(bot, message)


async def on_startup(dp):
    await Message.load_all_messages_from_db()
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    # await dp.storage.close()
    # await dp.storage.wait_closed()
    logging.warning('Bye!')


async def reload_messages(request):
    try:
        await Message.reload_all_messages()
    except Exception as e:
        text = str(e)
    else:
        text = 'Сообщения успешно обновлены'

    return web.Response(text=text)

app = web.Application()
app.add_routes([web.get('/'+SECRET_KEY_2, reload_messages)])

if __name__ == '__main__':
    custom_executor = executor.set_webhook(dispatcher=dp,
                            webhook_path=WEBHOOK_PATH,
                            on_startup=on_startup,
                            on_shutdown=on_shutdown,
                            skip_updates=True,
                            web_app = app
    )
    custom_executor.run_app()

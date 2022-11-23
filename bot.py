from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

# * using is bad practices
from script import *

from config import API_TOKEN


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
ctx_dict = {}


@dp.message_handler()
async def echo_message(msg: types.Message):
    ctx = ctx_dict.get(msg.from_user.id, {})
    out_response, ctx = turn_handler(msg.text, ctx, actor)
    ctx_dict[msg.from_user.id] = ctx
    await bot.send_message(msg.from_user.id, out_response)


if __name__ == "__main__":
    executor.start_polling(dp)

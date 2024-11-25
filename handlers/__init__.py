from aiogram import Dispatcher
from handlers import start, balance


def register_all_handlers(dp: Dispatcher):
    dp.include_router(start.router)
    dp.include_router(balance.router)

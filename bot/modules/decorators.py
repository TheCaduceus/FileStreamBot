from hydrogram import Client 
from hydrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Union, Callable
from functools import wraps
from bot.config import Telegram
from bot.modules.static import *

def verify_user(func: Callable):

    @wraps(func)
    async def decorator(client: Client, update: Union[Message, CallbackQuery]):
        chat_id = str(update.from_user.id if update.from_user else update.chat.id)

        if not Telegram.ALLOWED_USER_IDS or chat_id in Telegram.ALLOWED_USER_IDS:
            return await func(client, update)
        elif isinstance(update, CallbackQuery):
            return await update.answer(UserNotInAllowedList, show_alert=True)
        elif isinstance(update, Message):
            return await update.reply(
                text = UserNotInAllowedList,
                quote = True,
                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Deploy Own', url='https://github.com/TheCaduceus/FileStreamBot')]])
            )
        
    return decorator

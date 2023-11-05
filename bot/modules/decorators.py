from pyrogram import Client 
from pyrogram.types import Message, CallbackQuery
from typing import Union, Callable
from functools import wraps
from bot.config import Telegram

def verify_user(func: Callable):
    
    @wraps(func)
    async def decorator(client: Client, update: Union[Message, CallbackQuery]):
        user_id = str(update.from_user.id)

        if not Telegram.ALLOWED_USER_IDS or user_id in Telegram.ALLOWED_USER_IDS:
            return await func(client, update)
    
    return decorator
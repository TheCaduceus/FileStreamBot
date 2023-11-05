from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiofiles import open as async_open
from aiofiles.os import remove as async_rm
from bot import TelegramBot, logger
from bot.config import Telegram
from bot.modules.static import *
from .deeplinks import deeplinks
from bot.modules.decorators import verify_user

@TelegramBot.on_message(filters.command('start') & filters.private)
@verify_user
async def start(_, msg: Message):
    if len(msg.command) != 1:
        return await deeplinks(msg, msg.command[1])

    await msg.reply(
        text=WelcomeText % {'first_name': msg.from_user.first_name},
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Add to Channel', url=f'https://t.me/{Telegram.BOT_USERNAME}?startchannel&admin=post_messages+edit_messages+delete_messages')
                ]
            ]
        )
    )

@TelegramBot.on_message(filters.command('info') & filters.private)
@verify_user
async def user_info(_, msg: Message):
    await msg.reply(text=f'`{msg.from_user}`', quote=True)

    filename = f'{msg.from_user.id}.json'
    async with async_open(filename, "w") as file:
        await file.write(f'{msg.from_user}')
    
    await msg.reply_document(filename)
    await async_rm(filename)

@TelegramBot.on_message(filters.private & filters.command('log') & filters.user(Telegram.OWNER_ID))
async def send_log(_, msg: Message):
    await msg.reply_document('event-log.txt', quote=True)

logger.info('Bot is now started!')
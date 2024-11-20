from hydrogram import filters
from hydrogram.types import Message
from bot import TelegramBot
from bot.modules.static import *
from bot.modules.decorators import verify_user

@TelegramBot.on_message(filters.command(['start', 'help']) & filters.private)
@verify_user
async def start_command(_, msg: Message):
    await msg.reply(
        text=WelcomeText % {'first_name': msg.from_user.first_name},
        quote=True
    )

@TelegramBot.on_message(filters.command('privacy') & filters.private)
@verify_user
async def privacy_command(_, msg: Message):
    await msg.reply(text=PrivacyText, quote=True)

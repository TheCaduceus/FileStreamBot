from telethon.events import NewMessage
from telethon.tl.custom import Message
from bot import TelegramBot
from bot.modules.decorators import verify_user
from bot.modules.telegram import get_message, send_message
from bot.modules.static import *

@TelegramBot.on(NewMessage(incoming=True, pattern=r'^/start file_'))
@verify_user(private=True)
async def send_file(event: NewMessage.Event | Message):
    payload = event.raw_text.split()[-1].split('_')

    if len(payload) != 3:
        return await event.reply(InvalidPayloadText)
    
    message = await get_message(int(payload[1]))

    if not message:
        return await event.reply(MessageNotExist)
    if payload[2] != message.raw_text:
        return await event.reply(InvalidPayloadText)
    
    message.raw_text = ''
    await send_message(message, send_to=event.chat_id)

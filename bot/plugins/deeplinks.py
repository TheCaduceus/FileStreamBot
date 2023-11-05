from pyrogram.types import Message
from bot.modules.static import *
from bot.modules.telegram import get_message

async def deeplinks(msg: Message, payload: str):
    if payload.startswith('file_'):
        sp = payload.split('_')

        if len(sp) != 3:
            return await msg.reply(InvalidPayloadText, quote=True)
        
        message = await get_message(int(sp[1]))

        if not message:
            return await msg.reply(MessageNotExist)
        if sp[2] != message.caption:
            return await msg.reply(InvalidPayloadText, quote=True)

        await message.copy(chat_id=msg.from_user.id, caption="")
    else:
        await msg.reply(InvalidPayloadText, quote=True)
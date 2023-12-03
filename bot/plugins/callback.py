from telethon.events import CallbackQuery
from bot import TelegramBot
from bot.modules.decorators import verify_user
from bot.modules.static import *
from bot.modules.telegram import get_message

@TelegramBot.on(CallbackQuery(pattern=r'^rm_'))
@verify_user(private=True)
async def delete_file(event: CallbackQuery.Event):
    query_data = event.query.data.decode().split('_')

    if len(query_data) != 3:
        return await event.answer(InvalidQueryText, alert=True)

    message = await get_message(int(query_data[1]))

    if not message:
        return await event.answer(MessageNotExist, alert=True)
    if query_data[2] != message.raw_text:
        return await event.answer(InvalidQueryText, alert=True)

    await message.delete()

    return await event.answer(LinkRevokedText, alert=True)

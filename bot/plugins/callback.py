from hydrogram.types import CallbackQuery
from hydrogram.errors import MessageDeleteForbidden
from bot import TelegramBot
from bot.modules.decorators import verify_user
from bot.modules.static import *
from bot.modules.telegram import get_message

@TelegramBot.on_callback_query()
@verify_user
async def manage_callback(_, query: CallbackQuery):
    query_data = query.data

    if query_data.startswith('rm_'):
        splited_query_data = query_data.split('_')

        if len(splited_query_data) != 3:
            return await query.answer(InvalidQueryText, show_alert=True)

        message = await get_message(int(splited_query_data[1]))

        if not message:
            return await query.answer(MessageNotExist, show_alert=True)
        
        splited_caption = message.caption.split('/')

        if query.from_user.id != int(splited_caption[1]) or splited_query_data[2] != splited_caption[0]:
            return await query.answer(InvalidQueryText, show_alert=True)
        
        try:
            await message.delete()
            await query.answer(LinkRevokedText, show_alert=True)
        except MessageDeleteForbidden: # Bot not have permission or File is older than 48 hours
            await query.answer(FileDeleteForbiddenText, show_alert=True)
    else:
        await query.answer(InvalidQueryText, show_alert=True)

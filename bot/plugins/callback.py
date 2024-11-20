from hydrogram.types import CallbackQuery
from bot import TelegramBot
from bot.modules.decorators import verify_user
from bot.modules.static import *
from bot.modules.telegram import get_message

@TelegramBot.on_callback_query()
@verify_user
async def manage_callback(bot, q: CallbackQuery):
    query = q.data

    if query.startswith('rm_'):
        sq = query.split('_')

        if len(sq) != 3:
            return await q.answer(InvalidQueryText, show_alert=True)

        message = await get_message(int(sq[1]))

        if not message:
            return await q.answer(MessageNotExist, show_alert=True)
        
        sc = message.caption.split('/')

        if q.from_user.id != int(sc[1]) or sq[2] != sc[0]:
            return await q.answer(InvalidQueryText, show_alert=True)
        
        await message.delete()
        await q.answer(LinkRevokedText, show_alert=True)
    else:
        await q.answer(InvalidQueryText, show_alert=True)

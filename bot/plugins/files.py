from hydrogram import filters
from hydrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from secrets import token_hex
from bot import TelegramBot
from bot.config import Telegram, Server
from bot.modules.decorators import verify_user
from bot.modules.static import *

@TelegramBot.on_message(
    filters.private
    & (
        filters.document
        | filters.video
        | filters.video_note
        | filters.audio
        | filters.voice
        | filters.photo
    )
)
@verify_user
async def handle_user_file(_, msg: Message):
    sender_id = msg.from_user.id
    secret_code = token_hex(Telegram.SECRET_CODE_LENGTH)
    file = await msg.copy(
        chat_id=Telegram.CHANNEL_ID,
        caption=f'||{secret_code}/{sender_id}||'
    )
    file_id = file.id
    dl_link = f'{Server.BASE_URL}/dl/{file_id}?code={secret_code}'

    if (msg.document and 'video' in msg.document.mime_type) or msg.video:
        stream_link = f'{Server.BASE_URL}/stream/{file_id}?code={secret_code}'
        await msg.reply(
            text=MediaLinksText % {'dl_link': dl_link, 'stream_link': stream_link},
            quote=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('Download', url=dl_link),
                        InlineKeyboardButton('Stream', url=stream_link)
                    ],
                    [
                        InlineKeyboardButton('Revoke', callback_data=f'rm_{file_id}_{secret_code}')
                    ]
                ]
            )
        )
    else:
        await msg.reply(
            text=FileLinksText % {'dl_link': dl_link},
            quote=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('Download', url=dl_link),
                        InlineKeyboardButton('Revoke', callback_data=f'rm_{file_id}_{secret_code}')
                    ]
                ]
            )
        )

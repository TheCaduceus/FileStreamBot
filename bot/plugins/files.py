from pyrogram import filters, errors
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
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
    secret_code = token_hex(Telegram.SECRET_CODE_LENGTH)
    file = await msg.copy(
        chat_id=Telegram.CHANNEL_ID,
        caption=f'`{secret_code}`'
    )
    file_id = file.id

    dl_link = f'{Server.BASE_URL}/dl/{file_id}?code={secret_code}'
    tg_link = f'{Server.BASE_URL}/file/{file_id}?code={secret_code}'
    deep_link = f'https://t.me/{Telegram.BOT_USERNAME}?start=file_{file_id}_{secret_code}'

    if (msg.document and 'video' in msg.document.mime_type) or msg.video:
        stream_link = f'{Server.BASE_URL}/stream/{file_id}?code={secret_code}'
        await msg.reply(
            text=MediaLinksText % {'dl_link': dl_link, 'tg_link': tg_link, 'stream_link': stream_link},
            quote=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('Download', url=dl_link),
                        InlineKeyboardButton('Stream', url=stream_link)
                    ],
                    [
                        InlineKeyboardButton('Get File', url=deep_link),
                        InlineKeyboardButton('Revoke', callback_data=f'rm_{file_id}_{secret_code}')
                    ]
                ]
            )
        )
    else:
        await msg.reply(
            text=FileLinksText % {'dl_link': dl_link, 'tg_link': tg_link},
            quote=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('Download', url=dl_link),
                        InlineKeyboardButton('Get File', url=deep_link)
                    ],
                    [
                        InlineKeyboardButton('Revoke', callback_data=f'rm_{file_id}_{secret_code}')
                    ]
                ]
            )
        )

@TelegramBot.on_message(
    filters.channel
    & ~filters.forwarded
    & ~filters.media_group
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
async def handle_channel_file(_, msg: Message):
    if msg.caption and '#pass' in msg.caption:
        return
    
    secret_code = token_hex(Telegram.SECRET_CODE_LENGTH)

    try:
        file = await msg.copy(
            chat_id=Telegram.CHANNEL_ID,
            caption=f'`{secret_code}`'
        )
    except (errors.ChatForwardsRestricted, errors.MessageIdInvalid, errors.ChannelPrivate):
        return

    file_id = file.id

    dl_link = f'{Server.BASE_URL}/dl/{file_id}?code={secret_code}'
    tg_link = f'{Server.BASE_URL}/file/{file_id}?code={secret_code}'

    if (msg.document and 'video' in msg.document.mime_type) or msg.video:
        stream_link = f'{Server.BASE_URL}/stream/{file_id}?code={secret_code}'
        await msg.edit_reply_markup(
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('Download', url=dl_link),
                        InlineKeyboardButton('Stream', url=stream_link)
                    ],
                    [
                        InlineKeyboardButton('Get File', url=tg_link)
                    ]
                ]
            )
        )
    else:
        await msg.edit_reply_markup(
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('Download', url=dl_link),
                        InlineKeyboardButton('Get File', url=tg_link)
                    ]
                ]
            )
        )
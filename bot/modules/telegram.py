from hydrogram.types import Message
from datetime import datetime
from mimetypes import guess_type
from bot import TelegramBot
from bot.config import Telegram
from bot.server.error import abort

async def get_message(message_id: int) -> Message | None:
    message = None
    
    try:
        message = await TelegramBot.get_messages(Telegram.CHANNEL_ID, message_ids=message_id)
        if message.empty: message = None
    except Exception:
        pass

    return message

async def send_message(msg: Message, send_to: int = Telegram.CHANNEL_ID) -> Message:
    return await TelegramBot.send_message(entity=send_to, message=msg)

def get_file_properties(msg: Message):
    attributes = (
        'document',
        'video',
        'audio',
        'voice',
        'photo',
        'video_note'
    )
    for attribute in attributes:
        media = getattr(msg, attribute, None)
        if media:
            file_type = attribute
            break

    if not media: abort(400, 'Unknown file type.')

    file_name = getattr(media, 'file_name', None)
    file_size = getattr(media, 'file_size', 0)

    if not file_name:
        file_format = {
            'video': 'mp4',
            'audio': 'mp3',
            'voice': 'ogg',
            'photo': 'jpg',
            'video_note': 'mp4'
        }.get(file_type)
        date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f'{file_type}-{date}.{file_format}'
    
    mime_type = guess_type(file_name)[0] or 'application/octet-stream'

    return file_name, file_size, mime_type

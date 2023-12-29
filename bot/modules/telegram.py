from telethon.events import NewMessage
from telethon.tl.custom import Message
from datetime import datetime
from mimetypes import guess_type
from bot import TelegramBot
from bot.config import Telegram
from bot.server.error import abort

async def get_message(message_id: int) -> Message | None:
    message = None
    
    try:
        message = await TelegramBot.get_messages(Telegram.CHANNEL_ID, ids=message_id)
    except Exception:
        pass

    return message

async def send_message(message:Message, send_to:int = Telegram.CHANNEL_ID) -> Message:
    return await TelegramBot.send_message(entity=send_to, message=message)

def filter_files(update: NewMessage.Event | Message):
    return bool(
        (
            update.document
            or update.photo
            or update.video
            or update.video_note
            or update.audio
            or update.gif
        )
        and not update.sticker
    )

def get_file_properties(message: Message):
    file_name = message.file.name
    file_size = message.file.size or 0
    mime_type = message.file.mime_type

    if not file_name:
        attributes = {
            'video': 'mp4',
            'audio': 'mp3',
            'voice': 'ogg',
            'photo': 'jpg',
            'video_note': 'mp4'
        }

        for attribute in attributes:
            media = getattr(message, attribute, None)
            if media:
                file_type, file_format = attribute, attributes[attribute]
                break
        
        if not media:
            abort(400, 'Invalid media type.')

        date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f'{file_type}-{date}.{file_format}'
    
    if not mime_type:
        mime_type = guess_type(file_name)[0] or 'application/octet-stream'
    
    return file_name, file_size, mime_type

from quart import Blueprint, Response, request, render_template, redirect
from math import ceil
from re import match as re_match
from .error import abort
from bot import TelegramBot
from bot.config import Telegram, Server
from bot.modules.telegram import get_message, get_file_properties

bp = Blueprint('main', __name__)

@bp.route('/')
async def home():
    return redirect(f'https://t.me/{Telegram.BOT_USERNAME}')

@bp.route('/dl/<int:file_id>')
async def transmit_file(file_id):
    file = await get_message(file_id) or abort(404)
    code = request.args.get('code') or abort(401)
    range_header = request.headers.get('Range')

    if code != file.caption.split('/')[0]:
        abort(403)

    file_name, file_size, mime_type = get_file_properties(file)

    start = 0
    end = file_size - 1
    chunk_size = 1 * 1024 * 1024  # 1 MB

    if range_header:
        range_match = re_match(r'bytes=(\d+)-(\d*)', range_header)
        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2)) if range_match.group(2) else file_size - 1
            if start > end or start >= file_size:
                abort(416, 'Requested range not satisfiable')
        else:
            abort(400, 'Invalid Range header')

    offset_chunks = start // chunk_size
    total_bytes_to_stream = end - start + 1
    chunks_to_stream = ceil(total_bytes_to_stream / chunk_size)

    content_length = total_bytes_to_stream
    headers = {
        'Content-Type': mime_type,
        'Content-Disposition': f'attachment; filename={file_name}',
        'Content-Range': f'bytes {start}-{end}/{file_size}',
        'Accept-Ranges': 'bytes',
        'Content-Length': str(content_length),
    }
    status_code = 206 if range_header else 200

    async def file_stream():
        bytes_streamed = 0
        chunk_index = 0
        async for chunk in TelegramBot.stream_media(
            file,
            offset=offset_chunks,
            limit=chunks_to_stream,
        ):
            if chunk_index == 0: # Trim the first chunk if necessary
                trim_start = start % chunk_size
                if trim_start > 0:
                    chunk = chunk[trim_start:]

            remaining_bytes = content_length - bytes_streamed
            if remaining_bytes <= 0:
                break

            if len(chunk) > remaining_bytes: # Trim the last chunk if necessary
                chunk = chunk[:remaining_bytes]

            yield chunk
            bytes_streamed += len(chunk)
            chunk_index += 1

    return Response(file_stream(), headers=headers, status=status_code)

@bp.route('/stream/<int:file_id>')
async def stream_file(file_id):
    code = request.args.get('code') or abort(401)
    return await render_template('player.html', mediaLink=f'{Server.BASE_URL}/dl/{file_id}?code={code}')

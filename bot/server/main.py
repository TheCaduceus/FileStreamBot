from quart import Blueprint, Response, request, render_template, redirect
from .error import abort
from bot import version, TelegramBot
from bot.config import Telegram, Server
from bot.modules.telegram import get_message, get_file_properties

bp = Blueprint('main', __name__)

@bp.route('/')
async def home():
    return redirect(f'https://t.me/{Telegram.BOT_USERNAME}')

@bp.route('/dl/<int:file_id>')
async def transmit_file(file_id):
    file = await get_message(int(file_id)) or abort(404)
    code = request.args.get('code') or abort(401)

    if code != file.caption:
        abort(403)
    
    file_name, mime_type = await get_file_properties(file)
    headers = {
        'Content-Type': mime_type,
        'Content-Disposition': f'attachment; filename="{file_name}"'
    }

    file_stream = TelegramBot.stream_media(file)

    return Response(file_stream, headers=headers)

@bp.route('/stream/<int:file_id>')
async def stream_file(file_id):
    code = request.args.get('code') or abort(401)

    return await render_template('player.html', mediaLink=f'{Server.BASE_URL}/dl/{file_id}?code={code}')

@bp.route('/file/<int:file_id>')
async def file_deeplink(file_id):
    code = request.args.get('code') or abort(401)

    return redirect(f'https://t.me/{Telegram.BOT_USERNAME}?start=file_{file_id}_{code}')
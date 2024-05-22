import re
from telethon import Button, events
from telethon.events import NewMessage
from telethon.tl.custom.message import Message
from bot import TelegramBot
from bot.config import Telegram
from bot.modules.static import *
from bot.modules.decorators import verify_user
from bot.database import db

@TelegramBot.on(NewMessage(incoming=True, pattern=r'^/start$'))
@verify_user(private=True)
async def welcome(event: Message):
    if await db.is_inserted("ban", event.sender_id):
        return await event.reply("You are banned")
    await event.reply(
        message=WelcomeText % {'first_name': event.sender.first_name}
    )
    if not await db.is_inserted("users", event.sender_id):
        await db.insert("users", event.sender_id)

@TelegramBot.on(NewMessage(incoming=True, pattern=r'^/info$'))
@verify_user(private=True)
async def user_info(event: Message):
    await event.reply(UserInfoText.format(sender=event.sender))

@TelegramBot.on(NewMessage(chats=Telegram.OWNER_ID, incoming=True, pattern=r'^/logs$'))
async def send_log(event: Message):
    await event.reply(file='event-log.txt')

@TelegramBot.on(NewMessage(chats=Telegram.OWNER_ID, incoming=True, pattern=r'^/users$'))
@verify_user(private=True)
async def users(event: Message):
    total_users = len(await db.fetch_all("users"))
    await event.reply(f'Total Users Count: {total_users}')

@TelegramBot.on(NewMessage(chats=Telegram.OWNER_ID, incoming=True, pattern=r'^/ban (\d+)$'))
@verify_user(private=True)
async def ban_user(event: Message):
    match = re.match(r'^/ban (\d+)$', event.raw_text)
    if not match:
        await event.reply("Please provide a valid user ID.")
        return
    user_id = int(match.group(1))
    if not await db.is_inserted("ban", user_id):
        await db.insert("ban", user_id)
    await event.reply('User banned!')

@TelegramBot.on(NewMessage(chats=Telegram.OWNER_ID, incoming=True, pattern=r'^/unban (\d+)$'))
@verify_user(private=True)
async def unban_user(event: Message):
    match = re.match(r'^/unban (\d+)$', event.raw_text)
    if not match:
        await event.reply("Please provide a valid user ID.")
        return
    user_id = int(match.group(1))
    if await db.is_inserted("ban", user_id):
        await db.delete("ban", user_id)
    await event.reply('User unbanned!')

@TelegramBot.on(NewMessage(chats=Telegram.OWNER_ID, incoming=True, pattern=r'^/cban (\d+)$'))
@verify_user(private=True)
async def ban_channel(event: Message):
    match = re.match(r'^/cban (\d+)$', event.raw_text)
    if not match:
        await event.reply("Please provide a valid channel ID.")
        return
    channel_id = int(match.group(1))
    if not await db.is_inserted("cban", channel_id):
        await db.insert("cban", channel_id)
    await event.reply('channel banned!')

@TelegramBot.on(NewMessage(chats=Telegram.OWNER_ID, incoming=True, pattern=r'^/cunban (\d+)$'))
@verify_user(private=True)
async def unban_channel(event: Message):
    match = re.match(r'^/cunban (\d+)$', event.raw_text)
    if not match:
        await event.reply("Please provide a valid channel ID.")
        return
    channel_id = int(match.group(1))
    if await db.is_inserted("cban", channel_id):
        await db.delete("cban", channel_id)
    await event.reply('channel unbanned!')

@TelegramBot.on(NewMessage(chats=Telegram.OWNER_ID, incoming=True, pattern=r'^/bcast$'))
@verify_user(private=True)
async def bcast(event: Message):
    if not event.reply_to_msg_id:
        return await event.reply(
            "Please use `/bcast` as reply to the message you want to broadcast."
        )
    msg = await event.get_reply_message()
    xx = await event.reply("In progress...")
    users = await db.fetch_all('users')
    done = error = 0
    for user_id in users:
        try:
            await TelegramBot.send_message(
                int(user_id),
                msg.text.format(user=(await TelegramBot.get_entity(int(user_id))).first_name),
                file=msg.media,
                buttons=msg.buttons,
                link_preview=False,
            )
            done += 1
        except Exception as brd_er:
            log.error("Broadcast error:\nChat: %d\nError: %s", int(user_id), brd_er)
            error += 1
    await xx.edit(f"Broadcast completed.\nSuccess: {done}\nFailed: {error}")

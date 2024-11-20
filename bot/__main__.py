from bot import TelegramBot
from bot.server import server

if __name__ == '__main__':
    TelegramBot.loop.create_task(server.serve())
    TelegramBot.run()

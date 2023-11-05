from bot import TelegramBot, logger
from bot.server import server

if __name__ == '__main__':
    logger.info('Initializing...')
    TelegramBot.loop.create_task(server.serve())
    TelegramBot.run()
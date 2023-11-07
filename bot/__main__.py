from bot import TelegramBot, logger
from bot.server import run_server

if __name__ == '__main__':
    logger.info('Initializing...')
    TelegramBot.loop.create_task(run_server())
    TelegramBot.run()

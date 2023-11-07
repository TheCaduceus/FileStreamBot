from quart import Quart
from hypercorn import Config
from hypercorn.asyncio import serve
from logging import getLogger
from bot.config import Server, LOGGER_CONFIG_JSON

from . import main, error

logger = getLogger('hypercorn')
instance = Quart(__name__)

@instance.before_serving
async def before_serve():
    logger.info('Web server is started!')
    logger.info(f'Server running on {Server.BIND_ADDRESS}:{Server.PORT}')

instance.register_blueprint(main.bp)

instance.register_error_handler(400, error.invalid_request)
instance.register_error_handler(404, error.not_found)
instance.register_error_handler(405, error.invalid_method)
instance.register_error_handler(error.HTTPError, error.http_error)

async def run_server():
    config = Config()
    config.bind = [f'{Server.BIND_ADDRESS}:{Server.PORT}']
    config.logconfig_dict = LOGGER_CONFIG_JSON 

    await serve(instance, config)

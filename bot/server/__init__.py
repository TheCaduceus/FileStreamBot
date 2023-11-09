from quart import Quart
from uvicorn import Server as UvicornServer, Config
from logging import getLogger
from bot.config import Server, LOGGER_CONFIG_JSON

from . import main, error

logger = getLogger('uvicorn')
instance = Quart(__name__)
instance.config['RESPONSE_TIMEOUT'] = None

@instance.before_serving
async def before_serve():
    logger.info('Web server is started!')
    logger.info(f'Server running on {Server.BIND_ADDRESS}:{Server.PORT}')

instance.register_blueprint(main.bp)

instance.register_error_handler(400, error.invalid_request)
instance.register_error_handler(404, error.not_found)
instance.register_error_handler(405, error.invalid_method)
instance.register_error_handler(error.HTTPError, error.http_error)

server = UvicornServer (
    Config (
        app=instance,
        host=Server.BIND_ADDRESS,
        port=Server.PORT,
        log_config=LOGGER_CONFIG_JSON
    )
)

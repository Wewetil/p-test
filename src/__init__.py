from aiologger import Logger
from aiologger.formatters.base import Formatter
from aiologger.handlers.streams import AsyncStreamHandler
from aiologger.levels import LogLevel

from src.config import settings
from src.db import Base, get_async_session

logger = Logger(name='p-test', level=LogLevel.DEBUG)
afh = AsyncStreamHandler()
afh.formatter = Formatter('%(levelname)s: [%(asctime)s] %(message)s')
logger.add_handler(afh)

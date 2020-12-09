import sys

from loguru import logger
from webforces.server.auth import Auth
from webforces.server.interface.dbworker import DBWorker
from webforces.server.mongodbworker import MongoDBWorker


class Core:
    _instance = None
    auth: Auth = None
    _is_done: bool = False
    db: DBWorker = None

    def __init__(self, validation=False) -> None:
        """Initialization of webforces core

        Parameters:
            validation (bool): Set to true if validation is running
        """
        if self._is_done:
            return
        self._setup_logging()
        logger.debug("Core init")
        self.auth = Auth()
        self.db = MongoDBWorker(validation)
        #self._is_done = True

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Core, cls).__new__(cls)
        return cls._instance

    def _setup_logging(self, level="DEBUG"):
        logger.remove()
        fmt = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: ^7}</level> | {name}.{function}:{line} - "
            "<level>{message}</level>")
        logger.add(sys.stderr, level=level, format=fmt)

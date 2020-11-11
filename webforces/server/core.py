import sys

from loguru import logger
from webforces.server.interface.dbworker import DBWorker
from webforces.server.mongodbworker import MongoDBWorker


class Core:
    _instance = None
    db: DBWorker = None

    def __init__(self) -> None:
        self._setup_logging()
        logger.debug("Core init")
        self.db = MongoDBWorker()

    def __new__(cls):
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

import sys
sys.path.append('../')
sys.path.append('../../')
import pymongo
from loguru import logger
from webforces.server.interface import dbworker
from webforces.settings import MONGODB_PROPERTIES


class MongoDBWorker(dbworker.DBWorker):
    client: pymongo.MongoClient = None

    def __init__(self) -> None:
        self.connect()

    def connect(self) -> int:
        if self.client is not None:
            logger.error("Databate is already connected!")
        self.client = pymongo.MongoClient(MONGODB_PROPERTIES['production_url'])
        self.db = self.client.webforces
        try:
            # <PLACEHOLDER>
            if "stats" not in self.db.list_collection_names():
                stats_collection = self.db["stats"]
                stats_collection.insert_one({
                    "name": "webforces",
                })
            # </PLACEHOLDER>
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return 1
        else:
            logger.debug(f"MongoDBWorker is connected to {MONGODB_PROPERTIES['production_url']}")
            return 0

    def disconnect(self) -> int:
        return 0


if __name__ == "__main__":
    MDB = MongoDBWorker()

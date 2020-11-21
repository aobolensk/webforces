import sys
sys.path.append('../')
sys.path.append('../../')
import pymongo
from structs import User
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

    def getUserByID(self, id) -> dict():
        try:
            # <PLACEHOLDER>
            users_collection = self.db["users"]
            user_d = users_collection.find_one({"_id": id})
            if user_d is None:
                logger.error("This user is not exist")
                return 2
            # </PLACEHOLDER>
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return 1
        logger.debug("User was found")
        return user_d

    def getUserByLogin(self, login) -> dict():
        try:
            # <PLACEHOLDER>
            users_collection = self.db["users"]
            user_d = users_collection.find_one({"login": login})
            if user_d is None:
                logger.error("This user is not exist")
                return 2
            # </PLACEHOLDER>
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return 1
        logger.debug("User was found")
        return user_d

    def addUser(self, user_d) -> str:
        try:
            # <PLACEHOLDER>
            users_collection = self.db["users"]
            if users_collection.find_one({"login": user_d["login"]}) is not None:
                logger.error("This login is already taken")
                return 2
            id = users_collection.insert_one(user_d).inserted_id
            # </PLACEHOLDER>
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return 1
        logger.debug("New user was successfully added")
        return id

if __name__ == "__main__":
    MDB = MongoDBWorker()
    user = User(1, "login1", "fn", "sn", "mn", [0])
    user_d = user.__dict__
    #MDB.addUser(user_d)
    user_d2 = MDB.getUserByLogin("login1")
    print(user_d2["_id"])
    user_d3 = MDB.getUserByID(user_d2["_id"])
    print(user_d2 == user_d3)

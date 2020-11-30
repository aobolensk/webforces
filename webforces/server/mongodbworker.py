import pymongo
from loguru import logger
from webforces.server.structs import DBStatus, User
from webforces.server.interface import dbworker
from webforces.settings import MONGODB_PROPERTIES


class MongoDBWorker(dbworker.DBWorker):
    client: pymongo.MongoClient = None
    db_url: str = ''
    db_name: str = ''

    def __init__(self, validation=False) -> None:
        if not validation:
            self.db_url = MONGODB_PROPERTIES['production_url']
            self.db_name = "webforces"
        else:
            self.db_url = MONGODB_PROPERTIES['validation_url']
            self.db_name = "webforces_val"
        self.connect()

    def connect(self) -> int:
        if self.client is not None:
            logger.warning("Databate is already connected")
        self.client = pymongo.MongoClient(self.db_url)
        self.db = getattr(self.client, self.db_name)
        try:
            self._populateIds()
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return DBStatus.s_connection_error
        else:
            logger.debug(f"MongoDBWorker is connected to {self.db_url}")
            return DBStatus.s_ok

    def disconnect(self) -> int:
        return DBStatus.s_ok

    def _populateIds(self):
        to_insert = [
            {"name": "users", "last_id": 0},
            {"name": "tasks", "last_id": 0}
        ]
        id_collection = self.db["id"]
        id_collection.insert_many(to_insert)
        logger.debug("ID collection was created")

    def dropAll(self) -> None:
        (self.db["id"]).drop()
        (self.db["users"]).drop()
        (self.db["algorithms"]).drop()
        (self.db["tests"]).drop()
        (self.db["tasks"]).drop()
        logger.debug("Collections were dropped")

    # "users"       - get the last user ID + 1
    # "tasks"       - get the last task ID + 1
    # user_id + "u" - get ID of the last binded alg for this user + 1
    # alg_id + "a"  - get ID of the last added test for this alg + 1
    def _getNextID(self, name) -> int:
        try:
            id_collection = self.db["id"]
            dict = id_collection.find_one({"name": name})
            new_id = dict["last_id"] + 1
            id_collection.update_one(
                {"name": name},
                {"$set": {"last_id": new_id}}
            )
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return DBStatus.s_data_issue
        return new_id

    def _insertOneID(self, name) -> int:
        try:
            id_collection = self.db["id"]
            id_collection.insert_one(
                {"name": name, "last_id": 0}
            )
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return DBStatus.s_data_issue
        return DBStatus.s_ok

    def addUser(self, user) -> (DBStatus, User):
        try:
            users_collection = self.db["users"]
            if users_collection.find_one({"login": user.login}) is not None:
                logger.error("This login is already taken")
                return (DBStatus.s_data_issue, User(-100))
            user.user_id = self._getNextID("users")
            if user.user_id == DBStatus.s_data_issue:
                return (DBStatus.s_connection_error, User(-100))
            users_collection.insert_one(user.__dict__)
            if self._insertOneID(str(user.user_id) + "u") == DBStatus.s_data_issue:
                return (DBStatus.s_connection_error, User(-100))
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return (DBStatus.s_connection_error, User(-100))
        logger.debug("New user was successfully added")
        return (DBStatus.s_ok, user)

    def getUserByID(self, user_id) -> (DBStatus, User):
        try:
            users_collection = self.db["users"]
            user_d = users_collection.find_one({"user_id": user_id})
            if user_d is None:
                logger.error("This user does not exist")
                return (DBStatus.s_data_issue, User(-100))
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return (DBStatus.s_connection_error, User(-100))
        logger.debug("User was found")
        return (DBStatus.s_ok, User.fromDict(user_d))

    def getUserByLogin(self, login) -> (DBStatus, User):
        try:
            users_collection = self.db["users"]
            user_d = users_collection.find_one({"login": login})
            if user_d is None:
                logger.error("This user does not exist")
                return (DBStatus.s_data_issue, User(-100))
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return (DBStatus.s_connection_error, User(-100))
        logger.debug("User was found")
        return (DBStatus.s_ok, User.fromDict(user_d))

# TODO
    def getAlgByTitle(self, title) -> dict():
        try:
            algs_collection = self.db["algorithms"]
            alg_d = algs_collection.find_one({"title": title})
            if alg_d is None:
                logger.error("This algorithm does not exist")
                return 2
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return 1
        logger.debug("Algorithm was found")
        return alg_d

    def getAlgByID(self, id) -> dict():
        try:
            algs_collection = self.db["algorithms"]
            alg_d = algs_collection.find_one({"_id": id})
            if alg_d is None:
                logger.error("This algorithm does not exist")
                return 2
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return 1
        logger.debug("Algorithm was found")
        return alg_d

    def addAlg(self, alg_d):
        try:
            algs_collection = self.db["algorithms"]
            if algs_collection.find_one({"title": alg_d["title"]}) is not None:
                logger.error("This algorithm already exists")
                return 2
            id = algs_collection.insert_one(alg_d).inserted_id
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return 1
        logger.debug("New algorithm was successfully added")
        return id

    def bindAlgToUser(self, user_id, alg_id) -> int:
        try:
            user_d = self.getUserByID(user_id)
            alg_d = self.getAlgByID(alg_id)
            print(len(user_d["algs_id"]))
            for alg in user_d["algs_id"]:
                if alg["title"] == alg_d["title"]:
                    logger.error("This algorithm is already binded")
                    return 2
            # update author's list of algs
            new_list_algs = (user_d["alg_id"]).append(alg_id)
            users_collection = self.db["users"]
            users_collection.update_one(
                {"_id": user_id},
                {"$set": {"algs_id": new_list_algs}})
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return 1
        logger.debug("Algorithm was successfully binded")
        return 0

    def getTestByID(self, id) -> dict():
        try:
            tests_collection = self.db["tests"]
            test_d = tests_collection.find_one({"_id": id})
            if test_d is None:
                logger.error("This test does not exist")
                return 2
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return 1
        logger.debug("Test was found")
        return test_d

    def _addTest(self, test_d):
        try:
            tests_collection = self.db["tests"]
            id = tests_collection.insert_one(test_d).inserted_id
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return 1
        return id

    def addTest(self, user_id, test_d):
        try:
            user_d = self.getUserByID(user_id)
            for test in user_d["algs_id"]:
                if test["title"] == test_d["title"]:
                    logger.error("This test already exists")
                    return 2
            test_id = self._addTest(test_d)  # add test to tests table
            new_list_tests = (user_d["alg_id"]).append(test_id)
            users_collection = self.db["users"]
            # update author's list of algs
            users_collection.update_one(
                {"_id": user_id},
                {"$set": {"algs_id": new_list_tests}})
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return 1
        logger.debug("New test was successfully added")
        return test_id

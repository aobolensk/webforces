from typing import Tuple, List

import pymongo
from loguru import logger
from webforces.server.structs import DBStatus, User, Algorithm, Test
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
            {"name": "users", "last_id": "0"},
            {"name": "tasks", "last_id": "0"}
        ]
        id_collection = self.db["id"]
        id_collection.insert_many(to_insert)
        logger.debug("ID collection was created")

    def dropAll(self) -> None:
        (self.db["id"]).drop()
        (self.db["users"]).drop()
        (self.db["algs"]).drop()
        (self.db["tests"]).drop()
        (self.db["tasks"]).drop()
        logger.debug("Collections were dropped")

    # "users"                      - get the last user ID + 1
    # "tasks"                      - get the last task ID + 1
    # user_id + "u"                - get ID of the last binded alg for this user + 1
    # user_id + "u" + alg_id + "a" - get ID of the last added test for this alg + 1
    def _getNextID(self, name) -> int:
        try:
            id_collection = self.db["id"]
            dict = id_collection.find_one({"name": name})
            if dict is None:
                return DBStatus.s_data_issue
            new_id = int(dict["last_id"]) + 1
            id_collection.update_one(
                {"name": name},
                {"$set": {"last_id": str(new_id)}}
            )
        except Exception as e:
            return DBStatus.s_data_issue
        return new_id

    def _insertOneID(self, name) -> int:
        try:
            id_collection = self.db["id"]
            id_collection.insert_one(
                {"name": name, "last_id": "0"}
            )
        except Exception as e:
            return DBStatus.s_data_issue
        return DBStatus.s_ok

    def addUser(self, user) -> Tuple[DBStatus, User]:
        try:
            # check login
            st = (self.getUserByLogin(user.login))[0]
            if st != DBStatus.s_data_issue:
                logger.error("This login is already taken")
                return (DBStatus.s_data_issue, User(-100))
            # add user
            users_collection = self.db["users"]
            user.user_id = self._getNextID("users")
            if user.user_id == DBStatus.s_data_issue:
                return (DBStatus.s_connection_error, User(-100))
            if self._insertOneID(str(user.user_id) + "u") == DBStatus.s_data_issue:
                return (DBStatus.s_connection_error, User(-100))
            users_collection.insert_one(user.__dict__)
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return (DBStatus.s_connection_error, User(-100))
        logger.debug("New user was successfully added")
        return (DBStatus.s_ok, user)

    def getUserByID(self, user_id) -> Tuple[DBStatus, User]:
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

    def getUserByLogin(self, login) -> Tuple[DBStatus, User]:
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

    def addAlg(self, alg) -> Tuple[DBStatus, Algorithm]:
        try:
            # check user
            st, user = self.getUserByID(alg.author_id)
            if st == DBStatus.s_data_issue:
                logger.error("This user does not exist")
                return (DBStatus.s_data_issue, Algorithm(-100))
            # check title
            st, alg_check = self.getAlgByTitle(alg.title)
            if st != DBStatus.s_data_issue:
                logger.error("This algorithm already exists")
                return (DBStatus.s_data_issue, Algorithm(-100))
            # add alg
            algs_collection = self.db["algs"]
            alg.alg_id = self._getNextID(str(user.user_id) + "u")
            if alg.alg_id == DBStatus.s_data_issue:
                logger.error("This user does not exist")
                return (DBStatus.s_data_issue, Algorithm(-100))
            if self._insertOneID(str(alg.author_id) + "u" + str(alg.alg_id) + "a") == DBStatus.s_data_issue:
                return (DBStatus.s_connection_error, Algorithm(-100))
            algs_collection.insert_one(alg.__dict__)
            # update author's list of algs
            new_list_algs = user.algs_id
            new_list_algs.append(alg.alg_id)
            users_collection = self.db["users"]
            users_collection.update_one(
                {"user_id": user.user_id},
                {"$set": {"algs_id": new_list_algs}})
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return (DBStatus.s_connection_error, Algorithm(-100))
        logger.debug("New algorithm was successfully added")
        return (DBStatus.s_ok, alg)

    def getAlgByTitle(self, title) -> Tuple[DBStatus, Algorithm]:
        try:
            algs_collection = self.db["algs"]
            alg_d = algs_collection.find_one({"title": title})
            if alg_d is None:
                logger.error("This algorithm does not exist")
                return (DBStatus.s_data_issue, Algorithm(-100))
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return (DBStatus.s_connection_error, Algorithm(-100))
        logger.debug("Algorithm was found")
        return (DBStatus.s_ok, Algorithm.fromDict(alg_d))

    def getAuthorAlgByAlgID(self, author_id, alg_id) -> Tuple[DBStatus, Algorithm]:
        try:
            # check user
            st, author = self.getUserByID(author_id)
            if st == DBStatus.s_data_issue:
                logger.error("This user does not exist")
                return (DBStatus.s_data_issue, Algorithm(-100))
            # get alg
            algs_collection = self.db["algs"]
            alg_d = algs_collection.find_one({"alg_id": alg_id, "author_id": author_id})
            if alg_d is None:
                logger.error("This algorithm does not exist")
                return (DBStatus.s_data_issue, Algorithm(-100))
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return (DBStatus.s_connection_error, Algorithm(-100))
        logger.debug("Algorithm was found")
        return (DBStatus.s_ok, Algorithm.fromDict(alg_d))

    def getAllAuthorAlgs(self, author_id) -> Tuple[DBStatus, List[Algorithm]]:
        try:
            # check user
            st, author = self.getUserByID(author_id)
            if st == DBStatus.s_data_issue:
                logger.error("This user does not exist")
                return (DBStatus.s_data_issue, [Algorithm(-100)])
            # get algs
            algs_collection = self.db["algs"]
            algs = []
            for alg_id in author.algs_id:
                alg_d = algs_collection.find_one({"alg_id": alg_id, "author_id": author_id})
                algs.append(Algorithm.fromDict(alg_d))
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return (DBStatus.s_connection_error, [Algorithm(-100)])
        logger.debug("Algorithms was found")
        return (DBStatus.s_ok, algs)

# TODO
    def bindAlg(self, alg_id, user_id) -> DBStatus:
        try:
            user = self.getUserByID(user_id)
            for a in user.algs_id:
                if a.title == alg.title:
                    logger.error("This algorithm is already binded")
                    return DBStatus
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

    def getAlgByID(self, id) -> dict():
        try:
            algs_collection = self.db["algs"]
            alg_d = algs_collection.find_one({"_id": id})
            if alg_d is None:
                logger.error("This algorithm does not exist")
                return 2
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return 1
        logger.debug("Algorithm was found")
        return alg_d

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

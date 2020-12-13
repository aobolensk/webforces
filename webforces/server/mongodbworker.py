from typing import Tuple, List

import pymongo
from loguru import logger
from webforces.server.structs import DBStatus, ERROR_ID, User, Algorithm, Test, Task, Stats
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
    # user_id + "u"                - get ID of the last added alg for this user + 1
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
            logger.error(f"MongoDBWorker connection failed: {e}")
            return DBStatus.s_data_issue
        return new_id

    def _insertOneID(self, name) -> int:
        try:
            id_collection = self.db["id"]
            id_collection.insert_one(
                {"name": name, "last_id": "0"}
            )
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return DBStatus.s_data_issue
        return DBStatus.s_ok

    def addUser(self, user) -> Tuple[DBStatus, User]:
        try:
            # check login
            st = (self.getUserByLogin(user.login))[0]
            if st != DBStatus.s_data_issue:
                logger.error("This login is already taken")
                return (DBStatus.s_data_issue, User(ERROR_ID))
            # add user
            users_collection = self.db["users"]
            user.user_id = self._getNextID("users")
            if user.user_id == DBStatus.s_data_issue:
                return (DBStatus.s_connection_error, User(ERROR_ID))
            if self._insertOneID(str(user.user_id) + "u") == DBStatus.s_data_issue:
                return (DBStatus.s_connection_error, User(ERROR_ID))
            users_collection.insert_one(user.__dict__)
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return (DBStatus.s_connection_error, User(ERROR_ID))
        logger.debug("New user was successfully added")
        return (DBStatus.s_ok, user)

    def updUser(self, user) -> DBStatus:
        try:
            users_collection = self.db["users"]
            user_d = users_collection.find_one({"user_id": user.user_id})
            if user_d is None:
                logger.error("This user does not exist")
                return DBStatus.s_data_issue
            user_d = users_collection.update_one(
                {"user_id": user.user_id}, {"$set": {
                    "first_name": user.first_name,
                    "second_name": user.second_name,
                    "middle_name": user.middle_name,
                }})
            if user_d is None:
                logger.error("User update failed")
                return DBStatus.s_data_issue
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return DBStatus.s_connection_error
        logger.debug("User was updated")
        return DBStatus.s_ok

    def getUserByID(self, user_id) -> Tuple[DBStatus, User]:
        try:
            users_collection = self.db["users"]
            user_d = users_collection.find_one({"user_id": user_id})
            if user_d is None:
                logger.error("This user does not exist")
                return (DBStatus.s_data_issue, User(ERROR_ID))
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return (DBStatus.s_connection_error, User(ERROR_ID))
        logger.debug("User was found")
        return (DBStatus.s_ok, User.fromDict(user_d))

    def getUserByLogin(self, login) -> Tuple[DBStatus, User]:
        try:
            users_collection = self.db["users"]
            user_d = users_collection.find_one({"login": login})
            if user_d is None:
                logger.error("This user does not exist")
                return (DBStatus.s_data_issue, User(ERROR_ID))
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return (DBStatus.s_connection_error, User(ERROR_ID))
        logger.debug("User was found")
        return (DBStatus.s_ok, User.fromDict(user_d))

    def getAllUsers(self) -> Tuple[DBStatus, List[User]]:
        try:
            users_collection = self.db["users"]
            users_tmp = list(users_collection.find({}))
            users = []
            for user_d in users_tmp:
                users.append(User.fromDict(user_d))
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return (DBStatus.s_connection_error, [User(ERROR_ID)])
        logger.debug("Users was found")
        return (DBStatus.s_ok, users)

    def addAlg(self, alg) -> Tuple[DBStatus, Algorithm]:
        try:
            # check user
            st, user = self.getUserByID(alg.author_id)
            if st == DBStatus.s_data_issue:
                logger.error("This user does not exist")
                return (DBStatus.s_data_issue, Algorithm(ERROR_ID))
            # check title
            st, alg_check = self.getAlgByTitle(alg.title)
            if st != DBStatus.s_data_issue:
                logger.error("This algorithm already exists")
                return (DBStatus.s_data_issue, Algorithm(ERROR_ID))
            # add alg
            algs_collection = self.db["algs"]
            alg.alg_id = self._getNextID(str(user.user_id) + "u")
            if alg.alg_id == DBStatus.s_data_issue:
                logger.error("This user does not exist")
                return (DBStatus.s_data_issue, Algorithm(ERROR_ID))
            if self._insertOneID(str(alg.author_id) + "u" + str(alg.alg_id) + "a") == DBStatus.s_data_issue:
                return (DBStatus.s_connection_error, Algorithm(ERROR_ID))
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
            return (DBStatus.s_connection_error, Algorithm(ERROR_ID))
        logger.debug("New algorithm was successfully added")
        return (DBStatus.s_ok, alg)

    def getAlgByTitle(self, title) -> Tuple[DBStatus, Algorithm]:
        try:
            algs_collection = self.db["algs"]
            alg_d = algs_collection.find_one({"title": title})
            if alg_d is None:
                logger.error("This algorithm does not exist")
                return (DBStatus.s_data_issue, Algorithm(ERROR_ID))
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return (DBStatus.s_connection_error, Algorithm(ERROR_ID))
        logger.debug("Algorithm was found")
        return (DBStatus.s_ok, Algorithm.fromDict(alg_d))

    def getAuthorAlgByAlgID(self, author_id, alg_id) -> Tuple[DBStatus, Algorithm]:
        try:
            # check user
            st, author = self.getUserByID(author_id)
            if st == DBStatus.s_data_issue:
                logger.error("This user does not exist")
                return (DBStatus.s_data_issue, Algorithm(ERROR_ID))
            # get alg
            algs_collection = self.db["algs"]
            alg_d = algs_collection.find_one({"alg_id": alg_id, "author_id": author_id})
            if alg_d is None:
                logger.error("This algorithm does not exist")
                return (DBStatus.s_data_issue, Algorithm(ERROR_ID))
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return (DBStatus.s_connection_error, Algorithm(ERROR_ID))
        logger.debug("Algorithm was found")
        return (DBStatus.s_ok, Algorithm.fromDict(alg_d))

    def getAllAuthorAlgs(self, author_id) -> Tuple[DBStatus, List[Algorithm]]:
        try:
            # check user
            st, author = self.getUserByID(author_id)
            if st == DBStatus.s_data_issue:
                logger.error("This user does not exist")
                return (DBStatus.s_data_issue, [Algorithm(ERROR_ID)])
            # get algs
            algs_collection = self.db["algs"]
            algs = []
            for alg_id in author.algs_id:
                alg_d = algs_collection.find_one({"alg_id": alg_id, "author_id": author_id})
                algs.append(Algorithm.fromDict(alg_d))
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return (DBStatus.s_connection_error, [Algorithm(ERROR_ID)])
        logger.debug("Algorithms were found")
        return (DBStatus.s_ok, algs)

    def addTest(self, test) -> Tuple[DBStatus, Test]:
        try:
            # check alg
            st, alg = self.getAlgByTitle(test.alg_title)
            if st == DBStatus.s_data_issue:
                logger.error("This algorithm does not exist")
                return (DBStatus.s_data_issue, Test(ERROR_ID))
            # get user
            user = (self.getUserByID(alg.author_id))[1]
            # check title
            st, tests_check = self.getAllAlgTests(user.user_id, alg.alg_id)
            if st != DBStatus.s_ok:
                return (st, Test(ERROR_ID))
            for t in tests_check:
                if test.title == t.title:
                    logger.error("This test already exists")
                    return (DBStatus.s_data_issue, Test(ERROR_ID))
            # add test
            tests_collection = self.db["tests"]
            test.test_id = self._getNextID(str(user.user_id) + "u" + str(alg.alg_id) + "a")
            if test.test_id == DBStatus.s_data_issue:
                logger.error("This user/algorithm does not exist")
                return (DBStatus.s_data_issue, Test(ERROR_ID))
            tests_collection.insert_one(test.__dict__)
            # update alg's list of algs
            new_list_tests = alg.tests_id
            new_list_tests.append(test.test_id)
            algs_collection = self.db["algs"]
            algs_collection.update_one(
                {"title": alg.title},
                {"$set": {"tests_id": new_list_tests}})
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return (DBStatus.s_connection_error, Test(ERROR_ID))
        logger.debug("New test was successfully added")
        return (DBStatus.s_ok, test)

    def getTest(self, author_id, alg_id, test_id) -> Tuple[DBStatus, Test]:
        try:
            # check alg
            st, alg = self.getAuthorAlgByAlgID(author_id, alg_id)
            if st == DBStatus.s_data_issue:
                logger.error("This algorithm does not exist")
                return (DBStatus.s_data_issue, Test(ERROR_ID))
            # get test
            tests_collection = self.db["tests"]
            test_d = tests_collection.find_one({"test_id": test_id, "alg_title": alg.title})
            if test_d is None:
                logger.error("This test does not exist")
                return (DBStatus.s_data_issue, Test(ERROR_ID))
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return (DBStatus.s_connection_error, Test(ERROR_ID))
        logger.debug("Test was found")
        return (DBStatus.s_ok, Test.fromDict(test_d))

    def getAllAlgTests(self, author_id, alg_id) -> Tuple[DBStatus, List[Test]]:
        try:
            # check alg
            st, alg = self.getAuthorAlgByAlgID(author_id, alg_id)
            if st == DBStatus.s_data_issue:
                logger.error("This user/algorithm does not exist")
                return (DBStatus.s_data_issue, [Test(ERROR_ID)])
            # get tests
            tests_collection = self.db["tests"]
            tests = []
            for test_id in alg.tests_id:
                test_d = tests_collection.find_one({"test_id": test_id, "alg_title": alg.title})
                tests.append(Test.fromDict(test_d))
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return (DBStatus.s_connection_error, [Test(ERROR_ID)])
        logger.debug("Tests were found")
        return (DBStatus.s_ok, tests)

    def addTask(self, task) -> Tuple[DBStatus, Task]:
        try:
            # check alg
            st = (self.getAlgByTitle(task.alg_title))[0]
            if st == DBStatus.s_data_issue:
                logger.error("This algorithm does not exist")
                return (DBStatus.s_data_issue, Task(ERROR_ID, "error"))
            # add task
            tasks_collection = self.db["tasks"]
            task.task_id = self._getNextID("tasks")
            if task.task_id == DBStatus.s_data_issue:
                return (DBStatus.s_connection_error, Task(ERROR_ID, "error"))
            tasks_collection.insert_one(task.__dict__)
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return (DBStatus.s_connection_error, Task(ERROR_ID, "error"))
        logger.debug("New task was successfully added")
        return (DBStatus.s_ok, task)

    def getTask(self, task_id) -> Tuple[DBStatus, Task]:
        try:
            tasks_collection = self.db["tasks"]
            task_d = tasks_collection.find_one({"task_id": task_id})
            if task_d is None:
                logger.error("This task does not exist")
                return (DBStatus.s_data_issue, Task(ERROR_ID, "error"))
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return (DBStatus.s_connection_error, Task(ERROR_ID, "error"))
        logger.debug("Task was found")
        return (DBStatus.s_ok, Task.fromDict(task_d))

    def getAllTasks(self) -> Tuple[DBStatus, List[Task]]:
        try:
            tasks_collection = self.db["tasks"]
            tasks_tmp = list(tasks_collection.find({}))
            tasks = []
            for task_d in tasks_tmp:
                tasks.append(Task.fromDict(task_d))
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return (DBStatus.s_connection_error, [Task(ERROR_ID, "error")])
        logger.debug("Tasks were found")
        return (DBStatus.s_ok, tasks)

    def getStats(self) -> Tuple[DBStatus, Stats]:
        try:
            users = (self.getAllUsers())[1]
            num_of_users = len(users)
            num_of_algs = 0
            num_of_tests = 0
            for user in users:
                user_algs = (self.getAllAuthorAlgs(user.user_id))[1]
                num_of_algs += len(user_algs)
                for alg in user_algs:
                    alg_tests = (self.getAllAlgTests(user.user_id, alg.alg_id))[1]
                    num_of_tests += len(alg_tests)
            num_of_tasks = len((self.getAllTasks())[1])
        except Exception as e:
            logger.error(f"MongoDBWorker connection failed: {e}")
            return (DBStatus.s_connection_error, Stats(ERROR_ID, ERROR_ID, ERROR_ID, ERROR_ID))
        logger.debug("Stats were collected")
        return (DBStatus.s_ok, Stats(num_of_users, num_of_algs, num_of_tests, num_of_tasks))

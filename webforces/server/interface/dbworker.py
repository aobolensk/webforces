from typing import Tuple, List

import abc
from webforces.server.structs import DBStatus, User, Algorithm, Test, Task, Stats


class DBWorker(abc.ABC):
    @abc.abstractmethod
    def connect(self) -> int:
        pass

    @abc.abstractmethod
    def disconnect(self) -> int:
        pass

    @abc.abstractmethod
    def dropAll(self) -> None:
        pass

    @abc.abstractmethod
    def addUser(self, user) -> Tuple[DBStatus, User]:
        pass

    @abc.abstractmethod
    def updFNUser(self, user) -> DBStatus:
        pass

    @abc.abstractmethod
    def bindAlg(self, user) -> DBStatus:
        pass

    @abc.abstractmethod
    def getUserByID(self, id) -> Tuple[DBStatus, User]:
        pass

    @abc.abstractmethod
    def getUserByLogin(self, login) -> Tuple[DBStatus, User]:
        pass

    @abc.abstractmethod
    def getAllUsers(self) -> Tuple[DBStatus, List[User]]:
        pass

    @abc.abstractmethod
    def addAlg(self, alg) -> Tuple[DBStatus, Algorithm]:
        pass

    @abc.abstractmethod
    def updAlgCost(self, alg) -> DBStatus:
        pass

    @abc.abstractmethod
    def getAlgByTitle(self, title) -> Tuple[DBStatus, Algorithm]:
        pass

    @abc.abstractmethod
    def getAlgByID(self, alg_id) -> Tuple[DBStatus, Algorithm]:
        pass

    @abc.abstractmethod
    def getAllAuthorAlgs(self, author_id) -> Tuple[DBStatus, List[Algorithm]]:
        pass

    @abc.abstractmethod
    def getAllBoundAlgs(self, author_id) -> Tuple[DBStatus, List[Algorithm]]:
        pass

    @abc.abstractmethod
    def getAllAlgs(self) -> Tuple[DBStatus, List[Algorithm]]:
        pass

    @abc.abstractmethod
    def getAllAvailableAlgs(self, user_id) -> Tuple[DBStatus, List[Algorithm], List[bool]]:
        pass

    @abc.abstractmethod
    def addTest(self, test) -> Tuple[DBStatus, Test]:
        pass

    @abc.abstractmethod
    def getTest(self, alg_id, test_id) -> Tuple[DBStatus, Test]:
        pass

    @abc.abstractmethod
    def getAllAlgTests(self, alg_id) -> Tuple[DBStatus, List[Test]]:
        pass

    @abc.abstractmethod
    def addTask(self, task) -> Tuple[DBStatus, Task]:
        pass

    @abc.abstractmethod
    def getTask(self, task_id) -> Tuple[DBStatus, Task]:
        pass

    @abc.abstractmethod
    def getAllTasks(self) -> Tuple[DBStatus, List[Task]]:
        pass

    @abc.abstractmethod
    def getStats(self) -> Tuple[DBStatus, Stats]:
        pass

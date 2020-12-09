from typing import Tuple, List

import abc
from webforces.server.structs import User, Algorithm
from webforces.server.structs import DBStatus


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
    def getUserByID(self, id) -> Tuple[DBStatus, User]:
        pass

    @abc.abstractmethod
    def getUserByLogin(self, login) -> Tuple[DBStatus, User]:
        pass

    @abc.abstractmethod
    def addAlg(self, alg, user_id) -> Tuple[DBStatus, Algorithm]:
        pass

    @abc.abstractmethod
    def getAlgByTitle(self, title) -> Tuple[DBStatus, Algorithm]:
        pass

    @abc.abstractmethod
    def getAuthorAlgByAlgID(self, author_id, alg_id) -> Tuple[DBStatus, Algorithm]:
        pass

    @abc.abstractmethod
    def getAllAuthorAlgs(self, author_id) -> Tuple[DBStatus, List[Algorithm]]:
        pass

# TODO
    @abc.abstractmethod
    def bindAlg(self, alg, user_id) -> DBStatus:
        pass

    @abc.abstractmethod
    def getAlgByID(self, id) -> dict():
        pass

    @abc.abstractmethod
    def getTestByID(self, id) -> dict():
        pass

    @abc.abstractmethod
    def addTest(self, user_id, test_d):
        pass

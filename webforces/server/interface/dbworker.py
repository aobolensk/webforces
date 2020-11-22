import abc
from webforces.server.structs import User
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
    def addUser(self, user) -> (DBStatus, User):
        pass

    @abc.abstractmethod
    def getUserByID(self, id) -> (DBStatus, User):
        pass

    @abc.abstractmethod
    def getUserByLogin(self, login) -> (DBStatus, User):
        pass

# TODO
    @abc.abstractmethod
    def getAlgByTitle(self, title) -> dict():
        pass

    @abc.abstractmethod
    def getAlgByID(self, id) -> dict():
        pass

    @abc.abstractmethod
    def addAlg(self, alg_d):
        pass

    @abc.abstractmethod
    def bindAlgToUser(self, user_id, alg_id) -> int:
        pass

    @abc.abstractmethod
    def getTestByID(self, id) -> dict():
        pass

    @abc.abstractmethod
    def addTest(self, user_id, test_d):
        pass

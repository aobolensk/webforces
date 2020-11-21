import abc


class DBWorker(abc.ABC):
    @abc.abstractmethod
    def connect(self) -> int:
        pass

    @abc.abstractmethod
    def disconnect(self) -> int:
        pass

    @abc.abstractmethod
    def getUserByID(self, id) -> dict():
        pass

    @abc.abstractmethod
    def getUserByLogin(self, login) -> dict():
        pass

    @abc.abstractmethod
    def addUser(self, user_d):
        pass

    @abc.abstractmethod
    def getAlgByTitle(self, title) -> dict():
        pass

    @abc.abstractmethod
    def getAlgByID(self, id) -> dict():
        pass

    @abc.abstractmethod
    def addAlg(self, alg_d):
        pass

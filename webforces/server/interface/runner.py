import abc
from typing import Tuple


class Runner:
    @abc.abstractmethod
    def compile(self, task_id: int, alg_id: int) -> bool:
        pass

    @abc.abstractmethod
    def test(self, task_id: int, test_id: int) -> bool:
        pass

    @abc.abstractmethod
    def execute(self, task_id: int) -> bool:
        pass

    @abc.abstractmethod
    def check_status(self, task_id: int) -> Tuple[int, str]:
        pass

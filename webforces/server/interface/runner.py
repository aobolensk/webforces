import abc

from webforces.server.structs import RunnerStatus


class Runner:
    status = {}

    @abc.abstractmethod
    def compile(self, task_id: int, alg_id: int) -> bool:
        pass

    @abc.abstractmethod
    def test(self, task_id: int, test_id: int) -> bool:
        pass

    @abc.abstractmethod
    def execute(self, task_id: int, alg_id: int) -> bool:
        pass

    def check_status(self, task_id: int) -> RunnerStatus:
        if task_id not in self.status.keys():
            return RunnerStatus.s_unknown
        return self.status[task_id]

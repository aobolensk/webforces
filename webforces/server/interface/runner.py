import abc
from typing import TYPE_CHECKING, Optional, Tuple

if TYPE_CHECKING:
    from webforces.server.core import Core

from loguru import logger
from webforces.server.structs import DBStatus, RunnerStatus


class Runner:
    def __init__(self, core: 'Core') -> None:
        super().__init__()
        self.core = core

    @abc.abstractmethod
    def compile(self, task_id: int, alg_id: int) -> bool:
        pass

    @abc.abstractmethod
    def test(self, task_id: int, test_id: int) -> bool:
        pass

    def execute(self, task_id: int, alg_id: int) -> bool:
        logger.info(f"Started execution of task {task_id} for alg {alg_id}")
        _, task = self.core.db.getTask(task_id)

        task.status = RunnerStatus.s_compiling.value
        task.message = "[IN PROGRESS] compiling"
        _ = self.core.db.updTaskStatus(task)

        try:
            if not self.compile(task_id, alg_id):
                raise Exception("Compilation failed")
        except Exception as e:
            task.status = RunnerStatus.s_compiling.value
            task.message = f"[FAILED] Compilation failed ({e.__class__.__name__}) {e}"
            _ = self.core.db.updTaskStatus(task)
            return False

        task.status = RunnerStatus.s_running.value
        task.message = "[IN PROGRESS] running"
        _ = self.core.db.updTaskStatus(task)

        _, alg = self.core.db.getAlgByID(alg_id)
        failed_tests = []
        for test_id in alg.tests_id:
            try:
                print(f"Starting test: {test_id}")
                if not self.test(task_id, test_id):
                    failed_tests.append(test_id)
            except Exception:
                failed_tests.append(test_id)
        task.status = RunnerStatus.s_finished.value
        if failed_tests:
            task.message = f"[FAILED] Failed {len(failed_tests)}/{len(alg.tests_id)} tests: {failed_tests}"
        else:
            task.message = f"[PASSED] All {len(alg.tests_id)} tests have passed"
        _ = self.core.db.updTaskStatus(task)

        logger.info(f"Finished execution of task {task_id} for alg {alg_id}")
        return True

    def check_status(self, task_id: int) -> Optional[Tuple[int, str]]:
        status, task = self.core.db.getTask(task_id)
        if status != DBStatus.s_ok:
            return None
        return (task.status, task.message)

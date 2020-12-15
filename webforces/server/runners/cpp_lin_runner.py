from loguru import logger
from webforces.server.interface.runner import Runner
from webforces.server.structs import Language, RunnerStatus


class CppLinRunner(Runner):
    lang_id = Language.lang_cpp

    def compile(self, task_id: int, alg_id: int) -> bool:
        raise NotImplementedError

    def test(self, task_id: int, test_id: int) -> bool:
        raise NotImplementedError

    def execute(self, task_id: int, alg_id: int) -> bool:
        logger.info(f"Started execution of task {task_id} for alg {alg_id}")
        self.status[task_id] = RunnerStatus.s_scheduled
        logger.info(f"Finished execution of task {task_id} for alg {alg_id}")
        return True

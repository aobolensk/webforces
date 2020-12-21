import platform
import sys
import threading
from typing import List, Optional

from loguru import logger
from webforces.server.auth import Auth
from webforces.server.interface.dbworker import DBWorker
from webforces.server.interface.runner import Runner
from webforces.server.mongodbworker import MongoDBWorker
from webforces.server.runners.cpp_lin_runner import CppLinRunner
from webforces.server.runners.cpp_win_runner import CppWinRunner
from webforces.server.structs import DBStatus, Task


class Core:
    _instance = None
    auth: Auth = None
    _is_done: bool = False
    db: DBWorker = None
    runners: List[Runner] = []

    def __init__(self, validation=False) -> None:
        """Initialization of webforces core

        Parameters:
            validation (bool): Set to true if validation is running
        """
        if self._is_done:
            return
        self._setup_logging()
        logger.debug("Core init")
        self.auth = Auth()
        self.db = MongoDBWorker(validation)
        self._init_runners()
        self._is_done = True

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Core, cls).__new__(cls)
        return cls._instance

    def _setup_logging(self, level="DEBUG"):
        logger.remove()
        fmt = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: ^7}</level> | {name}.{function}:{line} - "
            "<level>{message}</level>")
        logger.add(sys.stderr, level=level, format=fmt)

    def _init_runners(self):
        if platform.system() == "Linux":
            self.runners.append(CppLinRunner())
        elif platform.system() == "Windows":
            self.runners.append(CppWinRunner())
        else:
            logger.warning("Unknown OS, no runners will be added")

    def schedule_task(self, alg_id: int) -> int:
        task = Task(0, alg_id, -1, '')
        status, task = self.db.addTask(task)
        if status != DBStatus.s_ok:
            logger.error(f"Could not schedule task for algorithm {alg_id}")
            return -1
        runner = self.get_runner(alg_id)
        thr = threading.Thread(target=runner.execute, args=(task.task_id, alg_id))
        thr.setDaemon(True)
        thr.start()
        return task.task_id

    def get_runner(self, alg_id: int) -> Optional[Runner]:
        status, alg = self.db.getAlgByID(alg_id)
        if status != DBStatus.s_ok:
            logger.error(f"Could not schedule task for algorithm {alg_id}")
            return None
        runner = [runner for runner in self.runners if runner.lang_id.value == int(alg.lang_id)]
        if not runner:
            logger.error(f"Could not find runner for language {alg.lang_id}")
            return None
        return runner[0]

from typing import Tuple

from webforces.server.interface.runner import Runner


class CppWinRunner(Runner):
    def compile(self, task_id: int, alg_id: int) -> bool:
        raise NotImplementedError

    def test(self, task_id: int, test_id: int) -> bool:
        raise NotImplementedError

    def execute(self, task_id: int) -> bool:
        raise NotImplementedError

    def check_status(self, task_id: int) -> Tuple[int, str]:
        raise NotImplementedError

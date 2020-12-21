from typing import TYPE_CHECKING

from webforces.server.interface.runner import Runner
from webforces.server.structs import Language

if TYPE_CHECKING:
    from webforces.server.core import Core


class CppLinRunner(Runner):
    lang_id = Language.lang_cpp

    def __init__(self, core: 'Core') -> None:
        super().__init__(core)

    def compile(self, task_id: int, alg_id: int) -> bool:
        raise NotImplementedError

    def test(self, task_id: int, test_id: int) -> bool:
        raise NotImplementedError

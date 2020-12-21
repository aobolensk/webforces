import os
import subprocess
import tempfile
from typing import TYPE_CHECKING

from loguru import logger

from webforces.server.interface.runner import Runner
from webforces.server.structs import Language
from webforces.utils import remove_empty_lines

if TYPE_CHECKING:
    from webforces.server.core import Core


class CppLinRunner(Runner):
    lang_id = Language.lang_cpp

    def __init__(self, core: 'Core') -> None:
        super().__init__(core)

    def compile(self, task_id: int, alg_id: int) -> bool:
        work_dir = os.path.join(tempfile.gettempdir(), "webforces", str(task_id))
        os.makedirs(work_dir)
        _, alg = self.core.db.getAlgByID(alg_id)
        with open(os.path.join(work_dir, 'main.cpp'), 'w') as f:
            print(alg.source, file=f)
        proc = subprocess.Popen([
                "g++", os.path.join(work_dir, 'main.cpp'),
                "-o", os.path.join(work_dir, 'main')
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        out, err = proc.communicate()
        out, err = out.decode("utf-8"), err.decode("utf-8")
        if proc.returncode != 0:
            raise Exception(err)
        return True

    def test(self, task_id: int, test_id: int) -> bool:
        work_dir = os.path.join(tempfile.gettempdir(), "webforces", str(task_id))
        _, task = self.core.db.getTask(task_id)
        _, test = self.core.db.getTest(task.alg_id, test_id)
        with open(os.path.join(work_dir, f'test_{test_id}.in'), 'w') as f:
            print(test.input, file=f)
        proc = subprocess.Popen([
                os.path.join(work_dir, "main"),
            ],
            stdin=open(os.path.join(work_dir, f'test_{test_id}.in')),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        out, err = proc.communicate()
        out, err = out.decode("utf-8"), err.decode("utf-8")
        if proc.returncode != 0:
            raise Exception(err)
        expected = remove_empty_lines(test.output)
        actual = remove_empty_lines(out)
        logger.debug(f"Actual:   `{actual}`")
        logger.debug(f"Expected: `{expected}`")
        if actual != expected:
            raise Exception("Output mismatch")
        return True

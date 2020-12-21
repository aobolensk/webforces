from dataclasses import dataclass, field
from typing import List
from enum import Enum, IntEnum


ERROR_ID = -100


class DBStatus(Enum):
    s_ok = 0
    s_connection_error = -1
    s_data_issue = -2


class RunnerStatus(IntEnum):
    s_unknown = 0
    s_scheduled = -1
    s_compiling = -2
    s_running = -3
    s_finished = -4


class Language(IntEnum):
    lang_unknown = 0
    lang_cpp = 1

    @classmethod
    def get_list(cls):
        return [
            (Language.lang_unknown.value, "Unknown"),
            (Language.lang_cpp.value, "C++"),
        ]


@dataclass
class User:
    user_id: int
    login: str = ''
    first_name: str = ''
    second_name: str = ''
    middle_name: str = ''
    algs_id: List[int] = field(default_factory=list)
    bound_ids: List[int] = field(default_factory=list)

    @classmethod
    def fromDict(cls, dict):
        return cls(
            dict["user_id"], dict["login"],
            dict["first_name"], dict["second_name"], dict["middle_name"],
            dict["algs_id"], dict["bound_ids"]
        )


@dataclass
class Algorithm:
    alg_id: int
    title: str = ''
    description: str = ''
    author_id: int = 0
    source: str = ''
    tests_id: List[int] = field(default_factory=list)
    lang_id: int = 0
    cost: int = 0

    @classmethod
    def fromDict(cls, dict):
        return cls(
            dict["alg_id"], dict["title"], dict["description"],
            dict["author_id"], dict["source"], dict["tests_id"],
            dict["lang_id"], dict["cost"]
        )


@dataclass
class Test:
    test_id: int
    alg_id: int
    title: str = ''
    input: str = ''
    output: str = ''

    @classmethod
    def fromDict(cls, dict):
        return cls(
            dict["test_id"], dict["alg_id"], dict["title"],
            dict["input"], dict["output"],
        )


Test.__test__ = False
# Added to suppress pytest collection warning:
# cannot collect test class 'Test' because it has a __init__ constructor


@dataclass
class Task:
    task_id: int
    alg_id: int
    status: int = 0
    message: str = ''

    @classmethod
    def fromDict(cls, dict):
        return cls(
            dict["task_id"], dict["alg_id"],
            dict["status"], dict["message"]
        )


@dataclass
class Stats:
    num_of_users: int
    num_of_algs: int
    num_of_tests: int
    num_of_tasks: int
    name: str = "webforces"

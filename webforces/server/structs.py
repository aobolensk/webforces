from dataclasses import dataclass, field
from typing import List
from enum import Enum


class DBStatus(Enum):
    s_ok = 0
    s_connection_error = -1
    s_data_issue = -2


@dataclass
class User:
    user_id: int
    login: str = ''
    first_name: str = ''
    second_name: str = ''
    middle_name: str = ''
    algs_id: List[int] = field(default_factory=list)

    @classmethod
    def fromDict(cls, dict):
        return cls(
            dict["user_id"], dict["login"],
            dict["first_name"], dict["second_name"], dict["middle_name"],
            dict["algs_id"]
        )


@dataclass
class Algorithm:
    alg_id: int
    title: str = ''
    author_id: int = 0
    source: str = ''
    tests_id: List[int] = field(default_factory=list)
    lang_id: int = 0


@dataclass
class Test:
    test_id: int
    title: str = ''
    source: str = ''


@dataclass
class Task:
    task_id: int
    alg_id: int
    status: int = 0
    message: str = ''

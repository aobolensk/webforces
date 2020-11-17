from dataclasses import dataclass, field
from typing import List


@dataclass
class User:
    user_id: int
    login: str = ''
    first_name: str = ''
    second_name: str = ''
    middle_name: str = ''
    algs_id: List[int] = field(default_factory=list)


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

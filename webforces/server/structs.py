from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
    login: str = ''
    first_name: str = ''
    second_name: str = ''
    middle_name: str = ''
    algs_id: list() = field(default_factory=list)


@dataclass
class Algorithm:
    title: str = ''
    author_id: 'typing.Any' = object()
    source: str = ''
    tests_id: list() = field(default_factory=list)
    lang_id: int = 0


@dataclass
class Test:
    title: str = ''
    source: str = ''


@dataclass
class Task:
    alg_id: 'typing.Any' = object()
    status: int = 0
    message: str = ''

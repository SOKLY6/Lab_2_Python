from dataclasses import dataclass
from typing import Iterable, Protocol, runtime_checkable


@dataclass
class Task:
    """Задача с id и описанием"""

    id: int
    payload: str


@runtime_checkable
class TaskSource(Protocol):
    """Протокол источника задач"""

    def get_tasks(self) -> Iterable[Task]: ...

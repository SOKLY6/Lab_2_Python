from typing import Iterable, Protocol, runtime_checkable
from datetime import datetime
from src.domain.descriptors import (CorrectTaskId,
                                    NotEmptyPayload,
                                    CorrectTaskStatus,
                                    CorrectTaskPriority)


class Task:
    id = CorrectTaskId()
    payload = NotEmptyPayload()
    priority = CorrectTaskPriority()
    status = CorrectTaskStatus()

    def __init__(self, id: int, payload: str, priority: int = 1, status: str = "new") -> None:
        self.id = id
        self.payload = payload
        self.priority = priority
        self.status = status
        self.__creation_time = datetime.now()

    @property
    def living_time(self) -> datetime:
        return datetime.now() - self.__creation_time
    
    @property
    def creation_time(self) -> datetime:
        return self.__creation_time


@runtime_checkable
class TaskSource(Protocol):
    """Протокол источника задач"""

    def get_tasks(self) -> Iterable[Task]: ...

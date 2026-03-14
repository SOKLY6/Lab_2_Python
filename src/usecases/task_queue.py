from asyncio import PriorityQueue
from typing import Iterable

from src.domain.descriptors import CorrectTaskPriority, CorrectTaskStatus
from src.domain.exceptions import IncorrectTaskPriority
from src.domain.task import Task


class TaskQueue:
    """Класс для работы с задачами"""

    priority = CorrectTaskPriority()
    status = CorrectTaskStatus()

    def __init__(self, priority_queue: PriorityQueue, max_priority: int = 5) -> None:
        self.queue = priority_queue

    def __len__(self) -> int:
        return self.queue.qsize()

    def __iter__(self) -> Iterable[Task]:
        for _ in range(len(self)):
            yield self.queue.get()

    def __bool__(self) -> bool:
        return True if len(self) > 0 else False
    
    def no_filter(self) -> Iterable[Task]:
        return iter(self)

    def filter_status(self, status: str) -> Iterable[Task]:
        self.status = status
        task: Task
        for task in iter(self):
            if task.status == status:
                yield task

    def filter_priority(self, max_priority: int) -> Iterable[Task]:
        if self.min_priority >= self.max_priority:
            raise IncorrectTaskPriority(
                "Минимальный приоритет должен быть "
                "меньше максимального возможного"
            )

        for priority in range(self.max_priority, self.min_priority - 1, -1):
            for task in self.priority_task_dict[priority].queue:
                yield task

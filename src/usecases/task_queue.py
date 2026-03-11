from queue import Queue
from typing import Iterable

from src.domain.descriptors import CorrectTaskPriority, CorrectTaskStatus
from src.domain.exceptions import IncorrectTaskPriority
from src.domain.task import Task


class TaskQueue:
    """Класс для работы с задачами"""

    max_priority = CorrectTaskPriority()
    min_priority = CorrectTaskPriority()
    status = CorrectTaskStatus()

    def __init__(self, max_priority: int = 5) -> None:
        self.max_priority = max_priority
        self.priority_task_dict: dict[int, Queue] = {
            priority: Queue() for priority in range(self.max_priority, 0, -1)
        }

    def __iter__(self) -> Iterable[Task]:
        for priority in range(self.max_priority, 0, -1):
            for task in self.priority_task_dict[priority].queue:
                yield task

    def __len__(self) -> int:
        return sum(q.qsize() for q in self.priority_task_dict.values())

    def __bool__(self) -> bool:
        return True if len(self) > 0 else False

    def __contains__(self, task_in: Task) -> bool:
        """Проверяет, есть ли задача в очереди"""
        for task_list_number in range(self.max_priority, 0, -1):
            task: Task
            for task in self.priority_task_dict[task_list_number].queue:
                if task_in.id == task.id:
                    return True
        return False

    def push(self, task: Task) -> None:
        if task.priority >= self.max_priority:
            raise IncorrectTaskPriority(
                "Приоритет задачи должен быть меньше максимально возможного"
            )

        self.priority_task_dict[task.priority].put(task)

    def pop(self) -> Task:
        for q in self.priority_task_dict.values():
            if not q.empty():
                return q.get()
        raise IndexError("Очередь пустая")

    def filter_status(self, status: str) -> Iterable[Task]:
        self.status = status
        for priority in range(self.max_priority, 0, -1):
            task: Task
            for task in self.priority_task_dict[priority].queue:
                if task.status == self.status:
                    yield task

    def filter_priority(self, min_priority: int) -> Iterable[Task]:
        self.min_priority = min_priority
        if self.min_priority >= self.max_priority:
            raise IncorrectTaskPriority(
                "Минимальный приоритет должен быть "
                "меньше максимального возможного"
            )

        for priority in range(self.max_priority, self.min_priority - 1, -1):
            for task in self.priority_task_dict[priority].queue:
                yield task

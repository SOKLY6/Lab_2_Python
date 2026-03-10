from src.domain.exceptions import (IncorrectTaskId,
                                   EmptyTaskPayload,
                                   IncorrectTaskPriority,
                                   IncorrectTaskStatus)


class CorrectTaskId:
    def __set_name__(self, owner, name) -> None:
        self.name = '_' + name

    def __get__(self, instance, owner) -> int:
        return instance.__dict__[self.name]
    
    def __set__(self, instance, value) -> None:
        if not isinstance(value, int):
            raise TypeError("Id должно быть целым числом")
        if value < 1:
            raise IncorrectTaskId("Id должен быть натуральным числом")
        instance.__dict__[self.name] = value


class NotEmptyPayload:
    def __set_name__(self, owner, name) -> None:
        self.name = '_' + name

    def __get__(self, instance, owner) -> str:
        return instance.__dict__[self.name]
    
    def __set__(self, instance, value) -> None:
        if not isinstance(value, str):
            raise TypeError("Описание задачи должно задаваться строкой")
        if value is None:
            raise EmptyTaskPayload("Описание задачи не может быть пустым")
        instance.__dict__[self.name] = value


class CorrectTaskPriority:
    def __set_name__(self, owner, name) -> None:
        self.name = '_' + name

    def __get__(self, instance, owner) -> int:
        return instance.__dict__[self.name]
    
    def __set__(self, instance, value) -> None:
        if not isinstance(value, int) and (1 <= value <= 5):
            raise IncorrectTaskPriority("Приоритет задачи должен задаваться натуральным числом от 1 до 5")
        instance.__dict__[self.name] = value


class CorrectTaskStatus:
    STATUSES = ["new", "processing", "complete"]

    def __set_name__(self, owner, name) -> None:
        self.name = '_' + name

    def __get__(self, instance, owner) -> str:
        return instance.__dict__[self.name]
    
    def __set__(self, instance, value) -> None:
        if not isinstance(value, str):
            raise TypeError("Статус задачи должен задаваться строкой")
        if value not in self.STATUSES:
            raise IncorrectTaskStatus("Несуществующий статус задачи")
        instance.__dict__[self.name] = value

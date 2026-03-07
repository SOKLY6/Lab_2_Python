from pathlib import Path

import pytest

from src.domain.task import Task, TaskSource
from src.repository.task_storage import TaskStorage
from src.repository.task_api import TaskAPI
from src.repository.task_file import FileSource
from src.repository.task_generator import TaskGenerator
from src.usecases.task_interact import TaskInteract


@pytest.fixture
def sample_tasks() -> list[Task]:
    """Возвращает список примеров задач"""
    return [
        Task(id="1", payload="Исправить баг с гусем, который съел дедлайн"),
        Task(id="2", payload="Написать тесты для гусиного дозора"),
        Task(id="3", payload="Добавить функционал кормления гусей в прод")
    ]


@pytest.fixture
def tasks_file_path() -> Path:
    """Возвращает путь к файлу с задачами"""
    return Path("source/tasks.jsonl")


@pytest.fixture
def tasks_from_file(tasks_file_path: Path) -> list[Task]:
    """Читает и возвращает задачи из файла"""
    file_source = FileSource(str(tasks_file_path))
    return list(file_source.get_tasks())


class TestTask:
    """Тесты для класса Task"""
    
    def test_task_creation(self) -> None:
        """Проверяет создание задачи"""
        task = Task("1", "Исправить баг с гусем, который съел дедлайн")
        assert task.id == "1"
        assert task.payload == "Исправить баг с гусем, который съел дедлайн"
        assert task == Task("1", "Исправить баг с гусем, который съел дедлайн")
        assert task != Task("2", "Написать тесты для гусиного дозора")


class TestTaskSource:
    """Тесты для протокола TaskSource"""
    
    def test_classes_implement_protocol(self) -> None:
        """Проверяет, что классы реализуют протокол"""
        assert issubclass(TaskGenerator, TaskSource)
        assert issubclass(FileSource, TaskSource)
        assert issubclass(TaskAPI, TaskSource)


class TestTaskGenerator:
    """Тесты для генератора задач"""
    
    def test_generator_returns_tasks(self) -> None:
        """Проверяет генерацию задач"""
        generator = TaskGenerator(3)
        tasks = list(generator.get_tasks())
        assert len(tasks) == 3
        assert all(isinstance(t, Task) for t in tasks)
        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[2].id == 3


class TestFileSource:
    """Тесты для файлового источника"""
    
    def test_file_source_reads_all_tasks(self, tasks_file_path: Path) -> None:
        """Проверяет чтение всех задач из файла"""
        file_source = FileSource(str(tasks_file_path))
        tasks = list(file_source.get_tasks())
        
        assert len(tasks) == 10
        assert tasks[0].id == 1
        assert tasks[0].payload == "Исправить баг с гусем, который съел дедлайн"
        assert tasks[3].id == 4
        assert tasks[3].payload == "Починить гуся, украл ноутбук у разработчика"

    def test_file_source_returns_correct_task_ids(self, tasks_file_path: Path) -> None:
        """Проверяет корректность ID задач"""
        file_source = FileSource(str(tasks_file_path))
        tasks = list(file_source.get_tasks())
        
        expected_ids = [i for i in range(1, 11)]
        actual_ids = [task.id for task in tasks]
        assert actual_ids == expected_ids

    def test_file_source_returns_correct_payloads(self, tasks_file_path: Path) -> None:
        """Проверяет корректность описаний задач"""
        file_source = FileSource(str(tasks_file_path))
        tasks = list(file_source.get_tasks())
        
        expected_payloads = [
            "Исправить баг с гусем, который съел дедлайн",
            "Написать тесты для гусиного дозора",
            "Добавить функционал кормления гусей в прод",
            "Починить гуся, украл ноутбук у разработчика",
            "Разблокировать вход в офис от стаи гусей",
            "Переписать говнокод, который написал гусь",
            "Освободить серверную от захвативших ее гусей",
            "Провести ревью кода, пока гусь не ущипнул",
            "Задеплоить фикс после гусиного переполоха",
            "Восстановить документацию, съеденную гусем"
        ]
        
        actual_payloads = [task.payload for task in tasks]
        assert actual_payloads == expected_payloads

    def test_file_source_file_not_found(self) -> None:
        """Проверяет обработку отсутствующего файла"""
        file_source = FileSource("несуществующий_файл.jsonl")
        with pytest.raises(FileNotFoundError):
            list(file_source.get_tasks())


class TestTaskAPI:
    """Тесты для API источника"""
    
    def test_api_returns_tasks(self) -> None:
        """Проверяет получение задач из API"""
        api = TaskAPI()
        tasks = list(api.get_tasks())
        assert len(tasks) == 3
        assert tasks[0].id == 100001
        assert tasks[0].payload == "Мяукнуть"


class TestTaskStorage:
    """Тесты для хранилища задач"""
    
    def test_storage_operations(self, sample_tasks: list[Task]) -> None:
        """Проверяет операции с хранилищем"""
        storage = TaskStorage()
        assert storage.get_list_tasks() == []
        
        storage.add_tasks(sample_tasks)
        assert len(storage.get_list_tasks()) == 3
        
        storage.add_tasks(sample_tasks[:2])
        assert len(storage.get_list_tasks()) == 5


class TestTaskInteract:
    """Тесты для интерактора задач"""
    
    def test_add_tasks_from_generator(self) -> None:
        """Проверяет добавление задач из генератора"""
        task_interactor = TaskInteract(TaskStorage())
        generator = TaskGenerator(3)
        count = task_interactor.add_tasks_from_source(generator)
        assert count == 3
        assert len(task_interactor.get_all_tasks()) == 3

    def test_add_tasks_from_file(self, tasks_file_path: Path) -> None:
        """Проверяет добавление задач из файла"""
        task_interactor = TaskInteract(TaskStorage())
        file_source = FileSource(str(tasks_file_path))
        count = task_interactor.add_tasks_from_source(file_source)
        assert count == 10
        assert len(task_interactor.get_all_tasks()) == 10

    def test_add_tasks_from_api(self) -> None:
        """Проверяет добавление задач из API"""
        task_interactor = TaskInteract(TaskStorage())
        api_source = TaskAPI()
        count = task_interactor.add_tasks_from_source(api_source)
        assert count == 3
        assert len(task_interactor.get_all_tasks()) == 3

    def test_add_tasks_multiple_sources(self, tasks_file_path: Path) -> None:
        """Проверяет добавление задач из нескольких источников"""
        task_interactor = TaskInteract(TaskStorage())
        task_interactor.add_tasks_from_source(TaskGenerator(2))
        task_interactor.add_tasks_from_source(FileSource(str(tasks_file_path)))
        task_interactor.add_tasks_from_source(TaskAPI())
        assert len(task_interactor.get_all_tasks()) == 15

    def test_invalid_source_raises_error(self) -> None:
        """Проверяет обработку невалидного источника"""
        class NotASource:
            pass
        task_interactor = TaskInteract(TaskStorage())
        with pytest.raises(TypeError):
            task_interactor.add_tasks_from_source(NotASource())


class TestIntegration:
    """Интеграционные тесты"""
    
    def test_full_flow(self, tasks_file_path: Path) -> None:
        """Проверяет полный цикл работы с задачами"""
        task_interactor = TaskInteract(TaskStorage())
        task_interactor.add_tasks_from_source(FileSource(str(tasks_file_path)))
        task_interactor.add_tasks_from_source(TaskGenerator(2))
        task_interactor.add_tasks_from_source(TaskAPI())
        
        tasks = task_interactor.get_all_tasks()
        assert len(tasks) == 15
        
        payloads = [task.payload for task in tasks]
        
        assert "Исправить баг с гусем, который съел дедлайн" in payloads
        assert "Освободить серверную от захвативших ее гусей" in payloads
        assert any(p in TaskGenerator.TEXTS for p in payloads)
        assert "Мяукнуть" in payloads
from dataclasses import dataclass
from typing import Any, Callable
from enum import Enum
import time


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    task_id: str
    func: Callable
    args: tuple = ()
    kwargs: dict = None
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: str = None
    created_at: float = None
    started_at: float = None
    completed_at: float = None

    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}

        if self.created_at is None:
            self.created_at = time.time()

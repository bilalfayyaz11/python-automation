import asyncio
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List

from task_model import Task, TaskStatus


@dataclass(order=True)
class PrioritizedTask:
    priority: int
    task: Any = field(compare=False)


class AsyncExecutionEngine:
    def __init__(self, max_workers: int = 5, use_priority: bool = False):
        self.max_workers = max_workers
        self.use_priority = use_priority
        self.task_queue = asyncio.PriorityQueue() if use_priority else asyncio.Queue()
        self.tasks: Dict[str, Task] = {}
        self.workers: List[asyncio.Task] = []
        self.running = False
        self.execution_order = []

    async def submit_task(self, task: Task, priority: int = 100) -> str:
        self.tasks[task.task_id] = task

        if self.use_priority:
            await self.task_queue.put(PrioritizedTask(priority, task))
        else:
            await self.task_queue.put(task)

        return task.task_id

    async def _worker(self, worker_id: int):
        print(f"Worker {worker_id} started")

        while self.running or not self.task_queue.empty():
            try:
                queue_item = await asyncio.wait_for(self.task_queue.get(), timeout=1)

                task = queue_item.task if self.use_priority else queue_item

                if task.status == TaskStatus.CANCELLED:
                    self.task_queue.task_done()
                    continue

                task.status = TaskStatus.RUNNING
                task.started_at = time.time()
                self.execution_order.append(task.task_id)

                print(f"Worker {worker_id} executing task {task.task_id}")

                try:
                    if asyncio.iscoroutinefunction(task.func):
                        task.result = await task.func(*task.args, **task.kwargs)
                    else:
                        task.result = task.func(*task.args, **task.kwargs)

                    task.status = TaskStatus.COMPLETED

                except Exception as exc:
                    task.status = TaskStatus.FAILED
                    task.error = str(exc)

                task.completed_at = time.time()
                self.task_queue.task_done()

            except asyncio.TimeoutError:
                continue
            except Exception as exc:
                print(f"Worker {worker_id} error: {exc}")

        print(f"Worker {worker_id} stopped")

    async def start(self):
        self.running = True

        self.workers = [
            asyncio.create_task(self._worker(worker_id))
            for worker_id in range(1, self.max_workers + 1)
        ]

    async def stop(self):
        self.running = False

        await self.task_queue.join()

        for worker in self.workers:
            worker.cancel()

        await asyncio.gather(*self.workers, return_exceptions=True)

    async def cancel_task(self, task_id: str) -> bool:
        task = self.tasks.get(task_id)

        if not task:
            return False

        if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
            return False

        task.status = TaskStatus.CANCELLED
        task.error = "Task cancelled before execution"
        task.completed_at = time.time()

        return True

    def get_task_status(self, task_id: str) -> Dict:
        task = self.tasks.get(task_id)

        if not task:
            return {"error": "Task not found"}

        return {
            "task_id": task.task_id,
            "status": task.status.value,
            "result": task.result,
            "error": task.error,
            "created_at": task.created_at,
            "started_at": task.started_at,
            "completed_at": task.completed_at,
        }

    def get_statistics(self) -> Dict:
        counts = {
            "pending": 0,
            "running": 0,
            "completed": 0,
            "failed": 0,
            "cancelled": 0,
        }

        durations = []

        for task in self.tasks.values():
            counts[task.status.value] += 1

            if task.started_at and task.completed_at:
                durations.append(task.completed_at - task.started_at)

        average_execution_time = sum(durations) / len(durations) if durations else 0

        return {
            "total_tasks": len(self.tasks),
            "queue_size": self.task_queue.qsize(),
            "max_workers": self.max_workers,
            "active_workers": len(self.workers),
            "status_counts": counts,
            "average_execution_time_seconds": round(average_execution_time, 3),
            "execution_order": self.execution_order,
        }

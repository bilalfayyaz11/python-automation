import asyncio
import uuid

from execution_engine import AsyncExecutionEngine
from task_model import Task
from sample_tasks import compute_intensive_task
from monitor import EngineMonitor


async def wait_until_complete(engine):
    while True:
        stats = engine.get_statistics()
        counts = stats["status_counts"]

        unfinished = counts["pending"] + counts["running"]

        if unfinished == 0:
            break

        await asyncio.sleep(1)


async def stress_test():
    engine = AsyncExecutionEngine(max_workers=5)
    monitor = EngineMonitor(engine)

    await engine.start()

    monitor_task = asyncio.create_task(
        monitor.display_stats(interval=2)
    )

    for index in range(20):
        task = Task(
            task_id=f"stress-{index + 1}",
            func=compute_intensive_task,
            args=((index % 3) + 1,)
        )

        await engine.submit_task(task)

    await wait_until_complete(engine)

    monitor.stop()
    await asyncio.sleep(1)
    monitor_task.cancel()

    print("\nFinal Stress Test Statistics")
    print("=" * 50)
    print(engine.get_statistics())

    await engine.stop()


async def priority_test():
    engine = AsyncExecutionEngine(
        max_workers=1,
        use_priority=True
    )

    await engine.start()

    tasks = [
        (30, Task("low-priority", compute_intensive_task, (1,))),
        (10, Task("high-priority", compute_intensive_task, (1,))),
        (20, Task("medium-priority", compute_intensive_task, (1,))),
    ]

    for priority, task in tasks:
        await engine.submit_task(task, priority=priority)
        print(f"Submitted {task.task_id} with priority {priority}")

    await wait_until_complete(engine)

    print("\nPriority Execution Order")
    print("=" * 50)
    print(engine.get_statistics()["execution_order"])

    await engine.stop()


if __name__ == "__main__":
    print("Select test:")
    print("1. Stress Test")
    print("2. Priority Test")

    choice = input("Enter choice (1-2): ")

    if choice == "1":
        asyncio.run(stress_test())

    elif choice == "2":
        asyncio.run(priority_test())

    else:
        print("Invalid choice")

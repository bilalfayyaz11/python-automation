import asyncio
import uuid

from execution_engine import AsyncExecutionEngine
from task_model import Task
from sample_tasks import compute_intensive_task, process_file


async def wait_until_complete(engine: AsyncExecutionEngine):
    while True:
        stats = engine.get_statistics()
        counts = stats["status_counts"]

        unfinished = counts["pending"] + counts["running"]

        if unfinished == 0:
            break

        await asyncio.sleep(1)


async def main():
    engine = AsyncExecutionEngine(max_workers=3)
    await engine.start()

    print("Async Execution Engine Started")
    print("-" * 50)

    tasks = [
        Task(str(uuid.uuid4()), compute_intensive_task, (2,)),
        Task(str(uuid.uuid4()), compute_intensive_task, (3,)),
        Task(str(uuid.uuid4()), compute_intensive_task, (1,)),
        Task(str(uuid.uuid4()), process_file, ("test_input.txt", "read")),
        Task(str(uuid.uuid4()), process_file, ("test_output.txt", "write")),
    ]

    for task in tasks:
        task_id = await engine.submit_task(task)
        print(f"Submitted task: {task_id}")

    await wait_until_complete(engine)

    print("\nTask Results")
    print("-" * 50)

    for task in tasks:
        print(engine.get_task_status(task.task_id))

    print("\nEngine Statistics")
    print("-" * 50)
    print(engine.get_statistics())

    await engine.stop()

    print("\nEngine stopped")


if __name__ == "__main__":
    asyncio.run(main())

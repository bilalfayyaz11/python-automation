import asyncio
import os


class EngineMonitor:
    def __init__(self, engine):
        self.engine = engine
        self.monitoring = False

    async def display_stats(self, interval: int = 2):
        self.monitoring = True

        while self.monitoring:
            os.system("clear")

            stats = self.engine.get_statistics()

            print("Async Execution Engine Monitor")
            print("=" * 50)
            print(f"Total Tasks: {stats['total_tasks']}")
            print(f"Queue Size: {stats['queue_size']}")
            print(f"Max Workers: {stats['max_workers']}")
            print(f"Active Workers: {stats['active_workers']}")
            print(f"Average Execution Time: {stats['average_execution_time_seconds']}s")
            print()
            print("Status Counts:")
            for status, count in stats["status_counts"].items():
                print(f"  {status}: {count}")

            await asyncio.sleep(interval)

    def stop(self):
        self.monitoring = False

#!/usr/bin/env python3
import time
from pprint import pprint

from job_manager import JobManager


def test_job_lifecycle():
    """Test complete job lifecycle."""
    manager = JobManager()

    job_id = manager.create_job("data_processing_job")
    print(f"Created job ID: {job_id}")

    initial_status = manager.get_job_status(job_id)
    print("Initial status:")
    pprint(initial_status)

    started = manager.start_job(job_id)
    print(f"Started successfully: {started}")

    time.sleep(2)

    completed = manager.complete_job(
        job_id,
        {
            "records_processed": 1500,
            "errors": 0,
            "execution_engine": "python",
        },
    )
    print(f"Completed successfully: {completed}")

    final_status = manager.get_job_status(job_id)
    print("Final status:")
    pprint(final_status)

    duration = manager.get_job_duration(job_id)
    print(f"Job duration: {duration:.2f} seconds")

    manager.close()


def test_failed_job():
    """Test job failure scenario."""
    manager = JobManager()

    job_id = manager.create_job("failing_job")
    print(f"Created failing job ID: {job_id}")

    started = manager.start_job(job_id)
    print(f"Started successfully: {started}")

    failed = manager.fail_job(job_id, "Simulated processing failure")
    print(f"Failed successfully: {failed}")

    failed_status = manager.get_job_status(job_id)
    print("Failed job status:")
    pprint(failed_status)

    manager.close()


def test_query_by_status():
    """Test querying jobs by status."""
    manager = JobManager()

    completed_jobs = manager.get_jobs_by_status("completed")
    print(f"Completed jobs count: {len(completed_jobs)}")
    pprint(completed_jobs)

    failed_jobs = manager.get_jobs_by_status("failed")
    print(f"Failed jobs count: {len(failed_jobs)}")
    pprint(failed_jobs)

    manager.close()


if __name__ == "__main__":
    print("Testing Job Lifecycle...")
    test_job_lifecycle()

    print("\nTesting Failed Job...")
    test_failed_job()

    print("\nTesting Query by Status...")
    test_query_by_status()

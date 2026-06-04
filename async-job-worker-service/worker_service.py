import requests
import time
import json
import subprocess
import os
import shutil
from datetime import datetime

API_BASE_URL = 'http://localhost:5000'
POLL_INTERVAL = 5


class JobWorker:

    def __init__(self, api_url):
        self.api_url = api_url
        self.running = True

    def fetch_pending_jobs(self):
        try:
            response = requests.get(
                f"{self.api_url}/jobs?status=pending",
                timeout=10
            )

            if response.status_code == 200:
                return response.json()

            return []

        except Exception as e:
            print(f"Fetch error: {e}")
            return []

    def update_job_status(self, job_id, status, result=None):
        try:
            payload = {
                "status": status,
                "result": result
            }

            response = requests.put(
                f"{self.api_url}/jobs/{job_id}/status",
                json=payload,
                timeout=10
            )

            if response.status_code in [200, 201]:
                print(f"Job {job_id} updated -> {status}")
            else:
                print(f"Status update failed for job {job_id}")

        except Exception as e:
            print(f"Status update error: {e}")

    def execute_backup_job(self, payload):

        data = json.loads(payload)

        source = data.get("path")
        destination = data.get("destination", "/tmp/backup")

        os.makedirs(destination, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if os.path.isfile(source):
            shutil.copy(source, destination)

            return {
                "success": True,
                "source": source,
                "destination": destination,
                "backup_type": "file_copy"
            }

        if os.path.isdir(source):
            archive_path = os.path.join(destination, f"backup_{timestamp}.tar.gz")

            tar_result = subprocess.run(
                ["tar", "-czf", archive_path, source],
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if not os.path.exists(archive_path):
                raise RuntimeError(tar_result.stderr)

            return {
                "success": True,
                "source": source,
                "destination": archive_path,
                "backup_type": "directory_archive"
            }

        return {
            "success": False,
            "message": f"{source} not found"
        }

    def execute_cleanup_job(self, payload):

        data = json.loads(payload)

        directory = data.get("directory", "/tmp")

        count = 0

        for root, dirs, files in os.walk(directory):
            count += len(files)

        return {
            "directory": directory,
            "files_found": count,
            "action": "simulated_cleanup"
        }

    def execute_report_job(self, payload):

        disk = subprocess.check_output(
            ["df", "-h"],
            text=True
        )

        memory = subprocess.check_output(
            ["free", "-m"],
            text=True
        )

        return {
            "disk_usage": disk,
            "memory_usage": memory
        }

    def process_job(self, job):

        job_id = job["id"]
        job_type = job["job_type"]
        payload = job["payload"]

        print(f"[{datetime.now()}] Processing job {job_id}")

        self.update_job_status(
            job_id,
            "processing"
        )

        try:

            if job_type == "backup":
                result = self.execute_backup_job(payload)

            elif job_type == "cleanup":
                result = self.execute_cleanup_job(payload)

            elif job_type == "report":
                result = self.execute_report_job(payload)

            else:
                raise Exception(
                    f"Unknown job type {job_type}"
                )

            self.update_job_status(
                job_id,
                "completed",
                json.dumps(result)
            )

            print(
                f"[{datetime.now()}] Job {job_id} completed"
            )

        except Exception as e:

            self.update_job_status(
                job_id,
                "failed",
                json.dumps(
                    {"error": str(e)}
                )
            )

            print(
                f"[{datetime.now()}] Job {job_id} failed"
            )

    def run(self):

        print(
            f"Worker started. Poll interval {POLL_INTERVAL}s"
        )

        while self.running:

            try:

                jobs = self.fetch_pending_jobs()

                if jobs:

                    print(
                        f"Found {len(jobs)} pending jobs"
                    )

                    for job in jobs:
                        self.process_job(job)

                else:
                    print(
                        f"[{datetime.now()}] No pending jobs"
                    )

                time.sleep(POLL_INTERVAL)

            except KeyboardInterrupt:

                print("Worker stopped")
                self.running = False

            except Exception as e:

                print(
                    f"Worker loop error: {e}"
                )

                time.sleep(POLL_INTERVAL)


if __name__ == "__main__":

    worker = JobWorker(API_BASE_URL)
    worker.run()

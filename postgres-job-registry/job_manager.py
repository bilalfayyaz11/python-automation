import json
from typing import Optional

import psycopg2
from psycopg2.extras import RealDictCursor


class JobManager:
    def __init__(
        self,
        host="localhost",
        database="job_registry",
        user="postgres",
        password="labpassword",
    ):
        """Initialize database connection."""
        self.connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
        )
        self.connection.autocommit = False
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def create_job(self, job_name: str) -> int:
        """Create a new job entry with pending status."""
        try:
            self.cursor.execute(
                """
                INSERT INTO jobs (job_name, status)
                VALUES (%s, 'pending')
                RETURNING job_id;
                """,
                (job_name,),
            )
            job_id = self.cursor.fetchone()["job_id"]
            self.connection.commit()
            return job_id
        except Exception:
            self.connection.rollback()
            raise

    def start_job(self, job_id: int) -> bool:
        """Mark job as running and set started_at timestamp."""
        try:
            self.cursor.execute(
                """
                UPDATE jobs
                SET status = 'running',
                    started_at = NOW()
                WHERE job_id = %s
                  AND status = 'pending';
                """,
                (job_id,),
            )
            updated = self.cursor.rowcount > 0
            self.connection.commit()
            return updated
        except Exception:
            self.connection.rollback()
            raise

    def complete_job(self, job_id: int, result_data: dict) -> bool:
        """Mark job as completed and store JSONB results."""
        try:
            self.cursor.execute(
                """
                UPDATE jobs
                SET status = 'completed',
                    completed_at = NOW(),
                    result_data = %s::jsonb
                WHERE job_id = %s
                  AND status = 'running';
                """,
                (json.dumps(result_data), job_id),
            )
            updated = self.cursor.rowcount > 0
            self.connection.commit()
            return updated
        except Exception:
            self.connection.rollback()
            raise

    def fail_job(self, job_id: int, error_message: str) -> bool:
        """Mark job as failed and store error message."""
        try:
            self.cursor.execute(
                """
                UPDATE jobs
                SET status = 'failed',
                    completed_at = NOW(),
                    error_message = %s
                WHERE job_id = %s
                  AND status = 'running';
                """,
                (error_message, job_id),
            )
            updated = self.cursor.rowcount > 0
            self.connection.commit()
            return updated
        except Exception:
            self.connection.rollback()
            raise

    def get_job_status(self, job_id: int) -> Optional[dict]:
        """Retrieve current job status and metadata."""
        self.cursor.execute(
            """
            SELECT job_id, job_name, status, created_at, started_at,
                   completed_at, result_data, error_message
            FROM jobs
            WHERE job_id = %s;
            """,
            (job_id,),
        )
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def get_jobs_by_status(self, status: str) -> list:
        """Retrieve all jobs with a specified status."""
        self.cursor.execute(
            """
            SELECT job_id, job_name, status, created_at, started_at,
                   completed_at, result_data, error_message
            FROM jobs
            WHERE status = %s
            ORDER BY job_id;
            """,
            (status,),
        )
        return [dict(row) for row in self.cursor.fetchall()]

    def get_job_duration(self, job_id: int) -> Optional[float]:
        """Calculate job execution duration in seconds."""
        self.cursor.execute(
            """
            SELECT EXTRACT(EPOCH FROM (completed_at - started_at)) AS duration
            FROM jobs
            WHERE job_id = %s
              AND started_at IS NOT NULL
              AND completed_at IS NOT NULL;
            """,
            (job_id,),
        )
        row = self.cursor.fetchone()

        if not row or row["duration"] is None:
            return None

        return float(row["duration"])

    def close(self):
        """Close database resources."""
        self.cursor.close()
        self.connection.close()

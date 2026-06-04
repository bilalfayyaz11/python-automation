from app import create_app
from app.models import db, JobHistory
from datetime import datetime, timedelta
import random


def populate_sample_data():
    """
    Create sample job history data for API testing.
    """

    app = create_app()

    with app.app_context():
        db.drop_all()
        db.create_all()

        job_names = ["backup-database", "deploy-app", "run-tests", "cleanup-logs"]
        statuses = ["success", "failed", "running"]
        environments = ["dev", "staging", "prod"]
        users = ["admin", "devops", "jenkins"]

        for _ in range(25):
            status = random.choice(statuses)
            start_time = datetime.now() - timedelta(
                days=random.randint(0, 7),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )

            end_time = None
            duration = None
            error_message = None

            if status in ["success", "failed"]:
                duration = random.randint(30, 1800)
                end_time = start_time + timedelta(seconds=duration)

            if status == "failed":
                error_message = random.choice([
                    "Connection timeout",
                    "Permission denied",
                    "Dependency unavailable",
                    "Configuration validation failed"
                ])

            job = JobHistory(
                job_name=random.choice(job_names),
                status=status,
                start_time=start_time,
                end_time=end_time,
                duration=duration,
                user=random.choice(users),
                environment=random.choice(environments),
                error_message=error_message
            )

            db.session.add(job)

        db.session.commit()

        print("Created 25 sample job history entries")


if __name__ == "__main__":
    populate_sample_data()

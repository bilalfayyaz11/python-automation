import pytest
from app import create_app
from app.models import db, JobHistory
from app.config import TestConfig
from datetime import datetime


@pytest.fixture
def app():
    """
    Create application for testing.
    """

    app = create_app(TestConfig)

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Create test client.
    """

    return app.test_client()


@pytest.fixture
def sample_jobs(app):
    """
    Create sample job data for tests.
    """

    with app.app_context():
        jobs = [
            JobHistory(
                job_name="backup-db",
                status="success",
                user="admin",
                environment="prod",
                start_time=datetime(2024, 1, 15, 10, 0),
                end_time=datetime(2024, 1, 15, 10, 5),
                duration=300
            ),
            JobHistory(
                job_name="deploy-app",
                status="failed",
                user="devops",
                environment="staging",
                start_time=datetime(2024, 1, 15, 11, 0),
                end_time=datetime(2024, 1, 15, 11, 2),
                duration=120,
                error_message="Connection timeout"
            ),
            JobHistory(
                job_name="run-tests",
                status="running",
                user="jenkins",
                environment="dev",
                start_time=datetime(2024, 1, 15, 12, 0)
            )
        ]

        db.session.add_all(jobs)
        db.session.commit()

        return jobs


def test_create_job(client):
    response = client.post("/jobs", json={
        "job_name": "security-scan",
        "status": "running",
        "user": "scanner",
        "environment": "prod"
    })

    data = response.get_json()

    assert response.status_code == 201
    assert data["job_name"] == "security-scan"
    assert data["status"] == "running"
    assert data["user"] == "scanner"
    assert data["environment"] == "prod"
    assert "id" in data


def test_create_job_missing_required_field(client):
    response = client.post("/jobs", json={
        "status": "running",
        "user": "scanner"
    })

    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Missing required fields"
    assert "job_name" in data["missing_fields"]


def test_get_all_jobs(client, sample_jobs):
    response = client.get("/jobs")
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 3


def test_get_job_by_id(client, sample_jobs):
    response = client.get("/jobs/1")
    data = response.get_json()

    assert response.status_code == 200
    assert data["job_name"] == "backup-db"
    assert data["status"] == "success"
    assert data["environment"] == "prod"


def test_get_nonexistent_job(client):
    response = client.get("/jobs/999")

    assert response.status_code == 404


def test_update_job(client, sample_jobs):
    response = client.put("/jobs/3", json={
        "status": "success",
        "end_time": "2024-01-15T12:10:00"
    })

    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "success"
    assert data["end_time"] == "2024-01-15T12:10:00"
    assert data["duration"] == 600


def test_filter_by_status(client, sample_jobs):
    response = client.get("/jobs?status=success")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1
    assert all(job["status"] == "success" for job in data)


def test_filter_by_environment(client, sample_jobs):
    response = client.get("/jobs?environment=prod")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1
    assert all(job["environment"] == "prod" for job in data)


def test_filter_by_user(client, sample_jobs):
    response = client.get("/jobs?user=admin")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1
    assert all(job["user"] == "admin" for job in data)


def test_filter_by_job_name(client, sample_jobs):
    response = client.get("/jobs?job_name=backup-db")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1
    assert all(job["job_name"] == "backup-db" for job in data)


def test_multiple_filters(client, sample_jobs):
    response = client.get("/jobs?status=success&environment=prod")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["status"] == "success"
    assert data[0]["environment"] == "prod"


def test_get_statistics(client, sample_jobs):
    response = client.get("/jobs/stats")
    data = response.get_json()

    assert response.status_code == 200
    assert data["total_jobs"] == 3
    assert data["status_counts"]["success"] == 1
    assert data["status_counts"]["failed"] == 1
    assert data["status_counts"]["running"] == 1
    assert data["environment_counts"]["prod"] == 1
    assert data["environment_counts"]["staging"] == 1
    assert data["environment_counts"]["dev"] == 1

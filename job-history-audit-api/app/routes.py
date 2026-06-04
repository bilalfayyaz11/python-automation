from flask import Blueprint, request, jsonify
from app.models import db, JobHistory
from sqlalchemy import func
from datetime import datetime

api = Blueprint("api", __name__)


@api.route("/jobs", methods=["POST"])
def create_job():
    """
    Create a new job history entry.
    """

    data = request.get_json(silent=True) or {}

    required_fields = ["job_name", "status"]
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing_fields
        }), 400

    job = JobHistory(
        job_name=data["job_name"],
        status=data["status"],
        user=data.get("user"),
        environment=data.get("environment"),
        error_message=data.get("error_message"),
    )

    if data.get("start_time"):
        job.start_time = datetime.fromisoformat(data["start_time"])

    if data.get("end_time"):
        job.end_time = datetime.fromisoformat(data["end_time"])
        job.duration = int((job.end_time - job.start_time).total_seconds())

    db.session.add(job)
    db.session.commit()

    return jsonify(job.to_dict()), 201


@api.route("/jobs", methods=["GET"])
def get_jobs():
    """
    Get job history with optional filters.
    """

    query = JobHistory.query

    status = request.args.get("status")
    job_name = request.args.get("job_name")
    environment = request.args.get("environment")
    user = request.args.get("user")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if status:
        query = query.filter(JobHistory.status == status)

    if job_name:
        query = query.filter(JobHistory.job_name == job_name)

    if environment:
        query = query.filter(JobHistory.environment == environment)

    if user:
        query = query.filter(JobHistory.user == user)

    if start_date:
        query = query.filter(JobHistory.start_time >= datetime.fromisoformat(start_date))

    if end_date:
        query = query.filter(JobHistory.start_time <= datetime.fromisoformat(end_date))

    jobs = query.order_by(JobHistory.start_time.desc()).all()

    return jsonify([job.to_dict() for job in jobs]), 200


@api.route("/jobs/<int:job_id>", methods=["GET"])
def get_job(job_id):
    """
    Get a specific job by ID.
    """

    job = JobHistory.query.get_or_404(job_id)

    return jsonify(job.to_dict()), 200


@api.route("/jobs/<int:job_id>", methods=["PUT"])
def update_job(job_id):
    """
    Update job status and end time.
    """

    job = JobHistory.query.get_or_404(job_id)
    data = request.get_json(silent=True) or {}

    if "status" in data:
        job.status = data["status"]

    if "end_time" in data:
        job.end_time = datetime.fromisoformat(data["end_time"])
        job.duration = int((job.end_time - job.start_time).total_seconds())

    if "error_message" in data:
        job.error_message = data["error_message"]

    db.session.commit()

    return jsonify(job.to_dict()), 200


@api.route("/jobs/stats", methods=["GET"])
def get_stats():
    """
    Get job execution statistics.
    """

    status_counts = (
        db.session.query(JobHistory.status, func.count(JobHistory.id))
        .group_by(JobHistory.status)
        .all()
    )

    environment_counts = (
        db.session.query(JobHistory.environment, func.count(JobHistory.id))
        .group_by(JobHistory.environment)
        .all()
    )

    return jsonify({
        "status_counts": {status: count for status, count in status_counts},
        "environment_counts": {environment: count for environment, count in environment_counts},
        "total_jobs": JobHistory.query.count()
    }), 200

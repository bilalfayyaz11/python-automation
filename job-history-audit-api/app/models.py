from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()


class JobHistory(db.Model):
    """
    Model for storing job execution history.
    """

    __tablename__ = "job_history"

    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    user = db.Column(db.String(50))
    environment = db.Column(db.String(20))
    error_message = db.Column(db.Text)

    def to_dict(self):
        """
        Convert model instance to dictionary.
        """
        return {
            "id": self.id,
            "job_name": self.job_name,
            "status": self.status,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.duration,
            "user": self.user,
            "environment": self.environment,
            "error_message": self.error_message,
        }

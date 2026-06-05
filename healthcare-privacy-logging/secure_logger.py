import logging
from pythonjsonlogger import jsonlogger
from log_sanitizer import HealthcareLogSanitizer


class SecureHealthcareLogger:
    """
    Production logger with automatic PII sanitization.
    """

    def __init__(self, log_file: str = "secure_app.log"):
        self.sanitizer = HealthcareLogSanitizer()

        self.logger = logging.getLogger("secure_healthcare_logger")
        self.logger.setLevel(logging.INFO)
        self.logger.handlers = []

        file_handler = logging.FileHandler(log_file)
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s %(event_type)s %(patient_data)s"
        )

        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log_patient_event(self, event_type: str, patient_data: dict, message: str):
        """
        Log patient-related event with automatic sanitization.
        """
        sanitized_data = self.sanitizer.sanitize_record(patient_data)

        self.logger.info(
            message,
            extra={
                "event_type": event_type,
                "patient_data": sanitized_data
            }
        )


if __name__ == "__main__":
    logger = SecureHealthcareLogger()

    patient = {
        "patient_id": "12345678",
        "name": "John Doe",
        "ssn": "123-45-6789",
        "email": "john.doe@example.com",
        "phone": "555-123-4567",
        "ip_address": "192.168.1.10"
    }

    logger.log_patient_event("admission", patient, "Patient admitted to ER")
    logger.log_patient_event("diagnosis", patient, "Diagnosed with pneumonia")
    logger.log_patient_event("discharge", patient, "Patient discharged")

    print("Logged 3 events to secure_app.log")

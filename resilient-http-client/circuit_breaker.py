from datetime import datetime, timedelta
from enum import Enum


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    """Circuit breaker implementation to prevent cascading failures."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        success_threshold: int = 2,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        if self.state == CircuitState.OPEN:
            if self._recovery_timeout_passed():
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
                print("Circuit transitioned to HALF_OPEN")
            else:
                raise RuntimeError("Circuit is OPEN. Request rejected.")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception:
            self._on_failure()
            raise

    def _recovery_timeout_passed(self) -> bool:
        """Return True if the circuit can attempt recovery."""
        if self.last_failure_time is None:
            return True

        return datetime.now() - self.last_failure_time >= timedelta(
            seconds=self.recovery_timeout
        )

    def _on_success(self) -> None:
        """Handle successful call."""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1

            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
                print("Circuit transitioned to CLOSED")
        else:
            self.failure_count = 0

    def _on_failure(self) -> None:
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            self.success_count = 0
            print("Circuit transitioned back to OPEN")
            return

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            print("Circuit transitioned to OPEN")

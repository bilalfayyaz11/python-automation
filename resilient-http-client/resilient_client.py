import time
from typing import Any, Dict, Optional

import requests
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

from circuit_breaker import CircuitBreaker


class ResilientHTTPClient:
    """HTTP client with retry logic, exponential backoff, timeouts, and optional circuit breaker protection."""

    RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}

    def __init__(
        self,
        max_retries: int = 3,
        base_timeout: int = 5,
        backoff_factor: float = 2.0,
        use_circuit_breaker: bool = False,
    ):
        self.max_retries = max_retries
        self.base_timeout = base_timeout
        self.backoff_factor = backoff_factor
        self.session = requests.Session()
        self.circuit_breaker = CircuitBreaker() if use_circuit_breaker else None

    def _calculate_backoff(self, attempt: int) -> float:
        """Calculate exponential backoff delay."""
        base_delay = 1
        return base_delay * (self.backoff_factor ** attempt)

    def _is_retryable_response(self, response: requests.Response) -> bool:
        """Return True when an HTTP response status should be retried."""
        return response.status_code in self.RETRYABLE_STATUS_CODES

    def _should_retry(self, exception: Exception, attempt: int) -> bool:
        """Determine if a failed request should be retried."""
        if attempt >= self.max_retries:
            return False

        if isinstance(exception, (Timeout, ConnectionError)):
            return True

        if isinstance(exception, HTTPError) and exception.response is not None:
            return self._is_retryable_response(exception.response)

        return False

    def _request_with_retry(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        """Execute an HTTP request with retry and backoff handling."""
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    timeout=self.base_timeout,
                    **kwargs,
                )

                if self._is_retryable_response(response):
                    raise HTTPError(
                        f"Retryable HTTP status received: {response.status_code}",
                        response=response,
                    )

                response.raise_for_status()
                return response

            except RequestException as exc:
                last_exception = exc

                if not self._should_retry(exc, attempt):
                    print(f"Request failed permanently after attempt {attempt + 1}: {exc}")
                    raise

                delay = self._calculate_backoff(attempt)
                print(
                    f"Attempt {attempt + 1} failed: {exc}. "
                    f"Retrying in {delay:.1f} seconds..."
                )
                time.sleep(delay)

        raise last_exception

    def _get_with_retry(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """Internal GET request with retry logic."""
        return self._request_with_retry(
            method="GET",
            url=url,
            params=params,
            headers=headers,
        )

    def _post_with_retry(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """Internal POST request with retry logic."""
        return self._request_with_retry(
            method="POST",
            url=url,
            data=data,
            json=json,
            headers=headers,
        )

    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """Perform a GET request with optional circuit breaker protection."""
        if self.circuit_breaker:
            return self.circuit_breaker.call(self._get_with_retry, url, params, headers)

        return self._get_with_retry(url, params, headers)

    def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """Perform a POST request with optional circuit breaker protection."""
        if self.circuit_breaker:
            return self.circuit_breaker.call(
                self._post_with_retry,
                url,
                data,
                json,
                headers,
            )

        return self._post_with_retry(url, data, json, headers)

    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close()

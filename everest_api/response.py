"""
Everest API Response

Wraps HTTP response data from API requests and provides
convenient methods for accessing response data, headers, and status.
"""

import json
from typing import Optional, Dict, List, Any


class EverestApiResponse:
    """
    Wraps an HTTP response from the Everest API.

    Provides convenient methods for accessing response data, headers,
    status codes, and error information.
    """

    def __init__(self, response_body: str, status_code: int, headers: Dict[str, str]):
        """
        Create a new API response instance.

        Args:
            response_body: Raw HTTP response body as string
            status_code: HTTP status code (e.g., 200, 404, 500)
            headers: Response headers as dictionary
        """
        self._raw_body = response_body
        self._status_code = status_code
        self._headers = headers
        self._data = None

        # Try to parse JSON response
        try:
            self._data = json.loads(response_body) if response_body else None
        except (json.JSONDecodeError, ValueError):
            self._data = None

    def get_data(self) -> Optional[Any]:
        """
        Get parsed JSON response data.

        Returns:
            Decoded JSON data (dict, list, etc.) or None if decoding failed
        """
        return self._data

    def get_raw_body(self) -> str:
        """
        Get raw response body string.

        Returns:
            Raw HTTP response body
        """
        return self._raw_body

    def get_status_code(self) -> int:
        """
        Get HTTP status code.

        Returns:
            HTTP status code (e.g., 200, 404, 500)
        """
        return self._status_code

    def get_headers(self) -> Dict[str, str]:
        """
        Get all response headers.

        Returns:
            Dictionary of all response headers
        """
        return self._headers

    def get_header(self, name: str) -> Optional[str]:
        """
        Get specific response header by name (case-insensitive).

        Args:
            name: Header name to retrieve

        Returns:
            Header value or None if not found
        """
        name_lower = name.lower()
        for key, value in self._headers.items():
            if key.lower() == name_lower:
                return value
        return None

    def is_success(self) -> bool:
        """
        Check if the request was successful (2xx status code).

        Returns:
            True if status code is between 200-299
        """
        return 200 <= self._status_code < 300

    def is_error(self) -> bool:
        """
        Check if the request failed (non-2xx status code).

        Returns:
            True if status code is not in 200-299 range
        """
        return not self.is_success()

    def has_error(self) -> bool:
        """
        Check if response contains an error.

        Checks both HTTP status code and presence of error field in response data.

        Returns:
            True if error exists in response or status indicates failure
        """
        if self.is_error():
            return True

        if isinstance(self._data, dict):
            return 'error' in self._data

        return False

    def get_error_message(self) -> Optional[str]:
        """
        Get error message from response.

        Attempts to extract error message from response data.
        Checks 'error' and 'message' fields in response object.

        Returns:
            Error message or None if no error found
        """
        if not isinstance(self._data, dict):
            return None

        # Check for 'error' field
        if 'error' in self._data:
            error = self._data['error']
            if isinstance(error, str):
                return error
            else:
                return json.dumps(error)

        # Check for 'message' field
        if 'message' in self._data:
            return self._data['message']

        return None

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert response to dictionary format.

        Returns:
            Dictionary containing data, status_code, and headers
        """
        return {
            'data': self._data,
            'status_code': self._status_code,
            'headers': self._headers,
        }

    def __repr__(self) -> str:
        """String representation of the response."""
        return f"<EverestApiResponse status={self._status_code} success={self.is_success()}>"

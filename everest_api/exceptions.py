"""
Everest API Exception

Exception thrown when API requests fail due to connection errors,
HTTP failures, or other technical issues (not API-level errors).
"""


class EverestApiException(Exception):
    """
    Exception raised for errors during API communication.

    This exception is raised when there are connection issues,
    HTTP errors, or other technical problems communicating with the API.
    It does not cover API-level errors returned in successful responses.
    """
    pass

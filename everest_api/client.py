"""
Everest API Client

Simple HTTP client for interacting with the Everest Logistics API.
Handles authentication, requests, and provides easy access to all API endpoints.
"""

import json
from typing import Dict, Any, Optional
import requests

from .response import EverestApiResponse
from .exceptions import EverestApiException


class EverestApi:
    """
    Everest API Client

    Simple HTTP client for interacting with the Everest Logistics API.
    Handles authentication, requests, and provides easy access to all API endpoints.
    """

    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        debug: bool = False
    ):
        """
        Create a new Everest API client instance.

        Args:
            base_url: API base URL (e.g., https://platform.everst.io/api)
            client_id: OAuth client ID for authentication
            client_secret: OAuth client secret for authentication
            debug: Enable debug mode to output request/response details
        """
        self._base_url = base_url.rstrip('/')
        self._client_id = client_id
        self._client_secret = client_secret
        self._debug = debug
        self._token: Optional[str] = None
        self._verify_ssl = True

    def set_verify_ssl(self, verify: bool) -> 'EverestApi':
        """
        Enable or disable SSL certificate verification.

        Args:
            verify: Whether to verify SSL certificates

        Returns:
            Self for method chaining
        """
        self._verify_ssl = verify
        return self

    def auth(self) -> EverestApiResponse:
        """
        Authenticate with the API and store the access token.

        Uses client credentials to obtain a bearer token that will be
        automatically included in subsequent requests.

        Returns:
            Response containing authentication result and token
        """
        response = self.post('auth', {
            'client_id': self._client_id,
            'client_secret': self._client_secret,
        })

        if response.is_success():
            data = response.get_data()
            if isinstance(data, dict) and 'token' in data:
                self._token = data['token']

        return response

    def get_token(self) -> Optional[str]:
        """
        Get the current authentication token.

        Returns:
            Current bearer token or None if not authenticated
        """
        return self._token

    def set_token(self, token: str) -> 'EverestApi':
        """
        Manually set the authentication token.

        Useful when reusing a previously obtained token without re-authenticating.

        Args:
            token: Bearer token to use for authentication

        Returns:
            Self for method chaining
        """
        self._token = token
        return self

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> EverestApiResponse:
        """
        Send a GET request to the API.

        Args:
            endpoint: API endpoint path (e.g., /missions/get)
            params: Query parameters or request body

        Returns:
            Response object containing status and data
        """
        return self._request('GET', endpoint, params or {})

    def post(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> EverestApiResponse:
        """
        Send a POST request to the API.

        Args:
            endpoint: API endpoint path (e.g., /missions/create)
            params: Request parameters to send in the body

        Returns:
            Response object containing status and data
        """
        return self._request('POST', endpoint, params or {})

    def put(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> EverestApiResponse:
        """
        Send a PUT request to the API.

        Args:
            endpoint: API endpoint path (e.g., /missions/update)
            params: Request parameters to send in the body

        Returns:
            Response object containing status and data
        """
        return self._request('PUT', endpoint, params or {})

    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> EverestApiResponse:
        """
        Send a DELETE request to the API.

        Args:
            endpoint: API endpoint path (e.g., /missions/delete)
            params: Request parameters to send in the body

        Returns:
            Response object containing status and data
        """
        return self._request('DELETE', endpoint, params or {})

    def _request(self, method: str, endpoint: str, params: Dict[str, Any]) -> EverestApiResponse:
        """
        Execute an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            params: Request parameters

        Returns:
            Response object

        Raises:
            EverestApiException: If request fails
        """
        endpoint = endpoint.lstrip('/')
        url = f"{self._base_url}/{endpoint}"

        # Prepare request body
        request_body = json.dumps(params) if params else ''

        # Prepare headers
        headers = {
            'Content-Type': 'text/plain; charset=UTF-8',
            'Content-Length': str(len(request_body.encode('utf-8'))),
        }

        if self._token:
            headers['Authorization'] = f'Bearer {self._token}'

        # Debug output
        if self._debug:
            self._debug_output('Request', {
                'Method': method,
                'URL': url,
                'Headers': headers,
                'Body': params,
            })

        try:
            # Make the request
            response = requests.request(
                method=method,
                url=url,
                data=request_body,
                headers=headers,
                verify=self._verify_ssl,
                timeout=30
            )

            # Extract response data
            response_body = response.text
            status_code = response.status_code
            response_headers = dict(response.headers)

            # Create response object
            api_response = EverestApiResponse(response_body, status_code, response_headers)

            # Debug output
            if self._debug:
                self._debug_output('Response', {
                    'Status Code': status_code,
                    'Headers': response_headers,
                    'Body': api_response.get_data(),
                })

            return api_response

        except requests.exceptions.RequestException as e:
            raise EverestApiException(f'Request error: {str(e)}') from e

    def _debug_output(self, title: str, data: Dict[str, Any]) -> None:
        """
        Output debug information to console.

        Args:
            title: Section title (Request/Response)
            data: Data to display
        """
        print('\n' + '=' * 60)
        print(title.upper())
        print('=' * 60)

        for key, value in data.items():
            print(f'\n{key}:')
            if isinstance(value, (dict, list)):
                print(json.dumps(value, indent=2, ensure_ascii=False))
            else:
                print(value)

        print('=' * 60 + '\n')

"""
Tests for EverestApiResponse class
"""

import pytest
from everest_api import EverestApiResponse


def test_response_success():
    """Test successful response parsing"""
    response_body = '{"success": true, "data": "test"}'
    response = EverestApiResponse(response_body, 200, {'content-type': 'application/json'})

    assert response.is_success() is True
    assert response.is_error() is False
    assert response.get_status_code() == 200
    assert response.get_data()['success'] is True
    assert response.get_data()['data'] == 'test'


def test_response_error():
    """Test error response handling"""
    response_body = '{"error": "Something went wrong"}'
    response = EverestApiResponse(response_body, 400, {'content-type': 'application/json'})

    assert response.is_success() is False
    assert response.is_error() is True
    assert response.has_error() is True
    assert response.get_error_message() == 'Something went wrong'


def test_response_headers():
    """Test header access"""
    headers = {
        'content-type': 'application/json',
        'x-custom-header': 'test-value'
    }
    response = EverestApiResponse('{}', 200, headers)

    assert response.get_header('content-type') == 'application/json'
    assert response.get_header('Content-Type') == 'application/json'  # Case insensitive
    assert response.get_header('x-custom-header') == 'test-value'
    assert response.get_header('non-existent') is None


def test_response_invalid_json():
    """Test handling of invalid JSON"""
    response = EverestApiResponse('invalid json', 200, {})

    assert response.get_data() is None
    assert response.get_raw_body() == 'invalid json'


def test_response_to_dict():
    """Test conversion to dictionary"""
    response_body = '{"test": "data"}'
    response = EverestApiResponse(response_body, 200, {'content-type': 'application/json'})

    result = response.to_dict()
    assert 'data' in result
    assert 'status_code' in result
    assert 'headers' in result
    assert result['status_code'] == 200

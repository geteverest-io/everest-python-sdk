#!/usr/bin/env python
"""
Simple test script to verify package installation and basic functionality.
Run this after installing the package to ensure everything works correctly.
"""

import sys


def test_imports():
    """Test that all package components can be imported."""
    print("Testing imports...")
    try:
        from everest_api import EverestApi, EverestApiResponse, EverestApiException
        print("  [OK] All imports successful")
        return True
    except ImportError as e:
        print(f"  [ERROR] Import failed: {e}")
        return False


def test_client_instantiation():
    """Test that the client can be instantiated."""
    print("\nTesting client instantiation...")
    try:
        from everest_api import EverestApi

        api = EverestApi(
            base_url='https://example.everst.io/api',
            client_id='test-client-id',
            client_secret='test-client-secret'
        )

        assert api._base_url == 'https://example.everst.io/api'
        assert api._client_id == 'test-client-id'
        assert api._client_secret == 'test-client-secret'
        assert api._debug is False
        assert api._verify_ssl is True

        print("  [OK] Client instantiation successful")
        return True
    except Exception as e:
        print(f"  [ERROR] Client instantiation failed: {e}")
        return False


def test_response_handling():
    """Test response parsing and methods."""
    print("\nTesting response handling...")
    try:
        from everest_api import EverestApiResponse

        # Test successful response
        response = EverestApiResponse(
            '{"success": true, "data": "test"}',
            200,
            {'content-type': 'application/json'}
        )

        assert response.is_success() is True
        assert response.is_error() is False
        assert response.get_status_code() == 200
        assert response.get_data()['success'] is True

        # Test error response
        error_response = EverestApiResponse(
            '{"error": "Test error"}',
            400,
            {}
        )

        assert error_response.is_success() is False
        assert error_response.has_error() is True
        assert error_response.get_error_message() == 'Test error'

        print("  [OK] Response handling successful")
        return True
    except Exception as e:
        print(f"  [ERROR] Response handling failed: {e}")
        return False


def test_exception():
    """Test exception handling."""
    print("\nTesting exception...")
    try:
        from everest_api import EverestApiException

        try:
            raise EverestApiException("Test exception")
        except EverestApiException as e:
            assert str(e) == "Test exception"

        print("  [OK] Exception handling successful")
        return True
    except Exception as e:
        print(f"  [ERROR] Exception handling failed: {e}")
        return False


def test_version():
    """Test version information."""
    print("\nTesting version info...")
    try:
        import everest_api
        version = getattr(everest_api, '__version__', 'Unknown')
        print(f"  [OK] Package version: {version}")
        return True
    except Exception as e:
        print(f"  [ERROR] Version check failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Everest API Client - Installation Test")
    print("=" * 60)

    tests = [
        test_imports,
        test_client_instantiation,
        test_response_handling,
        test_exception,
        test_version,
    ]

    results = [test() for test in tests]

    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)

    if all(results):
        print("\n[SUCCESS] All tests passed! Package is working correctly.")
        return 0
    else:
        print("\n[FAILURE] Some tests failed. Please check the errors above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())

# Everest API Client

[![PyPI version](https://badge.fury.io/py/everest-api-client.svg)](https://badge.fury.io/py/everest-api-client)
[![Python Support](https://img.shields.io/pypi/pyversions/everest-api-client.svg)](https://pypi.org/project/everest-api-client/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/everest/everest-python-sdk/workflows/Tests/badge.svg)](https://github.com/everest/everest-python-sdk/actions)

Simple Python client for the Everest TMS API.

🌐 **Website**: https://geteverest.io
📖 **Documentation**: [Full API Docs](README.md) | [Quick Start](QUICKSTART.md)
🐛 **Issues**: [GitHub Issues](https://github.com/everest/everest-python-sdk/issues)

## Installation

```bash
pip install everest-api-client
```

Or install from source:

```bash
git clone https://github.com/everest/everest-python-sdk.git
cd everest-python-sdk
pip install -e .
```

## Requirements

- Python >= 3.7
- requests >= 2.25.0

## Usage

### Basic Setup

```python
from everest_api import EverestApi, EverestApiException

api = EverestApi(
    base_url='https://your-platform.everst.io/api',
    client_id='your-client-id',
    client_secret='your-client-secret'
)

# Disable SSL verification for development (not recommended for production)
api.set_verify_ssl(False)
```

### Authentication

```python
# Authenticate and store token automatically
response = api.auth()

if response.is_success():
    print(f"Authenticated! Token: {api.get_token()}")
else:
    print(f"Authentication failed: {response.get_error_message()}")

# Or manually set a token
api.set_token('your-existing-token')
```

### Making API Calls

The client supports all HTTP methods through simple methods:

```python
# POST request
response = api.post('/missions/create', {
    'start_date': int(time.time()) + 3600,
    'service_id': 2,
    'client_ref': '12456XX',
    'address_start': '18 Boulevard des Batignolles, 75017 Paris',
    'address_end': '55 Rue du Faubourg Saint-Honoré, 75008 Paris',
    'packages': [
        {
            'name': 'Package name',
            'weight': 0.5,
            'quantity': 1,
        }
    ]
})

# GET request
response = api.post('/missions', {
    'limit_start': 0,
    'limit_end': 50,
})

# PUT request
response = api.post('/missions/update', {
    'ref': 'MISSION-REF',
    'address_end_comment': 'Updated comment'
})

# DELETE request
response = api.post('/missions/delete', {
    'ref': 'MISSION-REF'
})
```

### Working with Responses

```python
response = api.post('/missions/create', params)

# Check if request was successful
if response.is_success():
    # Get parsed JSON data
    data = response.get_data()
    print(f"Mission created: {data['mission']['ref']}")

# Check for errors
if response.has_error():
    print(f"Error: {response.get_error_message()}")

# Get HTTP status code
print(f"Status: {response.get_status_code()}")

# Get response headers
headers = response.get_headers()
content_type = response.get_header('content-type')

# Get raw response body
raw_body = response.get_raw_body()
```

### Debug Mode

Enable debug mode to see detailed request/response information:

```python
api = EverestApi(
    base_url='https://your-platform.everst.io/api',
    client_id='your-client-id',
    client_secret='your-client-secret',
    debug=True  # Enable debug mode
)
```

## Complete Example

```python
import time
from everest_api import EverestApi, EverestApiException

api = EverestApi(
    base_url='https://sinerlogic.everst.io/api',
    client_id='your-client-id',
    client_secret='your-client-secret'
)

# Authenticate
auth_response = api.auth()

if not auth_response.is_success():
    raise Exception(f'Authentication failed: {auth_response.get_error_message()}')

# Check if address is handled
address_check = api.post('/is-handled-address', {
    'address': '42 fake street, 75001 Paris',
    'start_date': int(time.time()) + 3600,
    'service_id': 61
})

if address_check.get_data()['success']:
    print("Address is handled!")

    # Create a mission
    mission = api.post('/missions/create', {
        'start_date': int(time.time()) + 3600,
        'service_id': 2,
        'client_ref': f'ORDER-{int(time.time())}',
        'address_start': '18 Boulevard des Batignolles, 75017 Paris',
        'address_end': '42 fake street, 75001 Paris',
        'address_end_name': 'John Doe',
        'address_end_tel': '0666666666',
        'packages': [
            {
                'name': 'Package',
                'weight': 0.5,
                'quantity': 1,
            }
        ]
    })

    if mission.is_success():
        mission_ref = mission.get_data()['mission']['ref']
        print(f"Mission created: {mission_ref}")

        # Get mission details
        details = api.post('/missions/get', {
            'ref': mission_ref
        })

        print(details.get_data())
```

## API Methods

### EverestApi

- `__init__(base_url: str, client_id: str, client_secret: str, debug: bool = False)` - Create a new client instance
- `auth() -> EverestApiResponse` - Authenticate and store token
- `set_token(token: str) -> EverestApi` - Manually set authentication token
- `get_token() -> Optional[str]` - Get current authentication token
- `set_verify_ssl(verify: bool) -> EverestApi` - Enable/disable SSL verification
- `get(endpoint: str, params: dict = None) -> EverestApiResponse` - Send GET request
- `post(endpoint: str, params: dict = None) -> EverestApiResponse` - Send POST request
- `put(endpoint: str, params: dict = None) -> EverestApiResponse` - Send PUT request
- `delete(endpoint: str, params: dict = None) -> EverestApiResponse` - Send DELETE request

### EverestApiResponse

- `get_data() -> Any` - Get parsed JSON response
- `get_raw_body() -> str` - Get raw response body
- `get_status_code() -> int` - Get HTTP status code
- `get_headers() -> dict` - Get all response headers
- `get_header(name: str) -> Optional[str]` - Get specific header
- `is_success() -> bool` - Check if status code is 2xx
- `is_error() -> bool` - Check if status code is not 2xx
- `has_error() -> bool` - Check if response contains error
- `get_error_message() -> Optional[str]` - Get error message if available
- `to_dict() -> dict` - Convert response to dictionary

## Error Handling

```python
try:
    response = api.post('/missions/create', params)

    if response.has_error():
        # Handle API errors
        print(f"API Error: {response.get_error_message()}")
except EverestApiException as e:
    # Handle connection/request errors
    print(f"Connection Error: {str(e)}")
```

## Type Hints

This library includes full type hints for better IDE support and type checking with tools like mypy.

## License

MIT

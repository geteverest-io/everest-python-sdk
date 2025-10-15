# Quick Start Guide

Get started with the Everest API Python Client in minutes!

## Installation

```bash
pip install everest-api-client
```

## Basic Usage

### 1. Initialize the Client

```python
from everest_api import EverestApi

api = EverestApi(
    base_url='https://your-platform.everst.io/api',
    client_id='your-client-id',
    client_secret='your-client-secret'
)
```

### 2. Authenticate

```python
response = api.auth()

if response.is_success():
    print(f"✓ Authenticated! Token: {api.get_token()[:20]}...")
else:
    print(f"✗ Authentication failed: {response.get_error_message()}")
```

### 3. Create a Mission

```python
import time

mission = api.post('/missions/create', {
    'start_date': int(time.time()) + 3600,  # 1 hour from now
    'service_id': 2,
    'client_ref': 'ORDER-12345',
    'address_start': '18 Boulevard des Batignolles, 75017 Paris',
    'address_end': '55 Rue du Faubourg Saint-Honoré, 75008 Paris',
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
    print(f"✓ Mission created: {mission_ref}")
else:
    print(f"✗ Failed: {mission.get_error_message()}")
```

### 4. Get Mission Details

```python
details = api.post('/missions/get', {
    'ref': mission_ref
})

if details.is_success():
    mission_data = details.get_data()['mission']
    print(f"Status: {mission_data['status']}")
    print(f"From: {mission_data['address_start']}")
    print(f"To: {mission_data['address_end']}")
```

### 5. List Missions

```python
missions = api.post('/missions', {
    'limit_start': 0,
    'limit_end': 10,
})

if missions.is_success():
    for mission in missions.get_data()['missions']:
        print(f"- {mission['ref']}: {mission['status']}")
```

## Common Operations

### Check if Address is Handled

```python
check = api.post('/is-handled-address', {
    'address': '42 rue Example, 75001 Paris',
    'start_date': int(time.time()) + 3600,
    'service_id': 2
})

if check.is_success() and check.get_data()['success']:
    print("✓ Address is handled!")
    if 'price' in check.get_data():
        print(f"Price: {check.get_data()['price']['total_ttc']} EUR")
else:
    print("✗ Address not handled")
```

### Update a Mission

```python
update = api.post('/missions/update', {
    'ref': mission_ref,
    'address_end_comment': 'Ring doorbell twice'
})

if update.is_success():
    print("✓ Mission updated!")
```

### Cancel a Mission

```python
cancel = api.post('/missions/cancel', {
    'ref': mission_ref
})

if cancel.is_success():
    print("✓ Mission canceled!")
```

## Error Handling

```python
from everest_api import EverestApiException

try:
    response = api.post('/missions/create', params)

    if response.has_error():
        print(f"API Error: {response.get_error_message()}")

except EverestApiException as e:
    print(f"Connection Error: {str(e)}")
```

## Token Management

```python
# Save token for reuse
token = api.get_token()
# Store in cache/database...

# Later, reuse the token
api.set_token(token)
# No need to call api.auth() again!
```

## Debug Mode

```python
# Enable debug mode to see all requests/responses
api = EverestApi(
    base_url='https://your-platform.everst.io/api',
    client_id='your-client-id',
    client_secret='your-client-secret',
    debug=True  # <-- Enable debug mode
)
```

## Next Steps

- Read the [Full Documentation](README.md)
- Check out the [Complete Example](example.py)
- Learn about [Webhooks](example_webhook_endpoint.py)
- Explore the [API Reference](https://docs.everst.io)

## Need Help?

- 📖 [Documentation](README.md)
- 🐛 [Report Issues](https://github.com/everest/everest-python-sdk/issues)
- 💬 [Contact Support](mailto:contact@everst.io)

Happy coding! 🚀

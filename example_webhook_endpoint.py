"""
Example Webhook Endpoint for Everest API
Event: mission_status

This is a Flask-based example. You can adapt it to your preferred framework
(Django, FastAPI, etc.)

To run this example:
    pip install flask
    python example_webhook_endpoint.py
"""

from flask import Flask, request, jsonify
from datetime import datetime
import pytz
import json
import os

app = Flask(__name__)

# Enable logging
ENABLE_LOGGING = True
LOG_FILE = 'webhook-logs.log'


@app.route('/webhook', methods=['POST'])
def webhook_handler():
    """
    Handle incoming webhooks from Everest API.
    """
    # Only accept POST requests
    if request.method != 'POST':
        return jsonify({'error': 'Method not allowed'}), 405

    # Get webhook data
    data = request.get_json() or request.form.to_dict()

    # Log webhook data
    if ENABLE_LOGGING:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] Webhook received:\n{json.dumps(data, indent=2, ensure_ascii=False)}\n\n"

        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)

    # ======================================================================
    # YOUR BUSINESS LOGIC HERE
    # ======================================================================

    # Required fields
    event = data.get('event')
    ref = data.get('ref')
    mission_type = data.get('type')
    start_date = data.get('start_date')
    status = data.get('status')
    client_id = data.get('client_id')
    service_id = data.get('service_id')
    date = data.get('date')
    agent_id = data.get('agent_id')
    agent_name = data.get('agent_name')

    # Optional fields
    start_date_max = data.get('start_date_max')
    status_slug = data.get('status_slug')
    client_ref = data.get('client_ref')
    medias = data.get('medias', [])
    lat = data.get('lat')
    lon = data.get('lon')
    extras = data.get('extras')
    extras_fields = data.get('extras_fields', [])

    # Parse dates (timestamps in Europe/Paris timezone)
    paris_tz = pytz.timezone('Europe/Paris')

    if start_date:
        start_datetime = datetime.fromtimestamp(int(start_date), tz=paris_tz)
        start_date_formatted = start_datetime.strftime('%Y-%m-%d %H:%M:%S')
        # Example: "2025-10-15 14:30:00"

    if start_date_max:
        start_date_max_datetime = datetime.fromtimestamp(int(start_date_max), tz=paris_tz)
        start_date_max_formatted = start_date_max_datetime.strftime('%Y-%m-%d %H:%M:%S')

    if date:
        date_datetime = datetime.fromtimestamp(int(date), tz=paris_tz)
        date_formatted = date_datetime.strftime('%Y-%m-%d %H:%M:%S')

    # Example: Process based on status
    if status == 'completed':
        # Handle completed missions
        print(f"Mission {ref} completed by {agent_name} on {date_formatted}")
        # send_email(client_id, f"Mission {ref} completed by {agent_name} on {date_formatted}")

    # Example: Process medias if present
    if medias and isinstance(medias, list):
        for media in medias:
            # Process each media
            print(f"Media URL: {media}")
            # download_media(media)

    # Example: Process GPS coordinates if present
    if lat and lon:
        print(f"Location: {lat}, {lon}")
        # save_location(ref, lat, lon)

    # Example: Process extras fields if present
    if extras_fields and isinstance(extras_fields, list):
        for field in extras_fields:
            # Process each extra field
            print(f"Extra field: {field}")

    # Return success response
    return jsonify({
        'success': True,
        'message': 'Webhook processed successfully'
    }), 200


@app.route('/webhook/test', methods=['GET'])
def webhook_test():
    """
    Test endpoint to verify the webhook server is running.
    """
    return jsonify({
        'status': 'ok',
        'message': 'Webhook endpoint is ready'
    }), 200


if __name__ == '__main__':
    print("Starting webhook server on http://localhost:5000")
    print("Webhook endpoint: http://localhost:5000/webhook")
    print("Test endpoint: http://localhost:5000/webhook/test")
    app.run(debug=True, host='0.0.0.0', port=5000)

"""
Everest API - Complete Example

This example demonstrates all major features of the Everest API Python client.
"""

import time
from everest_api import EverestApi, EverestApiException


def main():
    # Configuration
    api = EverestApi(
        base_url='https://<your-domain>/api',  # https://example.everst.io/api
        client_id='<your-client-id>',
        client_secret='<your-client-secret>',
        debug=True  # Enable debug mode
    )

    # Disable SSL verification for development
    api.set_verify_ssl(False)

    try:
        print("=== EVEREST API COMPLETE TEST ===\n")

        # ------------------------------------------------------------------
        # AUTHENTICATION
        # ------------------------------------------------------------------
        print("1. Testing authentication...")
        # The token (api.get_token()) can be cached and set via api.set_token()
        # You don't need to call api.auth() every time
        auth_response = api.auth()

        if not auth_response.is_success():
            print(f'Authentication failed: {auth_response.get_error_message()}')
            return

        print("Authenticated successfully!")
        print(f"Token: {api.get_token()[:20]}...\n")

        # ------------------------------------------------------------------
        # GET SERVICES LIST
        # ------------------------------------------------------------------
        print("2. Getting services list...")
        services = api.post('/services')

        if services.is_success():
            services_data = services.get_data()
            services_list = services_data.get('services', []) if isinstance(services_data, dict) else []
            print(f"Found {len(services_list)} services")
            if services_list:
                first_service = services_list[0]
                print(f"Example: Service #{first_service['id']} - {first_service['name']}")
        else:
            print(f"Failed to get services: {services.get_error_message()}")
        print()

        # ------------------------------------------------------------------
        # IS HANDLED ADDRESS
        # ------------------------------------------------------------------
        print("3. Checking if address is handled...")
        address_check = api.post('/is-handled-address', {
            'address': '18 Boulevard des Batignolles, 75017 Paris',
            'start_date': int(time.time()) + 3600,
            'service_id': 2
        })

        if address_check.is_success():
            check_data = address_check.get_data()
            is_handled = check_data.get('success', False) if isinstance(check_data, dict) else False
            if is_handled:
                print("Address is handled!")
                price = check_data.get('price')
                if price:
                    print(f"Price: {price.get('total_ttc')} EUR")
            else:
                print("Address is not handled")
        else:
            print(f"Failed to check address: {address_check.get_error_message()}")
        print()

        # ------------------------------------------------------------------
        # MISSION CREATE
        # ------------------------------------------------------------------
        print("4. Creating a new mission...")
        mission_create = api.post('/missions/create', {
            'start_date': int(time.time()) + 7200,  # 2 hours from now
            'service_id': 2,
            'client_ref': f'TEST-{int(time.time())}',
            'comment': 'API wrapper test mission',
            'address_start': '18 Boulevard des Batignolles, 75017 Paris',
            'address_start_name': 'Sender Name',
            'address_start_email': 'sender@test.com',
            'address_start_tel': '0123456789',
            'address_end': '55 Rue du Faubourg Saint-Honoré, 75008 Paris',
            'address_end_name': 'John Doe',
            'address_end_tel': '0666666666',
            'address_end_email': 'johndoe@email.tld',
            'address_end_comment': 'Code 2850 apt 108',
            'packages': [
                {
                    'name': 'Test Package',
                    'weight': 0.5,
                    'length': 34,
                    'width': 26,
                    'depth': 3.25,
                    'ref': f'PKG-{int(time.time())}',
                    'quantity': 1,
                },
            ],
            'custom_infos': [
                {
                    'name': 'Test Info',
                    'value': f'Test Value {int(time.time())}',
                },
            ],
        })

        mission_ref = None

        if mission_create.is_success():
            create_data = mission_create.get_data()
            if isinstance(create_data, dict) and 'mission' in create_data:
                mission_ref = create_data['mission'].get('ref')
                print("Mission created successfully!")
                print(f"Reference: {mission_ref}")

                mission = create_data['mission']
                if 'price' in mission:
                    print(f"Price: {mission['price'].get('total_ttc')} EUR")
        else:
            print(f"Failed to create mission: {mission_create.get_error_message()}")
        print()

        # ------------------------------------------------------------------
        # MISSION GET
        # ------------------------------------------------------------------
        if mission_ref:
            print("5. Getting mission details...")
            mission_get = api.post('/missions/get', {
                'ref': mission_ref,
            })

            if mission_get.is_success():
                print("Mission details retrieved!")
                get_data = mission_get.get_data()
                if isinstance(get_data, dict) and 'mission' in get_data:
                    mission = get_data['mission']
                    print(f"Status: {mission.get('status')}")
                    print(f"From: {mission.get('address_start')}")
                    print(f"To: {mission.get('address_end')}")

                    packages = mission.get('packages', [])
                    if packages:
                        print(f"Packages: {len(packages)}")
            else:
                print(f"Failed to get mission: {mission_get.get_error_message()}")
            print()

            # ------------------------------------------------------------------
            # MISSION UPDATE
            # ------------------------------------------------------------------
            print("6. Updating mission...")
            import datetime
            mission_update = api.post('/missions/update', {
                'ref': mission_ref,
                'address_end_comment': f'Updated comment via API wrapper test - {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            })

            if mission_update.is_success():
                print("Mission updated successfully!")
            else:
                print(f"Failed to update mission: {mission_update.get_error_message()}")
            print()

            # ------------------------------------------------------------------
            # MISSION CANCEL (if not already dispatched)
            # ------------------------------------------------------------------
            print("7. Canceling mission...")
            mission_cancel = api.post('/missions/cancel', {
                'ref': mission_ref,
            })

            if mission_cancel.is_success():
                print("Mission canceled successfully!")
            else:
                print(f"Failed to cancel mission: {mission_cancel.get_error_message()}")
            print()

        # ------------------------------------------------------------------
        # LIST RECENT MISSIONS
        # ------------------------------------------------------------------
        print("8. Listing recent missions...")
        missions_list = api.post('/missions', {
            'limit_start': 0,
            'limit_end': 50,
        })

        if missions_list.is_success():
            list_data = missions_list.get_data()
            missions = list_data.get('missions', []) if isinstance(list_data, dict) else []
            print(f"Retrieved {len(missions)} recent missions")

            for idx, mission in enumerate(missions[:3], 1):
                print(f"{idx}. {mission.get('ref')} - Status: {mission.get('status')}")
        else:
            print(f"Failed to list missions: {missions_list.get_error_message()}")
        print()

        # ------------------------------------------------------------------
        # GET ACCOUNT INFO
        # ------------------------------------------------------------------
        print("9. Getting account information...")
        account_info = api.post('/me')

        if account_info.is_success():
            print("Account info retrieved!")
            account = account_info.get_data()

            if isinstance(account, dict):
                if 'platform' in account:
                    print(f"Platform: {account['platform'].get('name')}")
                if 'client' in account:
                    print(f"Client: {account['client'].get('name')}")
        else:
            print(f"Failed to get account info: {account_info.get_error_message()}")
        print()

        print("=== ALL TESTS COMPLETED ===")

    except EverestApiException as e:
        print(f"\nException occurred: {str(e)}")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())

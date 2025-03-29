import requests
import json
import os

def test_safety_check_endpoint():
    """Test the /safetyCheck endpoint directly using requests"""
    print("Testing /safetyCheck endpoint...")

    # URL for the endpoint (adjust if needed)
    url = "http://127.0.0.1:5001/ai-hackathon-202503/us-central1/api/safetyCheck"

    try:
        # Make the request
        print(f"Making GET request to: {url}")
        response = requests.get(url)

        # Print status code
        print(f"Status code: {response.status_code}")

        # Print response headers
        print("Response headers:")
        for header, value in response.headers.items():
            print(f"  {header}: {value}")

        # Print response content
        print("\nResponse content:")
        print(response.text)

        # Try to parse JSON
        try:
            json_data = response.json()
            print("\nParsed JSON data:")
            print(json.dumps(json_data, indent=2))

            # Check if user_data is empty
            if 'user_data' in json_data and len(json_data['user_data']) == 0:
                print("\nWARNING: user_data array is empty!")

                # Check mock file directly
                mock_path = 'mocks/safety_response_log.json'
                if os.path.exists(mock_path):
                    with open(mock_path, 'r') as f:
                        mock_data = json.load(f)
                        print(f"\nMock file contains {len(mock_data)} records")

                        # Filter out USR01235
                        filtered_data = [
                            record for record in mock_data
                            if record.get('user_id') != 'USR01235'
                        ]
                        print(f"After filtering USR01235: {len(filtered_data)} records should remain")
                else:
                    print(f"\nMock file not found at: {mock_path}")
                    print(f"Current working directory: {os.getcwd()}")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")

    except requests.exceptions.ConnectionError:
        print(f"Connection error: Could not connect to {url}")
        print("Make sure the Firebase emulator is running")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    test_safety_check_endpoint()

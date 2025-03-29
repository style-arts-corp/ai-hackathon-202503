import main
import json

def test_safety_check():
    print("Testing safety_check function...")

    # Call the safety_check function
    response = main.safety_check()

    # Convert the Flask response to a string
    response_data = response.get_data(as_text=True)

    # Print the response
    print("Response:")
    print(response_data)

    # Try to parse the JSON response
    try:
        json_data = json.loads(response_data)
        print("\nParsed JSON data:")
        print(f"Number of records: {len(json_data.get('user_data', []))}")
        print(f"Full data: {json.dumps(json_data, indent=2)}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")

if __name__ == "__main__":
    test_safety_check()

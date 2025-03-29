import json
import os
from datetime import datetime

def test_json_processing():
    """Test the JSON file loading and filtering logic directly"""
    print("Testing JSON file processing...")

    # Try different paths for the mock file
    possible_paths = [
        'mocks/safety_response_log.json',  # Relative to CWD
        './mocks/safety_response_log.json',  # Explicit relative path
        os.path.join(os.path.dirname(__file__), 'mocks/safety_response_log.json'),  # Absolute path
    ]

    json_path = None
    for path in possible_paths:
        if os.path.exists(path):
            json_path = path
            print(f"Found mock file at: {json_path}")
            break
        else:
            print(f"Mock file not found at: {path}")

    if json_path is None:
        print("ERROR: Could not find the mock file!")
        print(f"Current working directory: {os.getcwd()}")
        return

    try:
        with open(json_path, 'r') as f:
            all_data = json.load(f)
            print(f"Loaded {len(all_data)} records from JSON file")

            # Debug: Print first few records to verify structure
            if all_data and len(all_data) > 0:
                print("First record structure:")
                print(json.dumps(all_data[0], indent=2))

            # Ensure all_data is a list
            if not isinstance(all_data, list):
                print("WARNING: all_data is not a list, converting...")
                if isinstance(all_data, dict):
                    # If it's a dict with a data array
                    if 'data' in all_data and isinstance(all_data['data'], list):
                        all_data = all_data['data']
                    else:
                        # Convert dict to single-item list
                        all_data = [all_data]

            # Filter out records where user_id is USR01235
            filtered_data = []
            for record in all_data:
                user_id = record.get('user_id')
                print(f"Processing record with user_id: {user_id}")
                if user_id != 'USR01235':
                    filtered_data.append(record)

            print(f"After filtering USR01235: {len(filtered_data)} records remain")

            if not filtered_data:
                print("WARNING: No records remain after filtering!")
                # Return all data without filtering as a fallback
                print("Using all data without filtering as fallback")
                filtered_data = all_data

            # Sort by timestamp in descending order
            try:
                sorted_data = sorted(
                    filtered_data,
                    key=lambda x: x.get('timestamp', ''),
                    reverse=True
                )
                print("Successfully sorted data by timestamp")
            except Exception as sort_error:
                print(f"Error sorting data: {str(sort_error)}")
                # Return unsorted data as fallback
                sorted_data = filtered_data

            # Create the final result structure
            result = {"user_data": sorted_data}
            print(f"Final result contains {len(sorted_data)} records")

            # Print a sample of the final result
            print("\nSample of final result (first 2 records):")
            sample = {"user_data": sorted_data[:2]} if len(sorted_data) >= 2 else result
            print(json.dumps(sample, indent=2))

    except json.JSONDecodeError as json_error:
        print(f"JSON parsing error: {str(json_error)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    test_json_processing()

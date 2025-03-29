import os
from firebase_functions import https_fn
from firebase_admin import initialize_app, firestore, credentials
from flask import Flask, json, jsonify, request
from json.decoder import JSONDecodeError
from flask_cors import CORS  # CORS をインポート
# Create safety response data with current timestamp
from datetime import datetime

# Try to import pytz, install if not available
try:
    import pytz
except ImportError:
    import subprocess
    import sys
    print("Installing pytz module...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pytz"])
    import pytz

from earthquakes import get_earthquakes_mock

# Firebase初期化 - Try to use service account if available
try:
    service_account_path = 'serviceAccountKey.json'
    if os.path.exists(service_account_path):
        print(f"Using service account: {service_account_path}")
        cred = credentials.Certificate(service_account_path)
        initialize_app(cred)
    else:
        print("Service account file not found, using default initialization")
        initialize_app()
except Exception as e:
    print(f"Firebase initialization error: {str(e)}")
    # Still try to initialize without credentials as fallback
    initialize_app()

# Firestoreクライアントの初期化
db = firestore.client()

# Flaskアプリケーションの作成
app = Flask(__name__)
# すべてのルートでCORSを明示的に許可
CORS(app, resources={r"/*": {"origins": "*"}})


# Flaskルートの定義
@app.route('/', methods=['GET'])
def home():
    return 'Hello from Flask on Firebase Functions!'


@app.route('/api/hello', methods=['GET'])
def hello_api():
    name = request.args.get('name', 'World')
    return {'message': f'Hello, {name}!'}


@app.route('/users', methods=['GET'])
def get_users():
    try:
        with open('mocks/users.json', 'r') as f:
            user_data = json.load(f)
            return jsonify(user_data=user_data)  # 再度確認：キーワード引数のみ
    except FileNotFoundError:
        return jsonify(error='User data not found'), 404
    except JSONDecodeError:
        return jsonify(error='Invalid JSON format'), 500
    except Exception as e:
        return jsonify(error=f'An unexpected error occurred: {str(e)}'), 500


@app.route('/safetyCheck', methods=['GET'])
def safety_check():
    try:
        # First, check if we have data in Firestore
        safety_collection = db.collection('safety_response_logs')
        print("Attempting to fetch data from 'safety_response_logs'")

        try:
            safety_docs = list(safety_collection.stream())
            print(f"Firestore query completed, found {len(safety_docs)} documents")
        except Exception as firestore_error:
            print(f"Firestore query error: {str(firestore_error)}")
            safety_docs = []

        # If we have data in Firestore, use it
        if safety_docs:
            print(f"Processing {len(safety_docs)} documents from Firestore")

            # Convert Firestore documents to dictionaries
            all_data = []
            for doc in safety_docs:
                data = doc.to_dict()
                # Add document ID if needed
                data['id'] = doc.id
                all_data.append(data)

            print(f"Converted {len(all_data)} Firestore documents to dictionaries")

            # Filter out USR01235 in Python code
            filtered_data = [
                record for record in all_data
                if record.get('user_id') != 'USR01235'
            ]
            print(f"After filtering USR01235: {len(filtered_data)} records remain")

            # Sort by timestamp in descending order
            sorted_data = sorted(
                filtered_data,
                key=lambda x: x.get('timestamp', ''),
                reverse=True
            )

            return jsonify(user_data=sorted_data)

        # Fallback to JSON file if no Firestore data
        else:
            print("No documents found in Firestore, falling back to JSON file")
            # Try different paths for the mock file
            possible_paths = [
                'mocks/safety_response_log.json',  # Relative to CWD
                './mocks/safety_response_log.json',  # Explicit relative path
                os.path.join(os.path.dirname(__file__), 'mocks/safety_response_log.json'),  # Absolute path based on script location
            ]

            json_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    json_path = path
                    print(f"Found mock file at: {json_path}")
                    break
                else:
                    print(f"Mock file not found at: {path}")

            # If no valid path found, use the first one for error reporting
            if json_path is None:
                json_path = possible_paths[0]

            # Check if file exists
            if not os.path.exists(json_path):
                print(f"Warning: JSON file not found at {json_path}")
                print(f"Current working directory: {os.getcwd()}")
                # List files in the mocks directory if it exists
                mocks_dir = 'mocks'
                if os.path.exists(mocks_dir):
                    print(f"Files in {mocks_dir} directory: {os.listdir(mocks_dir)}")
                return jsonify(error=f'Mock data file not found: {json_path}'), 404

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
                        print("Returning all data without filtering as fallback")
                        filtered_data = all_data

                    # Sort by timestamp in descending order
                    try:
                        sorted_data = sorted(
                            filtered_data,
                            key=lambda x: x.get('timestamp', ''),
                            reverse=True
                        )
                    except Exception as sort_error:
                        print(f"Error sorting data: {str(sort_error)}")
                        # Return unsorted data as fallback
                        sorted_data = filtered_data

                    # Ensure we're returning a valid response
                    # Important: Use jsonify with keyword arguments to ensure proper structure
                    print(f"Returning {len(sorted_data)} records")
                    return jsonify(user_data=sorted_data)
            except json.JSONDecodeError as json_error:
                print(f"JSON parsing error: {str(json_error)}")
                return jsonify(error=f'Invalid JSON format in mock data: {str(json_error)}'), 500

    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"Error in safety_check: {str(e)}")
        print(f"Traceback: {error_traceback}")
        return jsonify(error=f'An unexpected error occurred: {str(e)}'), 500


@app.route('/earthquakes', methods=['GET'])
def get_earthquakes():
    return get_earthquakes_mock()


@app.route('/earthquakes/occur', methods=['POST'])
def occur_earthquake():
    occur_earthquake()


@app.route('/safetyPost', methods=['POST'])
def safety_post():
    try:
        # Get data from request
        request_data = request.get_json()

        if not request_data:
            return jsonify({
                'success': False,
                'error': 'リクエストデータが見つかりません'
            }), 400

        # Extract required fields
        status = request_data.get('status')

        # Validate required fields
        if not status:
            return jsonify({
                'success': False,
                'error': '必須フィールドが不足しています (user_id, location, status)'
            }), 400

        # Get current time in JST timezone
        jst = pytz.timezone('Asia/Tokyo')
        current_time = datetime.now(jst).isoformat()

        safety_data = {
            'user_id': "USR01235",
            'timestamp': current_time,
            'status': status,
            'location': "東京都千代田区外神田1-1-8"
        }

        # Add data to Firestore
        db.collection('safety_response_logs').add(safety_data)

        return jsonify({
            'success': True,
            'message': '安否情報が正常に記録されました',
            'data': safety_data
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'予期しないエラーが発生しました: {str(e)}'
        }), 500


# Firebase Functionsのエントリーポイント
@https_fn.on_request()
def api(req: https_fn.Request) -> https_fn.Response:
    # Flaskアプリケーションへリクエストを転送
    with app.request_context(req.environ):
        return app.full_dispatch_request()

# http://127.0.0.1:5001/ai-hackathon-202503/us-central1/api/

# Test function for direct execution
if __name__ == "__main__":
    print("Testing safety_check function directly...")

    # Call the safety_check function
    response = safety_check()

    # Print the response
    print("Response:")
    print(response.get_data(as_text=True))

import os
from firebase_functions import https_fn
from firebase_admin import initialize_app, firestore, credentials
from flask import Flask, json, jsonify, request
from json.decoder import JSONDecodeError
from flask_cors import CORS
from datetime import datetime

from firestore_insert_earthquakes import insert_earthquake_to_firestore

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
        # Get safety response data from Firestore
        safety_collection = db.collection('safety_response_logs')
        safety_docs = safety_collection.stream()

        # Convert to list of dictionaries
        all_data = []
        for doc in safety_docs:
            data = doc.to_dict()
            data['id'] = doc.id
            all_data.append(data)

        # Filter out records where user_id is USR01235
        filtered_data = [
            record for record in all_data
            if record.get('user_id') != 'USR01235'
        ]

        # Get user data from Firestore to match names
        users_collection = db.collection('users')
        users_docs = users_collection.stream()

        # Create a dictionary of user_id to user data for quick lookup
        users_dict = {}
        for user_doc in users_docs:
            user_data = user_doc.to_dict()
            user_id = user_data.get('user_id')
            if user_id:
                users_dict[user_id] = user_data

        # Add user name to each safety record
        for record in filtered_data:
            user_id = record.get('user_id')
            if user_id and user_id in users_dict:
                # Add user name and any other relevant user data
                record['user_name'] = users_dict[user_id].get('name', 'Unknown')
                # You can add more user fields if needed
                # record['user_email'] = users_dict[user_id].get('email')

        # Sort by timestamp in descending order
        sorted_data = sorted(
            filtered_data,
            key=lambda x: x.get('timestamp', ''),
            reverse=True
        )

        return jsonify(user_data=sorted_data)

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
    insert_earthquake_to_firestore(
        epicenter="東京都千代田区外神田1-1-8",
        intensity="震度7",
        magnitude=7.0
    )
    return jsonify({
        'success': True,
        'message': '地震情報が正常に登録されました'
    }), 200


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

    # Create an application context
    with app.app_context():
        try:
            # Get safety response data from Firestore
            safety_collection = db.collection('safety_response_logs')
            safety_docs = safety_collection.stream()

            print("Successfully connected to Firestore")

            # Convert to list of dictionaries
            all_data = []
            for doc in safety_docs:
                data = doc.to_dict()
                data['id'] = doc.id
                all_data.append(data)

            print(f"Retrieved {len(all_data)} safety records")

            # Filter out records where user_id is USR01235
            filtered_data = [
                record for record in all_data
                if record.get('user_id') != 'USR01235'
            ]

            print(f"After filtering USR01235: {len(filtered_data)} records remain")

            # Try to get user data
            try:
                users_collection = db.collection('users')
                users_docs = users_collection.stream()
                users_list = list(users_docs)
                print(f"Retrieved {len(users_list)} user records")

                # Print first user if available
                if users_list:
                    print("First user data:")
                    print(users_list[0].to_dict())
            except Exception as user_error:
                print(f"Error retrieving users: {str(user_error)}")

            # Sort by timestamp
            sorted_data = sorted(
                filtered_data,
                key=lambda x: x.get('timestamp', ''),
                reverse=True
            )

            # Print results
            print("\nResults:")
            for record in sorted_data[:3]:  # Print first 3 records
                print(f"User ID: {record.get('user_id')}, Status: {record.get('status')}")

        except Exception as e:
            import traceback
            print(f"Error: {str(e)}")
            print(traceback.format_exc())

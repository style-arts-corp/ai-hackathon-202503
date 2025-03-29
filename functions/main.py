from firebase_functions import https_fn
from firebase_admin import initialize_app, firestore
from flask import Flask, json, jsonify, request
from json.decoder import JSONDecodeError
from flask_cors import CORS  # CORS をインポート
# Create safety response data with current timestamp
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

# Firebase初期化
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
        safety_collection = db.collection('safety_response_log')
        safety_docs = list(safety_collection.stream())

        # If we have data in Firestore, use it
        if safety_docs:
            print(f"Found {len(safety_docs)} documents in Firestore")

            # Convert Firestore documents to dictionaries
            all_data = []
            for doc in safety_docs:
                data = doc.to_dict()
                # Add document ID if needed
                data['id'] = doc.id
                all_data.append(data)

            # Filter out USR01235 in Python code
            filtered_data = [
                record for record in all_data
                if record.get('user_id') != 'USR01235'
            ]

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
            with open('mocks/safety_response_log.json', 'r') as f:
                all_data = json.load(f)

                # Filter out records where user_id is USR01235
                filtered_data = [
                    record for record in all_data
                    if record.get('user_id') != 'USR01235'
                ]

                # Sort by timestamp in descending order
                sorted_data = sorted(
                    filtered_data,
                    key=lambda x: x.get('timestamp', ''),
                    reverse=True
                )

                return jsonify(user_data=sorted_data)

    except Exception as e:
        print(f"Error in safety_check: {str(e)}")
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
        db.collection('safety_response_log').add(safety_data)

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

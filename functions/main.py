from firebase_functions import https_fn
from firebase_admin import initialize_app
from flask import Flask, json, jsonify, request
from json.decoder import JSONDecodeError

# Firebase初期化
initialize_app()

# Flaskアプリケーションの作成
app = Flask(__name__)


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
        with open('mocks/safety_response_log.json', 'r') as f:
            user_data = json.load(f)
            return jsonify(user_data=user_data)  # 再度確認：キーワード引数のみ
    except FileNotFoundError:
        return jsonify(error='User data not found'), 404
    except JSONDecodeError:
        return jsonify(error='Invalid JSON format'), 500
    except Exception as e:
        return jsonify(error=f'An unexpected error occurred: {str(e)}'), 500


# Firebase Functionsのエントリーポイント
@https_fn.on_request()
def api(req: https_fn.Request) -> https_fn.Response:
    # Flaskアプリケーションへリクエストを転送
    with app.request_context(req.environ):
        return app.full_dispatch_request()

#http://127.0.0.1:5001/ai-hackathon-202503/us-central1/api/

from firebase_functions import https_fn
from firebase_admin import initialize_app, firestore
from flask import Flask, json, jsonify, request
from json.decoder import JSONDecodeError

# Firebase初期化
initialize_app()

# Firestoreクライアントの初期化
db = firestore.client()

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


@app.route('/import-users-to-firestore', methods=['POST'])
def import_users_to_firestore():
    try:
        # users.jsonからデータを読み込む
        with open('mocks/users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
        
        # Firestoreのバッチ処理を初期化
        batch = db.batch()
        
        # 追加されたユーザー数をカウント
        added_count = 0
        
        # 各ユーザーをFirestoreに追加
        for user in users:
            user_ref = db.collection('users').document(user['id'])
            batch.set(user_ref, user)
            added_count += 1
        
        # バッチコミット実行
        batch.commit()
        
        return jsonify({
            'success': True,
            'message': f'{added_count}人のユーザーデータがFirestoreに正常にインポートされました'
        })
    
    except FileNotFoundError:
        return jsonify({
            'success': False,
            'error': 'ユーザーデータファイルが見つかりません'
        }), 404
    except JSONDecodeError:
        return jsonify({
            'success': False, 
            'error': 'JSONフォーマットが無効です'
        }), 500
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

#http://127.0.0.1:5001/ai-hackathon-202503/us-central1/api/

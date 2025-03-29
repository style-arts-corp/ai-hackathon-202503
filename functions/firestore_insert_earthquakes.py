from datetime import datetime, timezone
import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

def insert_earthquake_to_firestore(
    epicenter: str,
    intensity: str,
    magnitude: float,
):
    try:
        print("Firebase初期化状態の確認...")
        if not firebase_admin._apps:
            print("Firebaseが初期化されていません。初期化を実行します。")
            cred = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(cred)
        
        id = str("EQ" + datetime.now(timezone.utc).strftime("%Y%m%d"))
        print(f"生成されたID: {id}")
        # Firestoreクライアントの初期化（既存のアプリケーションを使用）
        db = firestore.client()
        print("Firestoreクライアントの初期化完了")

        # 各地震データをFirestoreに追加
        data = {
            'id': id,
            'epicenter': epicenter,
            'intensity': intensity,
            'magnitude': magnitude,
            'time': firestore.SERVER_TIMESTAMP,
        }
        print(f"保存するデータ: {data}")
        earthquake_ref = db.collection('earthquakes').document(id)
        earthquake_ref.set(data)
        print(f"ドキュメント参照: {earthquake_ref}")
        print(f"成功: 地震データがFirestoreに正常にインポートされました")
    
    except FileNotFoundError as e:
        print(f"エラー: ファイルが見つかりません - {e}")
    except json.JSONDecodeError as e:
        print(f"エラー: JSONのデコードに失敗しました - {str(e)}")
    except Exception as e:
        print(f"エラー: 予期しないエラーが発生しました - {str(e)}")

def import_earthquakes_to_firestore():
    """
    ローカル環境でFirestoreにearth_quake.jsonのデータをインポートするスクリプト
    
    注意: このスクリプトを実行する前に、サービスアカウントのキーファイルが必要です。
    Firebase Consoleから取得して、serviceAccountKey.jsonという名前で保存してください。
    """
    try:
        # Firebase初期化（ローカル環境用）
        service_account_path = 'serviceAccountKey.json'
        
        if not os.path.exists(service_account_path):
            print(f"エラー: {service_account_path} が見つかりません。")
            print("Firebase Consoleからサービスアカウントのキーをダウンロードして、このディレクトリに保存してください。")
            return
        
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)
        
        # Firestoreクライアントの初期化
        db = firestore.client()
        
        # earth_quake.jsonからデータを読み込む
        json_path = 'mocks/earth_quake.json'
        with open(json_path, 'r', encoding='utf-8') as f:
            earthquakes = json.load(f)
        
        # Firestoreのバッチ処理を初期化
        batch = db.batch()
        
        # 追加された地震データの数をカウント
        added_count = 0
        
        # 各地震データをFirestoreに追加
        for earthquake in earthquakes:
            # IDフィールドを使用してドキュメントIDを設定
            earthquake_ref = db.collection('earthquakes').document(earthquake['id'])
            batch.set(earthquake_ref, earthquake)
            added_count += 1
        
        # バッチコミット実行
        batch.commit()
        
        print(f"成功: {added_count}件の地震データがFirestoreに正常にインポートされました")
    
    except FileNotFoundError as e:
        print(f"エラー: ファイルが見つかりません - {e}")
    except json.JSONDecodeError:
        print(f"エラー: {json_path} のJSONフォーマットが無効です")
    except Exception as e:
        print(f"エラー: 予期しないエラーが発生しました - {str(e)}")

if __name__ == "__main__":
    import_earthquakes_to_firestore() 
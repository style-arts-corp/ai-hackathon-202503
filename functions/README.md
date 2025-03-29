# Firebase Functions から Firestore へのデータインポート

このプロジェクトは、Firebase Functions を使用して Firestore にデータをインポートする方法を示します。

## セットアップ

1. 依存関係のインストール:

```bash
cd functions
pip install -r requirements.txt
```

2. ローカル環境でテストする場合は、サービスアカウントキーが必要です:
   - Firebase Console から [プロジェクト設定] > [サービスアカウント] に移動
   - [新しい秘密鍵の生成] をクリックして JSON キーファイルをダウンロード
   - ダウンロードしたファイルを `functions/serviceAccountKey.json` として保存

## 使用方法

### 方法1: Firebase Functions としてデプロイして使用

1. Firebase プロジェクトにデプロイ:

```bash
firebase deploy --only functions
```

2. POST リクエストを送信してユーザーをインポート:

```bash
curl -X POST https://us-central1-[YOUR-PROJECT-ID].cloudfunctions.net/api/import-users-to-firestore
```

### 方法2: ローカルスクリプトで直接実行

サービスアカウントキーを `functions/serviceAccountKey.json` として保存した後:

```bash
cd functions
python import_users.py
```

## 注意事項

- `mocks/users.json` ファイルには、Firestore にインポートするユーザーデータが含まれています
- ユーザーデータの ID フィールドは一意である必要があります
- 同じ ID を持つドキュメントがすでに存在する場合、データは上書きされます 
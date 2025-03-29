# ai-hackathon-202503

## プロジェクト概要

このプロジェクトは「ai-hackathon-202503」という名前のFirebaseプロジェクトです。Firebase FunctionsとFirestoreを使用しており、Pythonで実装されています。

## セットアップ方法

### 前提条件

- Python 3.11
- Firebase CLI
- Node.js と npm
- Java 8以上（Firebaseエミュレーター用）

### 手順

1. リポジトリをクローンする

```bash
git clone <リポジトリURL>
cd ai-hackathon-202503
```

2. Firebase CLIをインストール（まだの場合）

```bash
npm install -g firebase-tools
```

3. Firebaseにログイン

```bash
firebase login
```

4. Functionsのための仮想環境をセットアップ

```bash
cd functions && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

5. Java（Firebaseエミュレーター用）をインストール

```bash
# macOSの場合（Homebrew使用）
brew install openjdk@17
sudo ln -sfn $(brew --prefix)/opt/openjdk@17/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-17.jdk

# インストールの確認
java -version
```

## エミュレーターの起動方法

Firebaseエミュレーターを使用して、ローカル環境でプロジェクトをテストできます。

```bash
# プロジェクトのルートディレクトリで実行
firebase emulators:start
```

これにより、以下のエミュレーターが起動します：

- Functions: ポート5001
- Firestore: ポート8080
- エミュレーターUI: ポート4000（デフォルト）

エミュレーターUIには、ブラウザで以下のURLからアクセスできます：
[http://localhost:4000](http://localhost:4000)

## 開発方法

1. `functions/main.py`にFunctionsのコードを追加できます
2. ローカル環境でテストする場合は、エミュレーターを使用してください
3. デプロイする場合は以下のコマンドを実行します

```bash
firebase deploy
```

部分的なデプロイも可能です：

```bash
firebase deploy --only functions
firebase deploy --only firestore
```

## local の API エンドポイント

http://127.0.0.1:5001/ai-hackathon-202503/us-central1/api
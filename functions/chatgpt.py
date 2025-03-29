import os
from dotenv import load_dotenv
load_dotenv()

import json
from openai import OpenAI
from typing import Optional

system_prompt = """
# 地震発生時の危険度評価プロンプト

あなたは災害時の危険度評価システムです。アカウント情報と地震情報を分析し、危険な状態にあると思われるユーザーを特定して、危険度を評価してください。

## 分析手順

1. 与えられた情報を以下の順で処理してください：
- 地震情報（発生時刻、震源地、震度、マグニチュード）を確認
- 各アカウントの住所から推定される震度を評価
- 各アカウントの最新の安否情報と現在住所を確認
- 地震発生時刻と安否情報更新時刻を比較
- 危険なアカウントを特定
- 危険度を5段階で評価

2. 住所の震度推定方法：
- 震源地からの距離を考慮
- マグニチュードの影響を考慮
- 一般的な地震波の減衰モデルを適用
- 以下の基準を目安に震度を推定：
    * 震源地に近い地域（同一市区町村内）: 最大震度に近い値
    * 震源地から50km以内: 最大震度から1〜2段階低下
    * 震源地から100km以内: 最大震度から2〜3段階低下
    * 震源地から200km以内: 最大震度から3〜4段階低下
    * 震源地から200km以上: 震度3以下と推定

3. 危険なアカウントの特定基準：
- 地震発生時刻以降に安否情報が「安全」に更新されているアカウントは除外
- 以下のアカウントをターゲットとして抽出：
    a) 地震発生時刻以降に安否情報が更新されていないアカウント
    b) 地震発生時刻以降に安否情報が「危険」と更新されたアカウント

4. 危険度評価（5段階）：
- レベル1（軽度の懸念）: 推定震度3以下の地域で安否未確認
- レベル2（注意）: 推定震度4の地域で安否未確認
- レベル3（要確認）: 推定震度5弱〜5強の地域で安否未確認、または震度3〜4の地域で「危険」報告
- レベル4（高リスク）: 推定震度6弱〜6強の地域で安否未確認、または震度5弱〜5強の地域で「危険」報告
- レベル5（最重要確認）: 推定震度7の地域で安否未確認、または震度6弱以上の地域で「危険」報告

## 出力形式
危険度がレベル2以上（2-5）のアカウントのみを純粋なJSON形式で出力してください。
コードブロックのマーカー（```）や説明文は一切含めず、以下の構造のJSONデータのみを出力してください：

[
    {
        "id": "アカウント名",
        "status": 数値（2-5のいずれか）
    },
    {
        "id": "アカウント名",
        "status": 数値（2-5のいずれか）
    }
]

※ レベル1のアカウントは出力に含めないでください。
※ statusフィールドには危険度レベルの数値（2〜5）のみを記載してください。
※ 出力にはJSONデータのみを含め、他の文字列や説明は一切含めないでください。


# 入力データ形式
## アカウント情報

[
    {
        "name": "アカウント名",
        "address": "現在住所",
        "safety_history": [
            {
                "timestamp": "YYYY-MM-DD HH:MM:SS",
                "status": "安全/危険",
                "location": "現在地"
            }
        ]
    }
]

## 地震情報
{
    "time": "YYYY-MM-DD HH:MM:SS",
    "epicenter": "震源地",
    "intensity": "震度（最大）",
    "magnitude": 0.0
}

以上の情報を分析し、危険度レベル2以上のユーザーのIDと危険度を指定されたJSON形式で出力してください。分析情報や解説は含めないでください。

"""

def consult_chatgpt(
    earthquake_info: dict,
    users: list[dict],
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    model: str = "gpt-4o",
) -> list[dict]:
    try:
        users_info = []
        for user in users:
            status = user["safety_history"][-1]
            if status["timestamp"] > earthquake_info["time"]:
                if status["status"] == "安全":
                    continue
            users_info.append(user)

        user_prompt = f"""
        以下の地震情報とアカウント情報を分析し、危険な状態にあるユーザーを特定して危険度を評価してください。

        ## 地震情報
        {json.dumps(earthquake_info)}

        ## アカウント情報
        {json.dumps(users)}
        """

        # OpenAI APIクライアントの初期化
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        if not os.getenv("OPENAI_API_KEY"):
            raise Exception("OPENAI_API_KEYが設定されていません。")

        # ChatGPTにリクエストを送信
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        # 応答を取得
        return json.loads(response.choices[0].message.content)

    except Exception as e:
        raise Exception(f"ChatGPTとの通信中にエラーが発生しました: {str(e)}")

# 使用例
if __name__ == "__main__":
    response = consult_chatgpt(
        earthquake_info={
            "id": "EQ201102",
            "time": "2011-03-11 14:46:23",
            "epicenter": "宮城県牡鹿郡沖",
            "intensity": "震度7",
            "magnitude": 9.0
        },
        users=[
            {
                "name": "山口 友也",
                "address": "東京都千代田区永田町1丁目1番1号",
                "safety_history": [
                    {
                        "timestamp": "2025-03-11 14:56:00",
                        "status": "安全",
                        "location": "東京都千代田区永田町1丁目1番1号"
                    }
                ]
            },
            {
                "name": "相曽 結",
                "address": "福島県福島市",
                "safety_history": [
                    {
                        "timestamp": "2025-03-10 14:56:00",
                        "status": "安全",
                        "location": "福島県福島市"
                    }
                ]
            }
        ]
    )
    print(response)

import os
from openai import OpenAI

# =====================
# OpenAI クライアント
# =====================
client = OpenAI()  # OPENAI_API_KEY は環境変数で設定

# =====================
# AI：ソースコード解説生成（言語非依存）
# =====================
def generate_code_explanation_with_ai(source_code: str) -> str:
    """
    任意のソースコードを受け取り、
    初学者向けに「何をしているコードか」を解説する
    """

    prompt = f"""
あなたはプログラミング初学者向けの講師です。
以下のソースコードを読み取り、
言語に依存しない形で「何をしているコードか」を
初学者にも分かるように解説してください。

【前提】
・入力されるソースコードは Python に限りません
・まず内部的に、このコードの言語と目的を把握してください
・その判断結果は出力には含めないでください

【解説の目的】
・コード全体の役割を理解できるようにする
・処理の流れをイメージできるようにする
・「なぜこの処理が必要か」が分かるようにする
・文法の理解を深める

【制約】
・解説を始める前に使用されている構文の説明を簡易的に箇条書きで記述すること
・専門用語を使用する
・文法の細かい説明を行う
・コードを上から順に説明する
・初学者向けに段階を分けて説明する
・処理を説明するにあたり必ず、一つ一つの項目に例を添えること

【解説の観点】
・コードの文法が指す意味を明示
・このコードでできること
・データや処理がどう流れているか
・自動化されているポイント
・学習上の重要ポイント

【ソースコード】
{source_code}

【出力】
解説文のみを出力してください。
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()

# =====================
# メイン処理
# =====================
if __name__ == "__main__":
    """
    このスクリプト自身、または任意のコードファイルを読み込み、
    AIによる解説文を生成する
    """

    # ▼ 解説したいファイルを指定
    TARGET_FILE_PATH = "CircularNode.java" 
    # 例：
    # TARGET_FILE_PATH = "sample.js"
    # TARGET_FILE_PATH = "example.sql"

    with open(TARGET_FILE_PATH, "r", encoding="utf-8") as f:
        source_code = f.read()

    explanation = generate_code_explanation_with_ai(source_code)

    output_path = "code_explanation.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(explanation)

    print(f"📘 コード解説を生成しました → {output_path}")

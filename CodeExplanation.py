import os
from openai import OpenAI

client = OpenAI()  

TARGET_DIR = "TargetFile"     
OUTPUT_DIR = "TargetFileText"        

os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_code_explanation_with_ai(source_code: str) -> str:
    prompt = f"""
あなたはプログラミング初学者向けの講師です。
以下のソースコードを読み取り、
処理の目的や流れは言語に依存しない形で説明しつつ、
文法については、使用されている言語の文法として
明示的に解説してください。

【前提】
・入力されるソースコードは Python に限りません
・まず内部的に、このコードの言語と目的を把握してください
・その判断結果は出力には含めないでください

【解説の目的】
・コード全体の役割を理解できるようにする
・処理の流れをイメージできるようにする
・なぜこの処理が必要なのかを理解できるようにする
・文法の理解を深める
・コードの読解力を高める

【出力構成（必須）】

① 【使用されている文法・構文一覧】
最初に、コード全体で使われている文法・構文を
以下の形式で必ず列挙してください。

- 構文名：
- 文法カテゴリ（文／式／演算子／キーワードなど）：
- 一般的な意味：

② 【コードの行ごとの解説】
コードを上から順に、1行ずつ解説してください。
各行について、必ず次の順で説明してください。

1. 使用されている文法・構文（構文名を明示）
2. その文法が表す一般的な意味
3. このコード内で果たしている役割

③ 【処理の流れのまとめ】
・データや処理がどの順序で流れているか
・途中でデータの形がどう変わるか

④ 【学習上の重要ポイント】
・このコードを読む上で重要な考え方
・他のコードにも応用できるポイント

⑤ 【Q&A（初学者向け）】
・この解説を読んだ初学者が
　疑問に思いそうな点をQ&A形式で記述してください

【制約】
・文法の説明を省略しないこと
・処理の説明と文法の説明を混同しないこと
・各段落は50文字以内を目安に区切ること
・初学者向けに、段階を分けて説明すること
・必要に応じて簡単な例を添えること

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

if __name__ == "__main__":

    for filename in os.listdir(TARGET_DIR):
        input_path = os.path.join(TARGET_DIR, filename)

        if not os.path.isfile(input_path):
            continue

        with open(input_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        explanation = generate_code_explanation_with_ai(source_code)

        base_name, _ = os.path.splitext(filename)
        output_filename = f"{base_name}.txt"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(explanation)

        print(f"📘 解説生成完了 → {output_filename}")

    print("✅ すべてのファイルの解説が完了しました")

# Code Explanation Generator（AI解説自動生成ツール）

## 概要

このツールは、任意のソースコードを AI に解析させ、  
**プログラミング初学者向けの詳細な解説テキストを自動生成する  
Python スクリプト**です。

指定ディレクトリ内のソースコードを一括で読み込み、

- 使用されている文法・構文
- 行ごとの処理内容
- 処理全体の流れ
- 学習上の重要ポイント
- 初学者が疑問に思いそうな Q&A

を体系的にまとめた **解説テキスト（.txt）** を生成します。

---

## 主な特徴

- 言語非依存（Python 以外のコードも対応）
- 初学者向けに特化した解説構成
- 複数ファイルの一括処理が可能
- コード読解力・文法理解の補助に有効
- 学習ログ・日報・教材作成に利用可能

---
## ディレクトリ構成

```text
project/
├── main.py
├── TargetFile/
│   ├── sample.py
│   └── example.java
└── TargetFileText/
    ├── sample.txt
    └── example.txt
```
---

## 動作概要

1. TargetFile ディレクトリ内のファイルを順に読み込む  
2. 各ソースコードを AI に送信  
3. 初学者向けの解説文を生成  
4. 同名の .txt ファイルとして TargetFileText に保存  

---

## 使用技術

- Python 3.x
- OpenAI API
- openai Python SDK
- 標準ライブラリ（os）

---

## 事前準備

### OpenAI APIキーの設定

環境変数に API キーを設定。

```bash
export OPENAI_API_KEY="your_api_key"

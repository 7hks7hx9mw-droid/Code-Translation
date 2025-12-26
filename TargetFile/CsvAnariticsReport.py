import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os
from openai import OpenAI

# =====================
# OpenAI クライアント
# =====================
client = OpenAI()  # OPENAI_API_KEY は環境変数で設定

plt.rcParams["font.family"] = "Hiragino Sans"

CSV_DIR = "csv_files"
PNG_DIR = "csv_png"
PDF_DIR = "csv_pdf"

os.makedirs(PNG_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

monthly_totals = []

# =====================
# AI：月次売上推移の文章生成
# =====================
def generate_trend_analysis_with_ai(summary, monthly_df, product_sales):
    monthly_sales = monthly_df.set_index("month")["total_sales"].to_dict()

    prompt = f"""
あなたは売上分析の専門家です。
以下の数値データをもとに、
クライアントに提出する業務レポート用の
「月次売上の推移」に関する文章を作成してください。

【制約】
・断定しすぎない
・専門用語は使わない
・経営判断の材料になる示唆を含める
・日本語で簡潔に（2〜4文）

【数値データ】
総売上: {summary['total_sales']} 円
平均注文単価: {summary['avg_sales']:.0f} 円
月次売上: {monthly_sales}
主力商品: {product_sales.index[0]}（{product_sales.iloc[0]} 円）

【出力】
文章のみを出力してください。
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()

# =====================
# CSVごとの既存処理
# =====================
for csv_file in sorted(os.listdir(CSV_DIR)):
    if not csv_file.endswith(".csv"):
        continue

    path = os.path.join(CSV_DIR, csv_file)
    df = pd.read_csv(path, sep=None, engine="python")
    df["date"] = pd.to_datetime(df["date"])

    summary = {
        "total_sales": df["sales_amount"].sum(),
        "avg_sales": df["sales_amount"].mean(),
        "repeat_customers": df["customer_id"].nunique()
    }

    product_sales = (
        df.groupby("product")["sales_amount"]
        .sum()
        .sort_values(ascending=False)
    )

    base_name = csv_file.replace(".csv", "")

    # 商品別棒グラフ（既存）
    plt.figure()
    product_sales.plot(kind="bar")
    plt.title("Product Sales")
    plt.tight_layout()
    product_png = os.path.join(PNG_DIR, f"{base_name}_product_sales.png")
    plt.savefig(product_png)
    plt.close()

    # PDF（既存）
    pdf_path = os.path.join(PDF_DIR, f"{base_name}_report.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawString(20*mm, height - 30*mm, "Sales Analysis Report")

    c.setFont("Helvetica", 11)
    text = c.beginText(20*mm, height - 45*mm)
    text.textLine(f"Total Sales: {summary['total_sales']:,} JPY")
    text.textLine(f"Average Order Value: {summary['avg_sales']:,.0f} JPY")
    c.drawText(text)

    c.drawImage(
        product_png,
        20*mm,
        height - 160*mm,
        width=170*mm,
        preserveAspectRatio=True
    )

    c.showPage()
    c.save()

    # 月次集計（既存）
    month = df["date"].dt.to_period("M")[0]
    monthly_totals.append({
        "month": month.to_timestamp(),
        "total_sales": summary["total_sales"]
    })

# =====================
# 月次折れ線グラフ（既存）
# =====================
monthly_df = pd.DataFrame(monthly_totals).sort_values("month")

plt.figure()
plt.plot(monthly_df["month"], monthly_df["total_sales"], marker="o")
plt.title("月次売上推移")
plt.xlabel("月")
plt.ylabel("売上金額")
plt.grid(True)
plt.tight_layout()

trend_png = os.path.join(PNG_DIR, "monthly_sales_trend.png")
plt.savefig(trend_png)
plt.close()

# =====================
# ★ AI分析文を含む最終レポート（完成形）
# =====================
ai_trend_text = generate_trend_analysis_with_ai(
    summary,
    monthly_df,
    product_sales
)

final_report = f"""
【売上分析レポート】

■ 全体サマリー
対象期間の総売上は {summary['total_sales']:,} 円でした。
平均注文単価は {summary['avg_sales']:,.0f} 円となっています。

■ 月次売上の推移
{ai_trend_text}

■ 商品別売上分析
商品別では「{product_sales.index[0]}」が {product_sales.iloc[0]:,} 円と最も高く、
全体売上を牽引する主力商品となっています。
"""

report_path = os.path.join(PDF_DIR, "analysis_report.txt")
with open(report_path, "w", encoding="utf-8") as f:
    f.write(final_report.strip())

print(f"📝 AI分析レポートを作成しました → {report_path}")

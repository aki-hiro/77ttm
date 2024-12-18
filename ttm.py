import requests
from bs4 import BeautifulSoup
import csv

# 七十七銀行のTTMレートのURL
url = "https://www.77bank.co.jp/kawase/usd2024.html"

# ウェブページを取得
response = requests.get(url)
response.encoding = response.apparent_encoding  # エンコーディングを設定
soup = BeautifulSoup(response.text, 'html.parser')

# テーブルを取得
table = soup.find('table')

# テーブルが存在するか確認
if table is None:
    print("テーブルが見つかりませんでした。")
else:
    print("テーブルが見つかりました。")

# CSVファイルの作成
data_list = []

with open('ttm_rates.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    # 行ヘッダと列ヘッダを取得
    rows = table.find_all('tr')
    
    # 各月のデータを取得
    for row in rows:
        cells = row.find_all(['td'])
        if row.find('th'):
            day = row.find('th').get_text(strip=True)
            if not day.isdigit():
                continue
            
            for month in range(1, 13):  # 1から12までの月をループ
                if month - 1 < len(cells):  # セルの範囲を確認
                    rate = cells[month - 1].get_text(strip=True)
                    if rate:  # レートが空でない場合のみ追加
                        date_str = f"2024-{str(month).zfill(2)}-{str(day).zfill(2)}"
                        data_list.append((date_str, rate))  # タプルとしてリストに追加

    # 日付でソート
    data_list.sort(key=lambda x: x[0])

    # CSVに書き込む
    for date_str, rate in data_list:
        writer.writerow([date_str, rate])
        print(f"{date_str},{rate}")  # デバッグ出力

print("CSVファイルにTTMレートを出力しました。")

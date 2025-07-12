# scrape_today_race.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re

# Chromeのオプション設定（ヘッドレス実行したい場合は "--headless" を有効に）
options = Options()
# options.add_argument('--headless')  # ヘッドレスにしたい場合はコメント解除

# ChromeDriverの起動
driver = webdriver.Chrome(options=options)
driver.get("https://race.netkeiba.com/top/")

# ページの読み込み待機
time.sleep(3)

# ページのHTMLを取得
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# レースIDを収集
race_ids = []
for a in soup.find_all('a', href=True):
    href = a['href']
    m = re.search(r'race_id=(\d+)', href)
    if m:
        race_id = m.group(1)
        if race_id not in race_ids:
            race_ids.append(race_id)

driver.quit()

# ファイルへ保存
with open("race_ids.txt", "w", encoding="utf-8") as f:
    for race_id in race_ids:
        f.write(race_id + "\n")

print(f"取得したレース数: {len(race_ids)}")
print("race_ids.txt に保存しました。")

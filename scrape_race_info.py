import requests
from bs4 import BeautifulSoup
import csv
import os

CSV_FILE = 'race_info.csv'
RACE_IDS_FILE = 'race_ids.txt'

# JRAの競馬場コードと名称
JRA_PLACE_CODE = {
    '01': '札幌', '02': '函館', '03': '福島', '04': '新潟', '05': '東京',
    '06': '中山', '07': '中京', '08': '京都', '09': '阪神', '10': '小倉'
}

def get_race_components(race_id):
    """race_idから構成要素を抽出"""
    place_code = race_id[4:6]
    kaikai = race_id[6:8]
    nichime = race_id[8:10]
    race_num = race_id[10:12]
    return {
        'place': JRA_PLACE_CODE.get(place_code, '不明'),
        'place_code': place_code,
        '開催回数': int(kaikai),
        '開催日目': int(nichime),
        'race_number': int(race_num)
    }

from bs4 import BeautifulSoup
import requests

JRA_PLACE_CODE = {
    '01': '札幌', '02': '函館', '03': '福島', '04': '新潟', '05': '東京',
    '06': '中山', '07': '中京', '08': '京都', '09': '阪神', '10': '小倉'
}

def get_place_name(race_id):
    place_code = race_id[4:6]
    return JRA_PLACE_CODE.get(place_code, '不明')

from bs4 import BeautifulSoup
import requests

JRA_PLACE_CODE = {
    '01': '札幌', '02': '函館', '03': '福島', '04': '新潟', '05': '東京',
    '06': '中山', '07': '中京', '08': '京都', '09': '阪神', '10': '小倉'
}

def get_place_name(code):
    return JRA_PLACE_CODE.get(code, '不明')

def parse_race_info(race_id):
    import requests
    from bs4 import BeautifulSoup

    url = f'https://race.netkeiba.com/race/shutuba.html?race_id={race_id}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')

    race_name = start_time = course = weather = track_condition = ''
    distance = 0
    ground = ''

    try:
        race_name = soup.select_one('.RaceName').text.strip()
    except:
        pass

    try:
        # 例: 15:45発走 / 芝2000m (右 B) / 天候:曇 / 馬場:良
        data = soup.select_one('.RaceData01').get_text(separator=' / ', strip=True)
        parts = [p.strip() for p in data.split('/') if p.strip()]

        # 時刻
        for p in parts:
            if '発走' in p:
                start_time = p.replace('発走', '').strip()
            elif '芝' in p or 'ダート' in p:
                course = p.strip()
                ground = '芝' if '芝' in p else 'ダート'
                distance_str = ''.join([c for c in p if c.isdigit()])
                if distance_str:
                    distance = int(distance_str)
            elif '天候' in p:
                weather = p.split(':')[-1].strip()
            elif '馬場' in p:
                track_condition = p.split(':')[-1].strip()
    except:
        pass

    # race_id 構造から場所などを抽出
    place_code = race_id[4:6]
    place = JRA_PLACE_CODE.get(place_code, '不明')
    round_num = int(race_id[6:8])
    day_num = int(race_id[8:10])
    race_num = int(race_id[10:12])

    return {
        'race_id': f"'{race_id}",
        'race_name': race_name,
        'place': place,
        '開催回数': round_num,
        '開催日目': day_num,
        'race_num': race_num,
        'start_time': start_time,
        'course': course,
        'weather': weather,
        'track_condition': track_condition,
        'distance': distance,
        'ground': ground
    }


def save_to_csv(race_info):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'race_id', 'race_name', 'place', '開催回数', '開催日目',
            'race_num', 'start_time', 'course', 'weather',
            'track_condition', 'distance', 'ground'
        ])
        if not file_exists:
            writer.writeheader()
        writer.writerow(race_info)

if __name__ == '__main__':
    # race_ids.txt の最初の行だけ取得
    with open(RACE_IDS_FILE, 'r', encoding='utf-8') as f:
        race_ids = [line.strip() for line in f if line.strip()]

    if race_ids:
        race_id = race_ids[0]
        print(f"[INFO] 処理中: {race_id}")
        info = parse_race_info(race_id)
        if info:
            save_to_csv(info)
            print("[OK] CSVに保存しました")
    else:
        print("[ERROR] race_ids.txt にレースIDが見つかりませんでした。")

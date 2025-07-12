from sqlalchemy import create_engine, text

# PostgreSQL接続情報（パスワードをあなたのものに）
user = 'postgres'
password = 'iluilu6X'
host = 'localhost'
port = '5432'
dbname = 'jra'

url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}'
engine = create_engine(url)

# race_infoテーブルを作成（存在しなければ）
create_table_sql = text("""
CREATE TABLE IF NOT EXISTS race_info (
    race_id VARCHAR PRIMARY KEY,
    date DATE,
    race_number INTEGER,            -- 追加：第何レースか
    start_time TIME,               -- 追加：発走時刻
    race_name TEXT,
    course TEXT,
    distance INTEGER,
    ground TEXT,
    grade TEXT,
    weather TEXT,
    track_condition TEXT
);
""")

with engine.connect() as conn:
    conn.execute(create_table_sql)
    print("✅ テーブル race_info を作成または更新しました")

from sqlalchemy import create_engine, text

# 接続情報（パスワードはあなたがPostgreSQLインストール時に決めたものに置き換えてください）
user = 'postgres'
password = 'iluilu6X'
host = 'localhost'
port = '5432'
dbname = 'jra'

# SQLAlchemy用の接続URLを作成
url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}'
engine = create_engine(url)

# テスト接続してバージョンを表示
with engine.connect() as conn:
    result = conn.execute(text("SELECT version();"))
    print(result.fetchone())

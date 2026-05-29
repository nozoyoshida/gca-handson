# Cloud Run 用 Dockerfile（お問い合わせ管理 API / Flask）
FROM python:3.12-slim

WORKDIR /app

# 依存関係を先にインストールしてレイヤーキャッシュを効かせる
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud Run は PORT 環境変数（既定 8080）でリッスンすることを期待する。
# gunicorn で app.py の app オブジェクト（app:app）を起動する。
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app

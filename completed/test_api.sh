#!/bin/bash
BASE_URL="http://localhost:5000"

echo "=== 全チケット取得 ==="
curl -s $BASE_URL/tickets | python3 -m json.tool

echo -e "\n=== チケット作成 ==="
curl -s -X POST $BASE_URL/tickets \
  -H "Content-Type: application/json" \
  -d '{"title": "テスト用チケット", "description": "これはテストです", "priority": "medium", "customer_id": 1}' | python3 -m json.tool

echo -e "\n=== ステータスでフィルタ ==="
curl -s "$BASE_URL/tickets?status=open" | python3 -m json.tool

echo -e "\n=== チケット検索 ==="
curl -s "$BASE_URL/tickets/search?q=ログイン" | python3 -m json.tool

echo -e "\n=== 特定チケット取得 ==="
curl -s $BASE_URL/tickets/1 | python3 -m json.tool

echo -e "\n=== ステータス変更 ==="
curl -s -X PATCH $BASE_URL/tickets/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}' | python3 -m json.tool

echo -e "\n=== チケット更新 ==="
curl -s -X PUT $BASE_URL/tickets/1 \
  -H "Content-Type: application/json" \
  -d '{"assignee": "田中"}' | python3 -m json.tool

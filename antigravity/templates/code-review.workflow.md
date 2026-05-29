# /code-review — セキュリティ重視のコードレビュー（Workflow 雛形）

> Antigravity の Workflow 定義（`/code-review` で起動）。Ch.2 でこの内容を
> `.agents/workflows/code-review.md` にコピーして使います。
> ※ Workflow の正式なファイル配置・記法は Antigravity 公式ドキュメントで確認してください。

## 目的
現在の変更（`git diff`）を、チームのコーディング規約とセキュリティ基準に照らしてレビューする。

## 手順
1. `git diff`（必要に応じてステージ済みの差分も）を確認する。
2. 以下の観点で問題を指摘し、各指摘に「重大度」と「具体的な修正案」を付ける。

### セキュリティ（最優先）
- SQL に f-string / % / .format() でユーザー入力を埋め込んでいないか（→ パラメータ化クエリ）
- すべてのユーザー入力にバリデーションがあるか（最大長・HTML 除去・enum 許可リスト）
- 秘密鍵・パスワードのハードコードがないか（→ 環境変数）
- debug=True のまま本番に出ていないか

### コード品質
- 全関数に Google Style の docstring があるか
- エラーは `{"error": "..."}` の JSON と適切な HTTP ステータスで返しているか
- 命名は snake_case か、DB 接続を close しているか

3. 重大度（critical / high / medium / low）順に要約を出力する。

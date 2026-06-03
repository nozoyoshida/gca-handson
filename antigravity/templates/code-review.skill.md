# /code-review — セキュリティ重視のコードレビュー（コードレビュー Skill 雛形）

> Antigravity の Skill 定義。Ch.2 でこの内容を `.agents/skills/code-review.md` に
> コピーして使います。ファイル先頭に以下の Frontmatter（`name: code-review` /
> `description: ...`）を置くと、自動的に `/code-review` スラッシュコマンドとして
> 登録されます。
>
> ```yaml
> ---
> name: code-review
> description: セキュリティ重視のコードレビュー（差分を規約とセキュリティ基準で点検）
> ---
> ```

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

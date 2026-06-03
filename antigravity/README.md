# Antigravity ハンズオン（Cloud Workstations + Antigravity CLI）

Google Cloud（**Gemini Enterprise Agent Platform**）認証のもと、**Cloud Workstations のブラウザ IDE** 上で **Antigravity CLI** を使ってお問い合わせ管理 API を実装し、**Cloud Run** へデプロイする実践ハンズオンです。ローカルには何もインストールしません。

> Gemini Code Assist（ローカル VSCode）版は [`../gca/`](../gca/) にあります。

## 概要

| 項目 | 内容 |
|------|------|
| 所要時間 | 90分 |
| 対象者 | 中級 |
| 環境 | Cloud Workstations（ブラウザ IDE）+ Antigravity CLI |
| 認証 | Google Cloud / Gemini Enterprise Agent Platform |
| 題材 | お問い合わせ管理 API（Flask + SQLite） |

## ハンズオンガイド

**[ハンズオンガイドを開く](https://nozoyoshida.github.io/gca-handson/antigravity/docs/handson-guide.html)**

**[Antigravity CLI リファレンス（日本語要約）](https://nozoyoshida.github.io/gca-handson/antigravity/docs/cli/index.html)** — 公式 CLI ドキュメント（`agy`）の日本語まとめ＋ハンズオン活用ポイント＋追加ネタ

## ディレクトリ構成

```
starter/          参加者が最初に使うコード（脆弱性入り）← ワークステーションでこのフォルダを開く
templates/        演習中にコピーするテンプレート（AGENTS.md / コードレビュー Workflow）
completed/        全演習完了後のリファレンス（Cloud Run 対応込み）
docs/             ハンズオンガイド（HTML）
slides/           プレゼンター用資料
```

## 前提

- 管理者が **Gemini Enterprise Agent Platform** と **Cloud Workstations** を有効化済み（ガイドの「附録 A: 管理者セットアップ」参照）
- 各受講者に Cloud Workstation が割り当て済み（または作成権限あり）
- Chrome ブラウザ

## 注意（要検証）

Antigravity 2.0 / Gemini Enterprise Agent Platform は新しい製品です。**CLI の導入コマンド・認証フラグ・`.agents/` のパス・モデル名などの具体値は、実施前に公式ドキュメントで最新の手順を確認**してください。ガイド本文の該当箇所にも注記しています。

## ワークショップ構成

| Chapter | 内容 | 時間 |
|---------|------|------|
| Ch.0 | 環境準備（ワークステーション起動・CLI 認証・アプリ起動） | 15分 |
| Ch.1 | Antigravity CLI の基本（計画→承認→実行→検証） | 10分 |
| Ch.2 | Context Engineering（AGENTS.md / Workflows） | 16分 |
| Ch.3 | Agentic Coding（対応履歴機能の実装） | 16分 |
| Ch.4 | セキュア開発（検出・修正・ルール化） | 13分 |
| Ch.5 | Cloud Run デプロイ | 16分 |
| Wrap-up | まとめ・次のステップ | 4分 |

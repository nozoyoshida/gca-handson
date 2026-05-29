# Gemini Code Assist ハンズオン

Context Engineering / Agentic Coding / Secure Development / Cloud Run デプロイ を軸にした、Gemini Code Assist の実践ハンズオンです。ローカルの VSCode + Gemini Code Assist 拡張で進めます。

> Antigravity（Cloud Workstations + CLI）版は [`../antigravity/`](../antigravity/) にあります。

## 概要

| 項目 | 内容 |
|------|------|
| 所要時間 | 90分 |
| 対象者 | 中級 |
| 環境 | ローカル VSCode + Python |
| 題材 | お問い合わせ管理 API（Flask + SQLite） |

## ハンズオンガイド

参加者向けのステップバイステップガイドは以下で公開しています：

**[ハンズオンガイドを開く](https://nozoyoshida.github.io/gca-handson/gca/docs/handson-guide.html)**

## ディレクトリ構成

```
starter/          参加者が最初に使うコード（脆弱性入り）← VSCode でこのフォルダを開く
templates/        演習中にコピーするテンプレート（GEMINI.md, styleguide.md）
completed/        全演習完了後のリファレンスコード（Cloud Run 対応込み）
docs/             ハンズオンガイド（HTML）
slides/           プレゼンター用資料
```

## 事前準備

1. VSCode をインストール
2. [Gemini Code Assist 拡張機能](https://marketplace.visualstudio.com/items?itemName=Google.gca)をインストールしてログイン
3. Python 3.9 以上をインストール
4. （Ch.5 用）`gcloud` CLI と、課金が有効な Google Cloud プロジェクト

## クイックスタート

### 1. clone して VSCode で開く

```bash
git clone https://github.com/nozoyoshida/gca-handson.git
```

> **重要**: VSCode の **File → Open Folder** で **`gca-handson/gca/starter/`** フォルダを開いてください（リポジトリのルートや `gca/` ではありません）。GEMINI.md はワークスペースルートから読み込まれるため、開くフォルダを間違えると Ch.2 以降の演習が正しく機能しません。

以降のコマンドは **VSCode の統合ターミナル**（Ctrl+`` ` ``）で実行してください。`gca/starter/` を開いているので、ターミナルは最初からそこにいます。

### 2. 仮想環境のセットアップ

#### venv を使う場合

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

#### uv を使う場合

```bash
uv venv && uv pip install -r requirements.txt
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 3. 起動

```bash
python app.py
```

http://localhost:5000 で GUI、http://localhost:5000/tickets で API にアクセスできます。

## ワークショップ構成

| Chapter | 内容 | 時間 |
|---------|------|------|
| Ch.0 | セットアップ確認 | 5分 |
| Ch.1 | 基本操作（Tab補完 / チャット / インラインチャット） | 12分 |
| Ch.2 | Context Engineering（GEMINI.md / styleguide.md） | 18分 |
| Ch.3 | Agentic Coding（Agent モードで機能追加） | 20分 |
| Ch.4 | セキュア開発（脆弱性検出・修正・ルール化） | 15分 |
| Ch.5 | Cloud Run デプロイ（本番化・デプロイ・確認） | 15分 |
| Wrap-up | まとめ・次のステップ | 5分 |

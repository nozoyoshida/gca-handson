# Gemini Code Assist ハンズオン

Context Engineering / Agentic Coding / Secure Development を軸にした、Gemini Code Assist の実践ハンズオンです。

## 概要

| 項目 | 内容 |
|------|------|
| 所要時間 | 60分 |
| 対象者 | 中級 |
| 環境 | ローカル VSCode + Python |
| 題材 | お問い合わせ管理 API（Flask + SQLite） |

## ハンズオンガイド

参加者向けのステップバイステップガイドは以下で公開しています：

**[ハンズオンガイドを開く](https://nozoyoshida.github.io/gca-handson/handson-guide.html)**

## ディレクトリ構成

```
starter/          参加者が最初に使うコード（脆弱性入り）
templates/        演習中にコピーするテンプレート（GEMINI.md, styleguide.md）
completed/        全演習完了後のリファレンスコード
docs/             ハンズオンガイド（HTML）
slides/           プレゼンター用資料
```

## 事前準備

1. VSCode をインストール
2. [Gemini Code Assist 拡張機能](https://marketplace.visualstudio.com/items?itemName=Google.gca)をインストールしてログイン
3. Python 3.9 以上をインストール

## クイックスタート

### venv を使う場合

```bash
git clone https://github.com/nozoyoshida/gca-handson.git
cd gca-handson/starter/
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### uv を使う場合

```bash
git clone https://github.com/nozoyoshida/gca-handson.git
cd gca-handson/starter/
uv venv && uv pip install -r requirements.txt
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python app.py
```

http://localhost:5000 で GUI、http://localhost:5000/tickets で API にアクセスできます。

## ワークショップ構成

| Chapter | 内容 | 時間 |
|---------|------|------|
| Ch.0 | セットアップ確認 | 2分 |
| Ch.1 | 基本操作（Tab補完 / チャット / インラインチャット） | 10分 |
| Ch.2 | Context Engineering（GEMINI.md / styleguide.md） | 15分 |
| Ch.3 | Agentic Coding（Agent モードで機能追加） | 18分 |
| Ch.4 | セキュア開発（脆弱性検出・修正・ルール化） | 13分 |
| Wrap-up | まとめ・次のステップ | 2分 |

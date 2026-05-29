# AI 駆動開発 ハンズオン（お問い合わせ管理システム）

同じ題材（お問い合わせ管理 API / Flask + SQLite）を、2 種類の AI 開発ツールで実践するハンズオン集です。どちらも **Cloud Run へのデプロイまで**を含む約 90 分の構成です。

| 版 | ツール / 環境 | フォルダ |
|----|------------|---------|
| **Gemini Code Assist 版** | ローカル VSCode + GCA 拡張 | [`gca/`](gca/) |
| **Antigravity 版** | Cloud Workstations（ブラウザ IDE）+ Antigravity CLI（認証: Gemini Enterprise Agent Platform） | [`antigravity/`](antigravity/) |

両版とも、基本操作 → Context Engineering → Agentic Coding → セキュア開発 → **Cloud Run デプロイ** という流れで、「実装から出荷まで」を AI と一気通貫で体験します。

## ハンズオンガイド（公開ページ）

- **Gemini Code Assist 版**: https://nozoyoshida.github.io/gca-handson/gca/docs/handson-guide.html
- **Antigravity 版**: https://nozoyoshida.github.io/gca-handson/antigravity/docs/handson-guide.html

> **GitHub Pages 設定**: このリポジトリは2版構成のため、Pages の配信元を **main ブランチの `/`（ルート）** に設定してください（Settings → Pages → Source）。ルートの [`index.html`](index.html) が両版へのランディングになります。

## どちらを選ぶ？

- **Gemini Code Assist 版** … 手元の VSCode で、補完・チャット・Agent モードといった「補助的な AI」を使う日常的な開発スタイルを体験したい場合。
- **Antigravity 版** … Google Cloud（Gemini Enterprise Agent Platform）認証のもと、Cloud Workstations 上で「エージェントファースト」の CLI 開発を体験したい場合。

各版の詳しい進め方は、それぞれのフォルダの README を参照してください。

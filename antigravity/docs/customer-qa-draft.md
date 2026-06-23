# お客様 Q&A ドラフト（Antigravity の差別化）

---

## 質問① Browser in the loop とは何か / Playwright との違い

Antigravity の「Browser in the loop」は、**Browser Subagent** という組み込み機能を指しています。

**ポイント: テストコードを書くツールではなく、エージェントが自らブラウザを操作する仕組み**

Claude Code や GitHub Copilot でも Playwright のテストコードを生成できますが、Antigravity の Browser Subagent はアプローチが根本的に異なります。

| | Playwright / Claude Code | Antigravity Browser Subagent |
|---|---|---|
| やること | テスト**コード**を書く・実行する | エージェントが**ブラウザを直接操作**する |
| 検証方法 | スクリプトベース（事前にシナリオを定義） | ゴールベース（「ログインフォームが動くか確認して」と自然言語で指示） |
| 利用タイミング | テスト工程 | **開発中にリアルタイムで検証**（コード変更→ブラウザ確認のループが一体化） |
| 成果物 | テストスクリプト | スクリーンショット・アクション録画（Artifacts として保存） |

具体的には、Antigravity のエージェントは Chromium を起動し、スクリーンショット撮影・DOM 解析・クリック・テキスト入力を自律的に行い、UI が期待通りに動作するか視覚的に検証します。テストスクリプトを書くステップ自体をスキップし、**開発→検証のフィードバックループを一体化**できる点が、他のコーディングツールにはない Antigravity 固有の強みです。

なお、Playwright と Browser Subagent は**排他的ではなく補完的**です。Browser Subagent で素早く視覚検証しつつ、本格的な E2E テストには Playwright MCP を Antigravity に接続して使う、という組み合わせも可能です（Google Codelabs にチュートリアルあり）。

**参考リンク:**
- [Browser Subagent — Antigravity 公式ドキュメント](https://antigravity.google/docs/browser-subagent)
- [Browser Tools — Antigravity 公式ドキュメント](https://antigravity.google/docs/browser)
- [Automate UI Testing with Gemini CLI, BrowserMCP and Playwright — Google Codelabs](https://codelabs.developers.google.com/agentic-ui-testing)
- [Build with Google Antigravity — Google Developers Blog](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/)

---

## 質問② Antigravity 経由の Gemini vs GitHub Copilot 経由の Gemini

**ポイント: 同じ Gemini モデルでも「プラットフォームの深さ」が根本的に異なる**

GitHub Copilot で Gemini を選ぶのは「モデルを借りる」こと。Antigravity で Gemini を使うのは「Google Cloud のエージェントプラットフォーム全体を使う」ことです。

| 観点 | GitHub Copilot + Gemini | Antigravity + Gemini |
|---|---|---|
| モデルの位置づけ | 複数モデルの 1 つとして選択可能 | Gemini ファースト設計（最新モデルに最速対応） |
| マルチモデル | GPT, Claude, Gemini, Grok 等 | Gemini + **Model Garden** 経由で Claude, Grok 等も利用可能 |
| エージェント機能 | Agent Mode（VS Code 内） | 並列マルチエージェント + **Browser Subagent** |
| Google Cloud 統合 | なし | **GEAP 統合**（Cloud OAuth、VPC SC、データ境界） |
| ガバナンス | GitHub Enterprise 監査ログ、SOC2/ISO27001 | Agent Identity / Gateway / Registry + **Model Armor** |
| データ境界 | Microsoft/GitHub のインフラ | Google Cloud 境界内で推論（顧客テレメトリは外部に非保存） |
| 開発体験 | VS Code 拡張が中心 | デスクトップ + CLI + SDK + Managed Agents API（設定・スキルを共有） |

### エンタープライズ観点での 3 つの差別化

**1. GEAP（Gemini Enterprise Agent Platform）統合**
Cloud OAuth でログインし、Project ID と Region を指定するだけで、全推論がお客様の Google Cloud 境界内で実行されます。VPC Service Controls にも対応しており、既存の Google Cloud セキュリティポリシーをそのまま適用できます。

**2. Model Armor**
LLM の入出力をリアルタイムでスクリーニングします。プロンプトインジェクション検出、PII マスキング（Cloud DLP 連携で 150 種類以上）、有害コンテンツフィルタリング、マルウェア・不正 URL 検出が含まれます。

**3. Model Garden によるマルチモデル対応**
GEAP 経由で Claude（Opus 4.8, Sonnet 4.6, Fable 5）、Grok（4.3, 4.20）等のパートナーモデルも Google Cloud のガバナンス基盤上で統一管理しながら利用できます。GitHub Copilot もマルチモデル対応ですが、Google Cloud のデータ境界・ガバナンスの中で使える点が異なります。

**参考リンク:**
- [Gemini Enterprise Agent Platform — Google Cloud](https://cloud.google.com/products/gemini-enterprise-agent-platform)
- [I/O '26 news for agent developers — Google Cloud Blog](https://cloud.google.com/blog/topics/developers-practitioners/io26-news-for-agent-developers-on-google-cloud)
- [Model Garden — Partner Models](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/use-partner-models)
- [Model Armor — Google Cloud](https://cloud.google.com/security/products/model-armor)
- [Antigravity 公式サイト](https://antigravity.google/)

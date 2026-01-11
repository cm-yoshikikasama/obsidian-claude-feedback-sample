# Obsidian Vault - 個人ナレッジ管理システム

日本語と英語で整理されたマークダウンノートを含む個人のObsidianボルトです。

## プロジェクト概要

- Obsidianボルト - 構造化されたマークダウンノートシステム
- 音声・動画 → テキスト変換 - AI を使用した文字起こしツール
- Google Calendar連携 - 今日の予定取得ツール
- 議事録自動生成 - 音声ファイルから議事録を自動作成
- マークダウンフォーマット - Prettierを使用したファイル統一フォーマット
- Obsidian Base プラグイン - データベースライクなビュー管理（Base.base設定ファイル）

## ディレクトリ構造

```text
├── 00_Configs/           # 設定ファイル・テンプレート
│   ├── Extra/            # 追加設定
│   └── Templates/        # Obsidianテンプレート（Daily.md等）
├── 01_Daily/             # 日次ノート・デイリーログ
├── 02_Monthly/           # 月次まとめとAIレビュー
├── 03_RoughNotes/        # ラフメモ・一時的なノート
├── 04_EngStudy/         # 英語学習資料・フィードバック
├── 05_Meetings/          # 会議ノート・議事録
├── 06_Clippings/         # ウェブクリッピング・保存記事
├── Base.base             # Obsidian Base プラグイン設定
├── CLAUDE.md             # Claude Code 設定・プロジェクト指示
├── README.md             # このファイル
├── package.json          # Node.js依存関係（Prettier）
└── .claude/              # Claude Code設定・ツール群
    ├── skills/              # カスタムスキル（スラッシュコマンド）
    │   ├── scripts/             # 共有スクリプト（skill以外）
    │   │   ├── audio_video_to_text/  # AI音声・動画文字起こしツール
    │   │   │   ├── input/           # 変換元ファイル格納
    │   │   │   └── output/          # 変換結果テキスト出力
    │   │   └── today_calendar/      # Google Calendar API連携ツール
    │   ├── commit-msg/          # Gitコミットメッセージ生成
    │   ├── daily-morning/       # 朝のDaily作成
    │   ├── daily-evening/       # 夜のDaily更新
    │   ├── english-lesson/      # 英語レッスンフィードバック
    │   ├── meeting-minutes/     # 議事録自動生成
    │   └── monthly-review/      # 月次KPT形式まとめ
    ├── requirements.txt     # Python依存関係
    └── settings.json       # Claude Code設定
```

## クイックスタート

1. セットアップ手順を上から順番に実行
2. Obsidianアプリケーションでこのディレクトリをボルトとして開く
3. Claude Code でカスタムコマンドを使用してノートを作成・管理

## セットアップ手順

上から順番に実行

### 必要な環境

- uv（Python パッケージマネージャー）
- Node.js（Prettierフォーマット用）
- FFmpeg（動画変換用）
- Google Cloud Platform アカウント

#### 1. uv のインストール

uv は Python バージョン管理、仮想環境、パッケージ管理を一括で行えます。

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 2. Node.js と FFmpeg のインストール

```bash
# macOS の場合
brew install node ffmpeg

# または個別にインストール
# Node.js: https://nodejs.org/ からダウンロード
# FFmpeg: https://ffmpeg.org/download.html からダウンロード

# プロジェクトルートで依存関係をインストール
npm install
```

#### 3. Python 依存関係のインストール

```bash
# .claude ディレクトリに移動
cd .claude

# 仮想環境作成とPython 3.13インストール
uv venv --python 3.13
source .venv/bin/activate  # macOS/Linux
uv pip install -r requirements.txt
```

#### 4. Google Cloud Platform 設定

音声・動画文字起こし用

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
1. 新しいプロジェクト作成 or 既存プロジェクト選択
1. APIs & Services → Library → Vertex AI API を検索して有効化
1. サービスアカウントキーを作成・ダウンロード

#### 5. Google Calendar API 設定

カレンダー連携用

1. APIs & Services → Library → Google Calendar API を検索して有効化
1. OAuth consent screen を設定（Internal または External）
1. Credentials → Create Credentials → OAuth 2.0 Client IDs
1. Application type - Desktop application
1. `cal_client_secret.json` をダウンロードし `.claude/skills/scripts/today_calendar/` に配置

#### 6. 環境変数の設定

`.claude/skills/scripts/audio_video_to_text/`ディレクトリに`.env`ファイルを作成

```env
PROJECT_ID=your-gcp-project-id
GOOGLE_CREDENTIALS_JSON=path/to/your/service-account-key.json
```

#### 7. 環境変数のカスタマイズ

デイリーノートで使用するプロジェクト名と目標を自分の環境に合わせて設定

1. `.claude/skills/daily-morning/SKILL.md` を開く
1. 以下の環境変数セクションを編集

    ```txt
    ## 環境変数

    PROJECT_A = "あなたのプロジェクト名A"
    PROJECT_B = "あなたのプロジェクト名B"
    PROJECT_C = "あなたのプロジェクト名C"
    GOAL_1 = "あなたの目標1"
    GOAL_2 = "あなたの目標2"
    GOAL_3 = "あなたの目標3"
    ```

1. 以下のスキルファイルも同様に編集
    - `.claude/skills/daily-evening/SKILL.md`
    - `.claude/skills/monthly-review/SKILL.md`

これらの変数は、スキル実行時のテンプレートで自動的に使用されます。

## 使用方法

### 1. 音声・動画文字起こし

1. `.claude/skills/scripts/audio_video_to_text/input/` に MP3/MP4/M4A ファイルを配置
2. スラッシュコマンドで実行（後述）

変換されたテキストは `.claude/skills/scripts/audio_video_to_text/output/` に保存されます。

### 2. Google Calendar 連携

```bash
# 今日の予定を表示
cd .claude/skills/scripts/today_calendar
uv run today-calendar.py
```

初回実行時はブラウザでGoogle認証が必要です。

### 3. マークダウンフォーマット

```bash
# すべてのマークダウンファイルをフォーマット
npm run format
```

Claude Code使用時は自動でフォーマットされます。

## Claude Code カスタムスキル

`.claude/skills/` ディレクトリには Claude Code で使用するカスタムスキル（スラッシュコマンド）が含まれています

### タスクステータス管理システム

デイリーノートでは以下の5段階ステータス管理を採用

- `[ ]` 未着手（無色） - まだ開始していないタスク
- `[/]` 進行中（オレンジ⏵） - 現在作業中のタスク
- `[R]` レビュー中（青R） - 完了したがレビュー・承認待ちのタスク
- `[x]` 完了（緑✓） - 完全に完了したタスク

中止したタスクは打ち消し線（~~タスク名~~）で表現します。

### 利用可能なスキル

- `/daily-morning [YYYY-MM-DD]` - 朝のDaily Note作成アシスタント
    - 前日のDaily Noteから「明日やる」タスクを引き継ぎ
    - Google Calendarから今日の予定を取得
    - 新しいDaily Noteファイルを自動作成
    - 引数省略時は今日の日付を使用
- `/daily-evening [YYYY-MM-DD]` - 夜のDaily Note更新アシスタント
    - 今日のタスク進捗を一括確認・更新（5段階ステータス管理対応）
    - 目標に沿った振り返りを追加（カスタマイズ可能）
    - 明日のタスクを計画
    - 引数省略時は今日の日付を使用
- `/english-lesson [YYYY-MM-DD]` - 英会話レッスンフィードバック生成
    - 音声ファイルの文字起こし実行
    - レッスン内容の分析とフィードバック生成
    - 文法・表現の改善点を具体的に提案
    - 04_EngStudyフォルダに日付付きで自動保存
    - 引数省略時は今日の日付を使用
- `/meeting-minutes [YYYY-MM-DD] [会議名]` - 議事録自動生成
    - 音声ファイルの文字起こし実行
    - 文字起こしテキストから詳細な議事録を生成
    - 会議概要、報告事項、討議事項、決定事項、アクションアイテムを整理
    - 05_Meetingsフォルダに日付付きで自動保存
    - 引数省略時は今日の日付を使用、会議名はユーザーに確認
- `/commit-msg` - Gitコミットメッセージ生成
    - git statusとdiffから変更内容を分析
    - 最近のコミットスタイルを参考に
    - 規約に沿ったコミットメッセージを自動生成
- `/monthly-review [YYYY-MM]` - 月次KPT形式まとめ生成
    - デイリーノートから指定期間の活動を分析
    - 案件別の実績（完了タスク・MTG参加）を記録
    - 目標達成状況をKPT形式でまとめ
    - 定量的な実績を集計
    - 02_Monthlyフォルダにレビューファイルを作成
    - 引数省略時は実行月を使用

### スキル実行例

Claude Code で以下のようにスキルを実行

```bash
# 朝のDaily Note作成（引数省略時は今日）
/daily-morning
/daily-morning 2026-01-15

# 夜のDaily Note更新（引数省略時は今日）
/daily-evening
/daily-evening 2026-01-15

# 英語レッスンフィードバック生成（引数省略時は今日）
/english-lesson
/english-lesson 2026-01-15

# 議事録自動生成（引数省略時は今日、会議名はユーザーに確認）
/meeting-minutes
/meeting-minutes 2026-01-15 週次定例会議

# Gitコミットメッセージ生成
/commit-msg

# 月次まとめ生成（引数省略時は実行月）
/monthly-review
/monthly-review 2025-12
```

# Obsidian Vault - 個人ナレッジ管理システム

日本語と英語で整理されたマークダウンノートを含む個人のObsidianボルトです。

## プロジェクト概要

- **Obsidianボルト**: 構造化されたマークダウンノートシステム
- **音声・動画 → テキスト変換**: AI を使用した文字起こしツール
- **Google Calendar連携**: 今日の予定取得ツール
- **議事録自動生成**: 音声ファイルから議事録を自動作成
- **マークダウンフォーマット**: Prettierを使用したファイル統一フォーマット
- **Obsidian Base プラグイン**: データベースライクなビュー管理（Base.base設定ファイル）

## ディレクトリ構造

```text
├── 00_Configs/           # 設定ファイル・テンプレート
│   ├── Extra/            # 追加設定
│   └── Templates/        # Obsidianテンプレート（Daily.md等）
├── 01_Daily/             # 日次ノート・デイリーログ
├── 02_Weekly/            # 週次まとめとAIレビュー
├── 03_RoughNotes/        # ラフメモ・一時的なノート
├── 04_EngStudy/         # 英語学習資料・フィードバック
├── 05_Meetings/          # 会議ノート・議事録
├── 06_Clippings/         # ウェブクリッピング・保存記事
├── Base.base             # Obsidian Base プラグイン設定
├── CLAUDE.md             # Claude Code 設定・プロジェクト指示
├── README.md             # このファイル
├── package.json          # Node.js依存関係（Prettier）
└── .claude/              # Claude Code設定・ツール群
    ├── audio_video_to_text/  # AI音声・動画文字起こしツール
    │   ├── input/           # 変換元ファイル格納
    │   └── output/          # 変換結果テキスト出力
    ├── today_cal/           # Google Calendar API連携ツール
    ├── commands/            # カスタムスラッシュコマンド
    │   ├── daily-morning.md    # 朝のDaily作成
    │   ├── daily-evening.md    # 夜のDaily更新
    │   ├── english-lesson.md   # 英語レッスンフィードバック
    │   ├── meeting-minutes.md  # 議事録自動生成
    │   ├── commit-message.md   # Gitコミットメッセージ生成
    │   └── weekly-review.md    # 週次まとめとAIレビュー
    ├── requirements.txt     # Python依存関係
    └── settings.json       # Claude Code設定
```

## クイックスタート

1. **セットアップ手順**を上から順番に実行
2. **Obsidianアプリケーション**でこのディレクトリをボルトとして開く
3. Claude Code で**カスタムコマンド**を使用してノートを作成・管理

## セットアップ手順

上から順番に実行してください。

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

音声・動画文字起こし用：

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 新しいプロジェクト作成 or 既存プロジェクト選択
3. **APIs & Services** → **Library** → **Vertex AI API** を検索して有効化
4. サービスアカウントキーを作成・ダウンロード

#### 5. Google Calendar API 設定

カレンダー連携用：

1. **APIs & Services** → **Library** → **Google Calendar API** を検索して有効化
2. **OAuth consent screen** を設定（Internal または External）
3. **Credentials** → **Create Credentials** → **OAuth 2.0 Client IDs**
4. Application type: **Desktop application**
5. `cal_client_secret.json` をダウンロードし `.claude/` に配置

#### 6. 環境変数の設定

`.claude/audio_video_to_text/`ディレクトリに`.env`ファイルを作成:

```env
PROJECT_ID=your-gcp-project-id
REGION=your-region
FILE_NAME=audio
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json
```

## 使用方法

### 1. 音声・動画文字起こし

```bash
# 1. 音声・動画ファイルを配置
# .claude/audio_video_to_text/input/ に MP3 または MP4 ファイルを配置

# 2. .env ファイルの FILE_NAME を設定（拡張子なし）
# 例: FILE_NAME=meeting

# 3. 文字起こし実行
cd .claude
uv run audio_video_to_text/audio_video_to_text.py
```

変換されたテキストは `.claude/audio_video_to_text/output/` に保存されます。

### 2. Google Calendar 連携

```bash
# 今日の予定を表示
cd .claude
uv run today_cal/today-calendar.py
```

初回実行時はブラウザでGoogle認証が必要です。

### 3. マークダウンフォーマット

```bash
# すべてのマークダウンファイルをフォーマット
npm run format
```

Claude Code使用時は自動でフォーマットされます。

## Claude Code カスタムコマンド

`.claude/commands/` ディレクトリには Claude Code で使用するカスタムコマンド（スラッシュコマンド）が含まれています：

### タスクステータス管理システム

デイリーノートでは以下の5段階ステータス管理を採用：

- `[ ]` **未着手** - まだ開始していないタスク
- `[/]` **進行中** - 現在作業中のタスク
- `[R]` **レビュー中** - 完了したがレビュー・承認待ちのタスク
- `[x]` **完了** - 完全に完了したタスク
- `[-]` **中止** - キャンセルまたは延期されたタスク

### 利用可能なコマンド

- **`/daily-morning`**: 朝のDaily Note作成アシスタント
    - 前日のDaily Noteから「明日やる」タスクを引き継ぎ
    - Google Calendarから今日の予定を取得
    - 新しいDaily Noteファイルを自動作成

- **`/daily-evening`**: 夜のDaily Note更新アシスタント
    - 今日のタスク進捗を一括確認・更新（5段階ステータス管理対応）
    - 目標に沿った振り返りを追加（カスタマイズ可能）
    - 明日のタスクを計画

- **`/english-lesson [date]`**: 英会話レッスンフィードバック生成（日付引数対応）
    - 音声ファイルの文字起こし実行
    - レッスン内容の分析とフィードバック生成
    - 文法・表現の改善点を具体的に提案
    - 04_EngStudyフォルダに日付付きで自動保存

- **`/meeting-minutes [date]`**: 議事録自動生成（日付引数対応）
    - 音声ファイルの文字起こし実行
    - 文字起こしテキストから詳細な議事録を生成
    - 会議概要、報告事項、討議事項、決定事項、アクションアイテムを整理
    - 05_Meetingsフォルダに日付付きで自動保存

- **`/commit-message`**: Gitコミットメッセージ生成
    - git statusとdiffから変更内容を分析
    - 最近のコミットスタイルを参考に
    - 規約に沿ったコミットメッセージを自動生成

- **`/weekly-review [monday-date]`**: 週次まとめとAIレビュー生成
    - デイリーノートから1週間分（月〜金）の活動を分析
    - プロジェクト別の成果をまとめ
    - AI による生産性分析とフィードバック提供
    - 改善提案と来週への推奨事項を生成
    - 02_Weeklyフォルダに週次レビューファイルを作成

### コマンド実行例

Claude Code で以下のようにコマンドを実行：

```bash
# 朝のDaily Note作成（日付省略時は今日）
/daily-morning [yyyy-mm-dd]

# 夜のDaily Note更新（日付省略時は今日）
/daily-evening [yyyy-mm-dd]

# 英語レッスンフィードバック生成（日付引数対応）
/english-lesson [yyyy-mm-dd]

# 議事録自動生成（日付引数対応）
/meeting-minutes [yyyy-mm-dd]

# Gitコミットメッセージ生成
/commit-message

# 週次まとめとAIレビュー生成（月曜日の日付を指定）
/weekly-review [yyyy-mm-dd]
```

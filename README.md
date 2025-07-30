# Obsidian Vault - 個人ナレッジ管理システム

日本語と英語で整理されたマークダウンノートを含む個人のObsidianボルトです。

## プロジェクト概要

- **Obsidianボルト**: 構造化されたマークダウンノートシステム
- **音声・動画 → テキスト変換**: AI を使用した文字起こしツール
- **Google Calendar連携**: 今日の予定取得ツール
- **議事録自動生成**: 音声ファイルから議事録を自動作成
- **マークダウンフォーマット**: Prettierを使用したファイル統一フォーマット

## ディレクトリ構造

```text
├── 00_Configs/           # 設定ファイル・テンプレート
│   ├── Extra/            # 追加設定
│   └── Templates/        # Obsidianテンプレート（Daily.md等）
├── 01_Daily/             # 日次ノート・デイリーログ
├── 02_Inbox/             # 一時ノート・リサーチ資料
├── 03_eng_study/         # 英語学習資料・フィードバック
├── 04_Meetings/          # 会議ノート・議事録
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
    │   └── meeting-minutes.md  # 議事録自動生成
    ├── requirements.txt     # Python依存関係
    └── settings.json       # Claude Code設定
```

## クイックスタート

### 1. Obsidianボルトとして使用

1. **Obsidianアプリケーション**をインストール
2. このリポジトリをObsidianでボルトとして開く
3. `00_Configs/Templates/`のテンプレートを使用してノートを作成

### 2. 音声・動画文字起こし

1. 音声・動画ファイルを`.claude/audio_video_to_text/input/`に配置
2. `.env`ファイルで`FILE_NAME`を設定
3. `uv run audio_video_to_text/audio_video_to_text.py`で実行

### 3. Claude Codeカスタムコマンド

- `/daily-morning`: 朝のDaily Note作成
- `/daily-evening`: 夜のDaily Note更新
- `/english-lesson`: 英語レッスンフィードバック
- `/meeting-minutes`: 議事録自動生成

## セットアップ

### 依存関係のインストール

```bash
cd .claude
uv venv --python 3.13
source .venv/bin/activate  # macOS/Linux
uv pip install -r requirements.txt
```

### 必要な環境

- uv（Python パッケージマネージャー）
- FFmpeg（動画変換用）
- Google Cloud Platform アカウント
- Node.js（Prettierフォーマット用）

### セットアップ手順

#### 1. uv のインストール

uv は Python バージョン管理、仮想環境、パッケージ管理を一括で行えます。

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 2. 依存関係のインストール

```bash
# プロジェクトのルートディレクトリに移動
cd .claude

# 仮想環境作成とPython 3.13インストール
uv venv --python 3.13
source .venv/bin/activate  # macOS/Linux
uv pip install -r requirements.txt
```

#### 3. 環境変数の設定

`.claude/audio_video_to_text/`ディレクトリに`.env`ファイルを作成:

```env
PROJECT_ID=your-gcp-project-id
REGION=your-region
FILE_NAME=audio
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json
```

### 使用方法

1. `.claude/audio_video_to_text/input/` フォルダに変換したい MP3 または MP4 ファイルを配置
2. `.env` ファイルの `FILE_NAME` をファイル名（拡張子なし）に設定
3. スクリプトを実行:

```bash
cd .claude
uv run audio_video_to_text/audio_video_to_text.py
```

変換されたテキストは `.claude/audio_video_to_text/output/` フォルダに保存されます。

#### 対応ファイル形式

- **MP3**: そのまま文字起こし
- **MP4**: 自動的にMP3に変換してから文字起こし

#### フォルダ構成

```text
.claude/audio_video_to_text/
├── audio_video_to_text.py  # メイン実行スクリプト
├── .env                    # 環境変数設定
├── input/                  # 変換元ファイル格納
│   ├── audio.mp3          # MP3音声ファイル
│   └── video.mp4          # MP4動画ファイル
└── output/                # 変換結果出力
    └── audio_transcript.txt  # 文字起こし結果
```

#### 注意事項

- Google Cloud Platform の認証情報が必要です
- Vertex AI の使用には課金が発生する可能性があります
- MP4ファイルの変換にはFFmpegが必要です
- 大きなファイルの場合、処理に時間がかかる場合があります
- `uv run`コマンドが自動で仮想環境を管理します

## 開発環境のセットアップ

### 前提条件

- Node.js（Prettierフォーマット用）
- Obsidianアプリケーション

### Prettierのインストール（マークダウンフォーマット用）

このプロジェクトには、マークダウンの統一フォーマットを維持するためのPrettierを使用するスクリプトが含まれています。

#### インストール手順

1. **Node.jsのインストール**（まだインストールされていない場合）：
    - [nodejs.org](https://nodejs.org/)からダウンロード
    - またはパッケージマネージャーでインストール（例：macOSでは`brew install node`）

2. **依存関係のインストール**：

```bash
npm install
npm list
```

#### フォーマットの実行

```bash
# すべてのマークダウンファイルをフォーマット
npm run format

# 特定のファイルをフォーマット
echo '{"tool_input":{"file_path":"path/to/file.md"}}' | .claude/format-md.sh
```

### フォーマットスクリプト

- `.claude/format-md.sh`: Claude Codeが使用する自動マークダウンフォーマットスクリプト
- PrettierがインストールされてPATHで利用可能である必要があります

※ formatterが機能しているかはclaude --debugで確認できる。

## Google Calendar 今日の予定取得ツール

Google Calendar APIを使用して今日の予定を取得するPythonスクリプトです。

### セットアップ

#### 1. uvを使用した実行

`.claude`ディレクトリで`uv run`を使用します：

#### 2. Google Cloud Console設定

1. https://console.cloud.google.com/ にアクセス
2. 新しいプロジェクト作成 or 既存プロジェクト選択
3. **APIs & Services** → **Library**
4. **Google Calendar API** を検索して有効化

##### OAuth同意画面の設定（必須）

5. **APIs & Services** → **OAuth consent screen**
6. **Internal**（会社アカウントの場合）または **External**（個人アカウントの場合）を選択して **CREATE**
7. **App Information** を入力：
    - **App name**: 任意の名前（例：Calendar Reader）
    - **User support email**: 自分のメールアドレス
8. **SAVE AND CONTINUE**
9. **Audience**: **Internal**（会社）または **External**（個人）を選択
10. **SAVE AND CONTINUE**
11. **Contact Information** を入力：
    - **Email addresses**: 自分のメールアドレス
12. **SAVE AND CONTINUE** を押して完了

##### OAuth Client IDの作成

10. **APIs & Services** → **Credentials** → **Create Credentials** → **OAuth 2.0 Client IDs**
11. Application typeを **Desktop application** に設定
12. 名前を適当に入力（例：Calendar Reader）
13. **Create** をクリック
14. `cal_client_secret.json` をダウンロード

#### 3. 認証情報の配置

ダウンロードした `cal_client_secret.json` を配置：

```
.claude/cal_client_secret.json
```

#### 4. 実行

```bash
cd .claude
uv run today_cal/today-calendar.py
```

初回実行時：

- ブラウザが自動で開く
- Googleアカウントでログイン
- 権限を許可
- `token.json` が自動作成される

2回目以降は認証不要で即座に実行される。

### 使用方法

```bash
# 今日の予定を表示
cd .claude
uv run today_cal/today-calendar.py
```

出力例：

```
10:30 - 会議
14:00 - プレゼン
終日 - 祝日
```

## Claude Code カスタムコマンド

`.claude/commands/` ディレクトリには Claude Code で使用するカスタムコマンド（スラッシュコマンド）が含まれています：

### 利用可能なコマンド

- **`/daily-morning`**: 朝のDaily Note作成アシスタント
    - 前日のDaily Noteから「明日やる」タスクを引き継ぎ
    - Google Calendarから今日の予定を取得
    - 新しいDaily Noteファイルを自動作成

- **`/daily-evening`**: 夜のDaily Note更新アシスタント
    - 今日の実績をプロジェクト別に記録
    - 振り返り（感謝・Good・Motto）を追加
    - 明日のタスクを計画

- **`/english-lesson`**: 英会話レッスンフィードバック生成（日付引数必須）
    - 音声ファイルの文字起こし実行
    - レッスン内容の分析とフィードバック生成
    - 文法・表現の改善点を具体的に提案
    - 03_eng_studyフォルダに日付付きで自動保存

- **`/meeting-minutes`**: 議事録自動生成（日付引数必須）
    - 音声ファイルの文字起こし実行
    - 文字起こしテキストから詳細な議事録を生成
    - 会議概要、報告事項、討議事項、決定事項、アクションアイテムを整理
    - 04_Meetingsフォルダに日付付きで自動保存

### 使用方法

Claude Code で以下のようにコマンドを実行：

```bash
# 朝のDaily Note作成
/daily-morning

# 夜のDaily Note更新
/daily-evening

# 英語レッスンフィードバック生成（日付引数が必要）
/english-lesson yyyy-mm-dd

# 議事録自動生成（日付引数が必要）
/meeting-minutes yyyy-mm-dd
```

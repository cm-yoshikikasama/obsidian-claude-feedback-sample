# Obsidian Vault - 個人ナレッジ管理システム

日本語と英語で整理されたマークダウンノートを含む個人のObsidianボルトです。

## プロジェクト概要

このリポジトリには以下の機能が含まれています：

- **Obsidianボルト**: 構造化されたマークダウンノートシステム
- **Audio/Video to Text Converter**: AI を使用した音声・動画ファイルのテキスト変換ツール
- **マークダウンフォーマット**: Prettierを使用したマークダウンファイルの統一フォーマット

## リポジトリ構造

```text
├── 00_Configs/           # 設定ファイルとテンプレート
├── 01_Daily/             # 日次ノートとログ
├── 02_Inbox/             # 一時的なノートとリサーチ資料
├── 03_eng_study/         # 英語学習資料
├── 04_Meetings/          # 会議ノートと議事録
├── audio_video_to_text/  # 音声・動画ファイルのテキスト変換ツール
└── .claude/              # Claude Code設定とスクリプト
```

## Obsidianボルトの使用方法

### 基本的な使用方法

1. **Obsidianアプリケーション**をインストール
2. このリポジトリをObsidianでボルトとして開く
3. 構造化テンプレートを使用してノートを作成

### テンプレートシステム

ボルトは統一されたノート作成のための構造化テンプレートを使用します。

- **Daily.md**: 日次ノート用テンプレート（MTG・イベント、Todo、振り返り、計画セクション）
- **English lesson.md**: 英語学習セッション用テンプレート

テンプレートは`00_Configs/Templates/`にあります。

## Audio/Video to Text Converter

Google Vertex AI の Gemini モデルを使用して MP3 音声ファイルや MP4 動画ファイルをテキストに変換するツールです。

### 機能

- MP3 音声ファイルの書き起こし
- MP4 動画ファイルの書き起こし（自動的にMP3に変換）
- 発言者の変わり目での改行
- 句読点の自動補完
- 日本語での出力

### 必要な環境

- uv（Python バージョン管理 + パッケージマネージャー）
- FFmpeg（MP4からMP3への変換用）
- Google Cloud Platform アカウント
- Vertex AI API の有効化

### セットアップ手順

#### 1. uv のインストール

uv は Python バージョン管理、仮想環境、パッケージ管理を一括で行えます。

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 2. 仮想環境の作成と依存関係のインストール

```bash
# プロジェクトディレクトリに移動
cd audio_video_to_text

# 仮想環境作成（Python 3.13を自動インストール）
uv venv --python 3.13

# 仮想環境の有効化
# macOS/Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate

# 依存関係のインストール
uv pip install -r requirements.txt
```

#### 3. 環境変数の設定

`audio_video_to_text/`ディレクトリに`.env`ファイルを作成:

```env
PROJECT_ID=your-gcp-project-id
REGION=your-region
FILE_NAME=audio.mp3
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json
```

### 使用方法

1. `audio_video_to_text/input/` フォルダに変換したい MP3 または MP4 ファイルを配置
2. `.env` ファイルの `FILE_NAME` をファイル名（拡張子あり）に設定
3. 仮想環境が有効化されていることを確認してスクリプトを実行:

```bash
cd audio_video_to_text
python audio_video_to_text.py
```

変換されたテキストは `output/` フォルダに保存されます。

#### 対応ファイル形式

- **MP3**: そのまま文字起こし
- **MP4**: 自動的にMP3に変換してから文字起こし

#### フォルダ構成

```text
audio_video_to_text/
├── audio_video_to_text.py
├── requirements.txt
├── .env
├── input/
│   ├── audio.mp3
│   └── video.mp4
└── output/
    └── audio.txt
```

#### 注意事項

- Google Cloud Platform の認証情報が必要です
- Vertex AI の使用には課金が発生する可能性があります
- MP4ファイルの変換にはFFmpegが必要です
- 大きなファイルの場合、処理に時間がかかる場合があります
- 実行前に仮想環境が有効化されていることを確認してください

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

---
allowed-tools: Bash(ls:*), Bash(cd:*), Bash(uv:*), Write, Read, Glob, LS
description: 音声文字起こしから議事録を生成
argument-hint: YYYY-MM-DD
---

# 議事録生成

## タスク

1. inputディレクトリの音声ファイルを確認し文字起こしを実行
2. 最新の文字起こしファイルを読み込む
3. 詳細な議事録を生成し04_Meetingsフォルダに保存

### ステップ1: 音声ファイル確認と文字起こし

```bash
ls .claude/audio_video_to_text/input/
cd .claude/audio_video_to_text && uv run audio_video_to_text.py
```

### ステップ2: 最新の文字起こしファイル読み込み

```bash
ls -la .claude/audio_video_to_text/output/
```

outputディレクトリから最新の`*_transcript.txt`ファイルを見つけて読み込む。

### ステップ3: 議事録生成

文字起こし内容を分析し、詳細な議事録を日本語で生成する。`04_Meetings/$ARGUMENTS-[会議名].md`に保存。

重要: 分析前に必ず文字起こし内容を読み込むこと。すべての内容を日本語で生成すること。

#### 議事録の要件

以下を含む詳細な議事録を生成する

1. 会議概要 - 会議の概要、日時、参加者、目的
2. 報告事項 - 報告内容と重要な情報
3. 討議事項 - 議論内容と質疑応答
4. 決定事項 - 決定事項と合意事項
5. アクションアイテム - 誰が、何を、いつまでに
6. メモ - 重要な備考と課題

すべてのステップを実行し、生成された議事録ファイルのパスをユーザーに報告すること。

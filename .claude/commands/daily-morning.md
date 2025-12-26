---
allowed-tools: Bash(cd:*), Bash(date:*), Bash(TZ=:*), Bash(uv:*), Bash(find:*), Write, Read, Glob, LS
argument-hint: [YYYY-MM-DD]
description: カレンダーイベントと前日のタスクからデイリーノートを作成（オプション: 特定の日付）
---

# デイリーノート朝用アシスタント（作成）

## 日付の扱い

- date引数（$1）がYYYY-MM-DD形式で指定された場合、その日付を使用
- 引数が指定されない場合、今日の日付（JST）を使用
- 対象日付: ${TARGET_DATE}

## プロジェクト設定

```txt
PROJECT_A = "Aプロジェクト"
PROJECT_B = "Bプロジェクト"
PROJECT_C = "Cプロジェクト"
```

## 目標設定

```txt
GOAL_1 = "技術力の向上"
GOAL_2 = "プロジェクト管理能力の強化"
GOAL_3 = "コミュニケーション能力の向上"
```

## タスク

1. 引数から対象日付を決定、または今日の日付を使用
2. Google Calendarのイベントを取得しMTG・イベントセクションに追加
3. 最新のデイリーノートから前日のtodoを取得
4. 対象日付のデイリーノートファイルを作成

### ステップ0: 対象日付の決定

```bash
TARGET_DATE="$1"
if [ -z "$TARGET_DATE" ]; then
  # 明示的にJSTタイムゾーンを使用
  TARGET_DATE=$(TZ=Asia/Tokyo date +%Y-%m-%d)
fi
echo "Creating daily note for: $TARGET_DATE"
```

### ステップ1: カレンダーイベントの取得

```bash
cd .claude && uv run today_cal/today-calendar.py --date "$TARGET_DATE"
```

カレンダー出力を解析し、各イベントをMTG・イベントセクション用のチェックボックス形式に変換する。

### ステップ2: 前日のタスク取得

- 重要: 現在のディレクトリは`.claude/`なので、親ディレクトリからデイリーノートを検索するためにbashを使用する必要がある
- bashコマンド`find ../01_Daily -name "*.md" -type f | sort -r | head -1`を使用して最新のデイリーノートファイルを取得
- Globツールを使用する場合、`path=".."`パラメータを明示的に指定する必要がある: `Glob(path="..", pattern="01_Daily/**/*.md")`
- 最新のデイリーノートを読み込み「明日やる」セクションの内容を抽出
- 注: タスクは以下のステータスを使用: [ ] 未着手, [/] 進行中, [R] レビュー中, [x] 完了, [-] 中止
- 抽出したタスクをユーザーに確認せずに直接使用

### ステップ3: デイリーノート作成

`01_Daily/YYYY/MM/[TARGET_DATE].md`を作成する

```markdown
---
tags:
    - { PROJECT_A }
    - { PROJECT_B }
    - { PROJECT_C }
---

# Daily [TARGET_DATE]

## MTG・イベント

[Insert calendar events from Step 1 in checkbox format]

- [ ] [Event from Google Calendar]
- [ ] [Event from Google Calendar]

## 今日のTodo

- {PROJECT_A}
  [Previous day tasks from "明日やる" section]
- {PROJECT_B}
  [Previous day tasks from "明日やる" section]
- {PROJECT_C}
  [Previous day tasks from "明日やる" section]
- ブログ
  [Previous day tasks from "明日やる" section]
- その他
  [Previous day tasks from "明日やる" section]

## 今日の振り返り

### {GOAL_1}

-

### {GOAL_2}

-

### {GOAL_3}

-

## 明日やる

- {PROJECT_A}
    - [ ] 未定
- {PROJECT_B}
    - [ ] 未定
- {PROJECT_C}
    - [ ] 未定
- ブログ
    - [ ] 未定
- その他
    - [ ] 未定
```

すべてのステップを実行し、ただちにファイルを作成すること。

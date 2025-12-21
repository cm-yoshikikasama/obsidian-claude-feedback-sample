---
allowed-tools: Bash(cd:*), Bash(source:*), Bash(date:*), Bash(TZ=*), Bash(uv:*), Write, Read, Glob, Edit, LS
argument-hint: [YYYY-MM-DD]
description: Update daily note with achievements and tomorrow's plan (optional: specific date)
---

# Daily Note Evening Assistant（夜用・更新）

## Date Handling

- If date argument ($1) is provided in YYYY-MM-DD format, use that date
- If no argument provided, use today's date (JST)
- Target date: ${TARGET_DATE}

## Project Configuration

```txt
PROJECT_A = "Aプロジェクト"
PROJECT_B = "Bプロジェクト"
PROJECT_C = "Cプロジェクト"
```

## Goals (目標) - Customize This Section

ここに自分の目標を記載してください。例:

- [目標1: 例) 技術力の向上]
- [目標2: 例) プロジェクト管理能力の強化]
- [目標3: 例) コミュニケーション能力の向上]

## Your task

1. Determine target date from argument or use today
2. Get Google Calendar events for target date
3. Find and read target date's daily note
4. Ask user 5 questions one by one about achievements and reflection
5. Update the existing daily note file with responses and auto-generate tomorrow's tasks

### Step 0: Determine Target Date

```bash
TARGET_DATE="$1"
if [ -z "$TARGET_DATE" ]; then
  # Explicitly use JST timezone
  TARGET_DATE=$(TZ=Asia/Tokyo date +%Y-%m-%d)
fi
echo "Processing daily note for: $TARGET_DATE"
```

### Step 1: Get Calendar Events

```bash
cd .claude && uv run today_cal/today-calendar.py --date "$TARGET_DATE"
```

Parse calendar output to understand the target date's events and generate relevant questions.

### Step 2: Find Target Date's Daily Note

- **IMPORTANT**: Current directory is `.claude/`, so you MUST specify `path=".."` when using Glob
- Use bash command: `find ../01_Daily -name "${TARGET_DATE}.md" -type f` to find the target daily note
- Alternative: Use Glob with `Glob(path="..", pattern="01_Daily/**/[TARGET_DATE].md")`
- The file should be in `01_Daily/YYYY/MM/[TARGET_DATE].md` format
- Read the file to understand current content structure

### Step 3: Ask User Questions with Calendar Context (一つずつ質問)

First, analyze the Google Calendar events and match them to projects. Then ask these questions one by one, incorporating calendar information. Wait for each response before proceeding:

**ステータス番号：**
1=未着手, 2=進行中, 3=レビュー中, 4=完了, 5=中止

**質問1: {PROJECT_A}のタスク進捗**
Google Calendarから、{PROJECT_A}関連で以下の予定がありました：
[カレンダーの該当イベントをリスト表示]

デイリーノートの{PROJECT_A}タスクは以下です：

1. [タスク1の内容]
2. [タスク2の内容]
3. [タスク3の内容]

各タスクのステータスを番号で入力してください（例: 1-4, 2-2, 3-1）：
追加でやったタスクがあれば教えてください。

**質問2: {PROJECT_B}のタスク進捗**
Google Calendarから、{PROJECT_B}関連で以下の予定がありました：
[カレンダーの該当イベントをリスト表示]

デイリーノートの{PROJECT_B}タスクは以下です：

1. [タスク1の内容]
2. [タスク2の内容]
3. [タスク3の内容]

各タスクのステータスを番号で入力してください（例: 1-4, 2-2, 3-1）：
追加でやったタスクがあれば教えてください。

**質問3: {PROJECT_C}のタスク進捗**
Google Calendarから、{PROJECT_C}関連で以下の予定がありました：
[カレンダーの該当イベントをリスト表示]

デイリーノートの{PROJECT_C}タスクは以下です：

1. [タスク1の内容]
2. [タスク2の内容]
3. [タスク3の内容]

各タスクのステータスを番号で入力してください（例: 1-4, 2-2, 3-1）：
追加でやったタスクがあれば教えてください。

**質問4: ブログ・その他のタスク進捗**
Google Calendarから、その他の予定で以下がありました：
[カレンダーの該当イベントをリスト表示]

デイリーノートのブログ・その他のタスクは以下です：

1. [タスク1の内容]
2. [タスク2の内容]
3. [タスク3の内容]

各タスクのステータスを番号で入力してください（例: 1-4, 2-2, 3-1）：
追加でやったタスクがあれば教えてください。

**質問5: 今日の振り返り（目標に沿った振り返り）**
今日1日をGoalsセクションに記載した目標に沿って振り返ってください（すべて答える必要はなく、気になる観点だけで構いません）:

各目標について、何か成果となるような行動、記録はありましたか？

### Step 4: Update Daily Note File

After collecting all responses, update the daily note file:

1. Read `01_Daily/YYYY/MM/[TARGET_DATE].md` file
2. Update MTG・イベント section:
    - Mark ALL Google Calendar events as `- [x]` (attended)
    - For events that exist in daily note but NOT in Google Calendar, mark with strikethrough: `- [ ] ~~event name~~ (実施せず)`
3. Update 今日のTodo section:
    - Mark completed items as `- [x]`
    - Update in-progress items as `- [/]`
    - Mark items under review as `- [R]`
    - Mark cancelled items as `- [-]`
    - Keep pending items as `- [ ]`
    - Update progress details (e.g., "実装進める" → "実装80%完了、動作検証に移行")
4. Update 今日の振り返り section:
    - 感謝: Add user responses as bullet points
    - Good: Add user responses as bullet points
    - Motto: Add user responses
5. Update 明日やる section:
    - Automatically extract tasks from "今日のTodo" section that are NOT completed (状態が [x] でないもの)
    - Include tasks with status: [ ] 未着手, [/] 進行中, [R] レビュー中
    - Exclude tasks with status: [x] 完了, [-] 中止
    - Copy these tasks to "明日やる" section, resetting all checkboxes to [ ]
    - If a project has no remaining tasks, set it to "[ ] 未定"

**Execute all steps and update the file immediately.**

更新例：

```markdown
## MTG・イベント

- [x] 08:30 - (プロジェクトA)実装 # Google Calendarにあった予定
- [x] 11:00 - (プロジェクトB)内部MTG # Google Calendarにあった予定
- [ ] ~~14:00 - (プロジェクトC)内部MTG~~ (実施せず) # Daily noteにあったがGoogle Calendarになかった予定
- [x] 終日 - 自宅 # Google Calendarにあった予定

## 今日のTodo

- Aプロジェクト
    - [x] 実装80%完了、動作検証に移行 # 完了
    - [/] APIテスト進行中 # 進行中
- Bプロジェクト
    - [x] 単体テスト完了、結合テスト開始 # 完了
    - [R] コードレビュー待ち # レビュー中
- Cプロジェクト
    - [x] アーキテクチャ検討完了、構成図作成中 # 完了
    - [-] 会議が中止になったため延期 # 中止
- ブログ
    - [ ] （予定なし） # 未着手
- その他
    - [ ] （予定なし）

## 今日の振り返り

### [目標1]

- [ユーザーの回答内容]

### [目標2]

- [ユーザーの回答内容]

### [目標3]

- [ユーザーの回答内容]

## 明日やる

- {PROJECT_A}
    - [ ] [今日のTodoから未完了タスクを自動抽出]
- {PROJECT_B}
    - [ ] [今日のTodoから未完了タスクを自動抽出]
- {PROJECT_C}
    - [ ] [今日のTodoから未完了タスクを自動抽出]
- ブログ
    - [ ] [今日のTodoから未完了タスクを自動抽出]
- その他
    - [ ] [今日のTodoから未完了タスクを自動抽出]
```

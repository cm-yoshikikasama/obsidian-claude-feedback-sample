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

### Step 3: Ask User Questions with Calendar Context (AskUserQuestionツールを使用)

First, analyze the Google Calendar events and match them to projects. Then use the AskUserQuestion tool to ask questions in checkbox format.

**IMPORTANT**: Use the AskUserQuestion tool for all questions below. This provides an interactive checkbox/selection interface.

ステータス番号: 1=未着手, 2=進行中, 3=レビュー中, 4=完了, 5=中止

#### 質問パターン（プロジェクトごと）

IMPORTANT: For each project, use a SINGLE AskUserQuestion call with multiple questions (up to 4). This creates a tabbed interface where users can switch between questions.

For each project (PROJECT_A, PROJECT_B, PROJECT_C, ブログ・その他):

1. Before asking questions, output text message showing Google Calendar events for this project
2. Collect all tasks in the project from the daily note
3. SKIP tasks that are "未定" (not yet determined) - do not ask about their status
4. Create one question per task (max 3 tasks to leave room for additional task question)
5. Add one final question asking about additional tasks
6. If ALL tasks are "未定", only ask the additional tasks question
7. Send all questions in ONE AskUserQuestion call

First, output a text message like:

```text
## {PROJECT_NAME}のタスク進捗

Google Calendar予定:
- [event 1]
- [event 2]
```

Then ask questions:

Task status question format (for each task in the project):

```text
タスク「[タスク内容]」の状態を教えてください。
```

header: "タスク[N]" (e.g., "タスク1", "タスク2", etc.)

multiSelect: false

options for task status:

- label: "未着手", description: "タスクにまだ着手していない"
- label: "進行中", description: "タスクを進行中"
- label: "レビュー中", description: "タスクがレビュー待ち"
- label: "完了", description: "タスクが完了"

For cancelled tasks (中止), user can input via "Other" field.

Additional tasks question format (final question in the project):

```text
{PROJECT_NAME}で追加でやったタスクがあれば「Other」で入力してください。なければ「なし」を選択してください。
```

header: "追加タスク"

multiSelect: false

options (minimum 2 required):

- label: "なし", description: "追加タスクはありません"
- label: "入力する", description: "Otherで追加タスクを入力します"

Note: User can input additional tasks via "Other" field.

Example: If PROJECT_A has 2 tasks, send ONE AskUserQuestion call with 3 questions (task1, task2, additional tasks) that appear as tabs.

#### 質問1: PROJECT_Aのタスク進捗

Use AskUserQuestion tool for each task in PROJECT_A section

#### 質問2: PROJECT_Bのタスク進捗

Use AskUserQuestion tool for each task in PROJECT_B section

#### 質問3: PROJECT_Cのタスク進捗

Use AskUserQuestion tool for each task in PROJECT_C section

#### 質問4: ブログ・その他のタスク進捗

Use AskUserQuestion tool for each task in ブログ and その他 sections

#### 質問5: 今日の振り返り（目標に沿った振り返り）

Do NOT use AskUserQuestion tool for reflection. Instead, output a text message asking for reflection:

```
今日1日を設定した目標に沿って振り返ってください（該当する観点があれば教えてください）:

- [目標1に関連する振り返り]
- [目標2に関連する振り返り]
- [目標3に関連する振り返り]
```

Wait for user's text response. User can provide free-form text answers for each category they want to reflect on.

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

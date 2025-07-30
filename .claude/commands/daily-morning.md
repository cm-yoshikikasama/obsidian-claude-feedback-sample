---
allowed-tools: Bash(cd:*), Bash(source:*), Bash(python:*), Write, Read, Glob
description: Create daily note from calendar events and previous day's tasks
---

# Daily Note Morning Assistant（朝用・作成）

## Project Configuration

```
PROJECT_A = "Aプロジェクト"
PROJECT_B = "Bプロジェクト"
PROJECT_C = "Cプロジェクト"
```

## Your task

1. Get Google Calendar events and add to MTG・イベント section
2. Get previous day's todo from latest daily note
3. Ask user for todo updates
4. Create today's daily note file

### Step 1: Get Calendar Events

```bash
cd .claude && source .venv/bin/activate && python today_cal/today-calendar.py
```

Parse calendar output and convert each event to checkbox format for MTG・イベント section.

### Step 2: Get Previous Tasks

- Find latest daily note in `01_Daily/`
- Extract "明日やる" section content
- If no previous daily note exists, skip to Step 3B

### Step 3A: User Confirmation (when previous tasks exist)

Show previous tasks and ask: "今日のTodoに修正や追加はありますか？修正がある場合は具体的に教えてください。修正がなければ「そのまま」とお答えください。"

### Step 3B: User Input (when no previous tasks exist)

Ask user for today's todos by project:
"前回のdaily noteがないため、今日の各プロジェクトの予定を教えてください：

- Aプロジェクト:
- Bプロジェクト:
- Cプロジェクト:
- ブログ:
- その他: "

### Step 4: Create Daily Note

Create `01_Daily/[今日の日付].md`:

```markdown
---
tags:
    - { PROJECT_A }
    - { PROJECT_B }
    - { PROJECT_C }
---

# Daily [今日の日付]

## MTG・イベント

[Insert calendar events from Step 1 in checkbox format]

- [ ] [Event from Google Calendar]
- [ ] [Event from Google Calendar]

## 今日のTodo

- {PROJECT_A}
  [Previous day tasks + user updates]
- {PROJECT_B}
  [Previous day tasks + user updates]
- {PROJECT_C}
  [Previous day tasks + user updates]
- ブログ
  [Previous day tasks + user updates]
- その他
  [Previous day tasks + user updates]

## 今日の振り返り

### 感謝

-

### Good

-

### Motto

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

**Execute all steps and create the file immediately.**

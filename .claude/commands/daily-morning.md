---
allowed-tools: Bash(cd:*), Bash(source:*), Bash(date:*), Bash(TZ=*), Bash(uv:*), Bash(TARGET_DATE=*), Write, Read, Glob, LS
argument-hint: [YYYY-MM-DD]
description: Create daily note from calendar events and previous tasks (optional: specific date)
---

# Daily Note Morning Assistant（朝用・作成）

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

## Your task

1. Determine target date from argument or use today
2. Get Google Calendar events and add to MTG・イベント section
3. Get previous day's todo from latest daily note
4. Create target date's daily note file

### Step 0: Determine Target Date

```bash
TARGET_DATE="$1"
if [ -z "$TARGET_DATE" ]; then
  # Explicitly use JST timezone
  TARGET_DATE=$(TZ=Asia/Tokyo date +%Y-%m-%d)
fi
echo "Creating daily note for: $TARGET_DATE"
```

### Step 1: Get Calendar Events

```bash
cd .claude && uv run today_cal/today-calendar.py --date "$TARGET_DATE"
```

Parse calendar output and convert each event to checkbox format for MTG・イベント section.

### Step 2: Get Previous Tasks

- **IMPORTANT**: Current directory is `.claude/`, so you MUST use bash to find daily notes from parent directory
- Use bash command: `find ../01_Daily -name "*.md" -type f | sort -r | head -1` to get the most recent daily note file
- If Glob tool is used, you MUST specify `path=".."` parameter explicitly: `Glob(path="..", pattern="01_Daily/**/*.md")`
- Read the latest daily note and extract "明日やる" section content
- Note: Tasks use these statuses: [ ] 未着手, [/] 進行中, [R] レビュー中, [x] 完了, [-] 中止
- Use the extracted tasks directly without asking the user for confirmation

### Step 3: Create Daily Note

Create `01_Daily/YYYY/MM/[TARGET_DATE].md`:

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

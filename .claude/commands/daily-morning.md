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
4. Ask user for todo updates
5. Create target date's daily note file

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
- If no previous daily note exists, skip to Step 3B

### Step 3A: User Confirmation (when previous tasks exist)

Show previous tasks and ask: "今日のTodoに修正や追加はありますか？修正がある場合は具体的に教えてください。修正がなければ「なし」とお答えください。"

### Step 3B: User Input (when no previous tasks exist)

Ask user for today's todos by project:
"前回のdaily noteがないため、今日の各プロジェクトの予定を教えてください：

- Aプロジェクト:
- Bプロジェクト:
- Cプロジェクト:
- ブログ:
- その他: "

### Step 4: Create Daily Note

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

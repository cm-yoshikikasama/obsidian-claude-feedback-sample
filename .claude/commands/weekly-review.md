---
allowed-tools: Bash, Write, Read, Glob, Edit
argument-hint: [monday-date]
description: Generate weekly summary and AI review from daily notes (Monday-Friday)
---

# Weekly Summary & AI Review Generator（週次まとめとAIレビュー生成）

## Overview

This command generates a weekly summary and AI review by analyzing daily notes from a specified week. It extracts key activities and provides AI-generated insights and recommendations.

## Date Handling

- If monday-date argument ($1) is provided in YYYY-MM-DD format, use that Monday as start date
- Week is Monday to Friday (5 working days)
- If no argument provided, use last week's Monday (last complete work week)

## Your Task

Execute the following steps in order to generate a complete weekly review:

### Step 1: Determine Target Week

First, calculate the target date range:

```bash
# If Monday date provided, use it; otherwise calculate last complete work week
if [ -n "$1" ]; then
  START_DATE="$1"
  # Calculate Friday (4 days after Monday)
  END_DATE=$(date -d "$START_DATE + 4 days" +%Y-%m-%d 2>/dev/null || date -v+4d -j -f "%Y-%m-%d" "$START_DATE" +%Y-%m-%d)
else
  # Default to last complete work week (Monday to Friday)
  # Get last Monday
  DAYS_SINCE_MONDAY=$(($(date +%u) - 1))
  if [ $DAYS_SINCE_MONDAY -eq 0 ]; then
    DAYS_SINCE_MONDAY=7
  fi
  START_DATE=$(date -d "$((DAYS_SINCE_MONDAY + 7)) days ago" +%Y-%m-%d 2>/dev/null || date -v-$((DAYS_SINCE_MONDAY + 7))d +%Y-%m-%d)
  # Calculate Friday (4 days after that Monday)
  END_DATE=$(date -d "$START_DATE + 4 days" +%Y-%m-%d 2>/dev/null || date -v+4d -j -f "%Y-%m-%d" "$START_DATE" +%Y-%m-%d)
fi

echo "Generating weekly review for: $START_DATE to $END_DATE (Mon-Fri)"
```

### Step 2: Find and Read Daily Notes

- **IMPORTANT**: Current directory is `.claude/`, so you MUST search from parent directory
- Use bash command: `find ../01_Daily -name "*.md" -type f | sort` to find all daily notes
- Alternative: Use Glob with `Glob(path="..", pattern="01_Daily/**/*.md")`
- Filter files within the target date range (START_DATE to END_DATE)
- Daily notes follow pattern: `01_Daily/YYYY/MM/YYYY-MM-DD.md`
- Read each file that falls within the target week

### Step 3: Extract and Analyze Information

From each daily note, systematically extract:

1. **MTG・イベント** - Completed meetings and events (check items marked with ✓ or completed)
2. **今日のTodo** - Tasks by project categories with status tracking:
    - [ ] 未着手 (pending)
    - [/] 進行中 (in progress)
    - [R] レビュー中 (under review)
    - [x] 完了 (completed)
    - [-] 中止 (cancelled)
3. **今日の振り返り** sections:
    - **感謝** - Gratitude entries
    - **Good** - Positive points
    - **Motto** - Daily mottos or insights
4. **明日やる** - Plans that were made
5. Any **thino** entries or quick notes
6. Any other significant content or achievements

### Step 4: Aggregate and Generate Insights

Organize extracted information and generate AI-powered insights:

1. **Daily Summaries** - Create meaningful summaries for each day
2. **Project Analysis** - Group activities by project and assess progress
3. **Pattern Recognition** - Identify recurring themes, challenges, or successes
4. **Productivity Analysis** - Analyze task completion patterns
5. **Balance Assessment** - Evaluate time/effort distribution across projects
6. **Growth Opportunities** - Identify areas for improvement based on patterns

### Step 5: Create Weekly Review File

Generate the file at: `02_Weekly/YYYYMMDD_weekly_review.md`

Use the following template structure, populated with actual data and insights:

## Weekly Review Template

```markdown
# 週次まとめとAIレビュー - [START_DATE]週

## 📅 対象期間

- [START_DATE] (月) 〜 [END_DATE] (金)

## 📊 今週のまとめ

### 日毎の活動

[デイリーノートから主要な活動と完了タスクを抽出して整理]

### プロジェクト別実績

[検出されたプロジェクト名で動的にセクション作成し、成果をまとめる]

### 主要な成果

[今週の重要な成果や達成事項]

## 🤖 AIによるレビューとフィードバック

### 📈 生産性の分析

[タスク完了率、作業パターン、効率性に関するAI分析]

### ✨ 良かった点

[デイリーノートから抽出した成功ポイントとAI評価]

### 🔧 改善提案

[課題の識別と具体的な改善アクション]

### 🎯 来週への推奨事項

[AIが分析したパターンに基づく来週の行動提案]

## 📎 参照ファイル

[参照したデイリーノートのwikiリンク]

```

### Step 6: AI Analysis and Feedback Generation

When generating the AI feedback sections, analyze the extracted data for:

1. **生産性パターン** - Look for productivity patterns, peak performance times, task completion rates
2. **バランス分析** - Assess whether time allocation aligns with priorities
3. **成長指標** - Identify learning opportunities and skill development areas
4. **習慣分析** - Recognize positive habits worth reinforcing and negative patterns to address
5. **ストレス指標** - Look for signs of overwhelm, burnout, or balance issues
6. **協力関係** - Analyze team interactions and collaboration effectiveness

### Execution Instructions

**Execute all steps immediately and create the complete weekly review file with:**

1. ✅ Proper date calculation and range determination
2. ✅ Systematic extraction from all daily notes in range
3. ✅ Meaningful daily summaries with actual achievements
4. ✅ Project-based organization of activities
5. ✅ AI-generated insights and patterns recognition
6. ✅ Specific, actionable improvement recommendations
7. ✅ Quantitative metrics where possible
8. ✅ Proper file linking to referenced daily notes
9. ✅ Professional formatting and structure

**Save the final file to: `02_Weekly/[YYYYMMDD]_weekly_review.md`**

The generated review should be comprehensive, insightful, and immediately actionable for continuous improvement.

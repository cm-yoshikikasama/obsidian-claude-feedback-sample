---
allowed-tools: Bash, Write, Read, Glob, LS
description: Generate meeting minutes from audio transcription
argument-hint: YYYY-MM-DD
---

# Meeting Minutes Generator

## Your task

1. Check and transcribe audio files from input directory
2. Read the latest transcript file
3. Generate detailed meeting minutes and save to 04_Meetings folder

### Step 1: Check Audio Files and Transcribe

```bash
ls .claude/audio_video_to_text/input/
cd .claude/audio_video_to_text && uv run audio_video_to_text.py
```

### Step 2: Read Latest Transcript

```bash
ls -la .claude/audio_video_to_text/output/
```

Find and read the latest `*_transcript.txt` file from output directory.

### Step 3: Generate Meeting Minutes

Analyze transcript and generate detailed meeting minutes in Japanese. Save to `04_Meetings/$ARGUMENTS-[meeting name].md`.

**Important: Read transcript before analysis. Generate all content in Japanese.**

#### Meeting Minutes Requirements

Generate detailed meeting minutes including:

1. **会議概要** - Meeting overview, date, participants, purpose
2. **報告事項** - Reports and important information
3. **討議事項** - Discussions and Q&A
4. **決定事項** - Decisions and agreements
5. **アクションアイテム** - Who, what, when (action items)
6. **メモ** - Important remarks and issues

**Execute all steps and report the generated meeting minutes file path to user.**

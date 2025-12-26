# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal Obsidian vault containing organized markdown notes in Japanese and English. The repository structure follows a personal knowledge management system with integrated tools for audio/video transcription and markdown formatting.

## Key Components

### 1. Obsidian Vault Structure

- 00_Configs/ - Configuration files and templates (Extra/, Templates/)
- 01_Daily/ - Daily notes and logs
- 02_Weekly/ - Weekly summaries and AI reviews
- 03_RoughNotes/ - Temporary notes and rough materials
- 04_EngStudy/ - English study materials and lesson feedback
- 05_Meetings/ - Meeting notes and minutes
- 06_Clippings/ - Web clippings and saved articles

### 2. Audio/Video Transcription Tool

Located in `audio_video_to_text/`, this Python tool uses Google Vertex AI's Gemini model to transcribe MP3 audio and MP4 video files to text.

### 3. Markdown Formatting System

Uses Prettier for consistent markdown formatting with automatic post-edit hooks.

## Development Commands

### Markdown Formatting

```bash
# Format all markdown files
npm run format

# Format automatically triggered by Claude Code hooks after Write/Edit/MultiEdit operations
```

### Audio/Video Transcription

```bash
# Setup and run from project root using uv
cd .claude
uv run audio_video_to_text/audio_video_to_text.py

# Alternative: Traditional setup (if needed)
cd .claude
uv venv --python 3.13
source .venv/bin/activate  # macOS/Linux
uv pip install -r requirements.txt
python audio_video_to_text/audio_video_to_text.py
```

### Google Calendar Integration

```bash
# Get today's calendar events
cd .claude
uv run today_cal/today-calendar.py
```

### Custom Slash Commands

The project includes several slash commands in `.claude/commands/`

- `/daily-morning [date]` - Create morning daily note with calendar events and previous day's tasks
- `/daily-evening [date]` - Update evening daily note with reflections and tomorrow's planning
- `/english-lesson [date]` - Generate English lesson feedback from audio transcription
- `/meeting-minutes [date]` - Generate meeting minutes from audio transcription
- `/commit-message` - Generate Git commit messages from staged changes
- `/weekly-review [monday-date]` - Generate weekly summaries and AI reviews

## Architecture Details

### Template System

The vault uses structured templates in `00_Configs/Templates/`

- Daily.md - Daily notes with sections for meetings, todos (categorized by projects), reflections, and planning
- English lesson.md - English study session template

### Todo Organization

Daily notes follow a consistent todo categorization and 5-stage status system

Categories

- Aプロジェクト, Bプロジェクト, Cプロジェクト (work projects)
- ブログ (blog-related tasks)
- その他 (other tasks)

Status System

- `[ ]` 未着手 (Not started)
- `[/]` 進行中 (In progress)
- `[R]` レビュー中 (Under review)
- `[x]` 完了 (Completed)
- `[-]` 中止 (Cancelled/Postponed)

### Audio Transcription Pipeline

1. Place MP3/MP4 files in `audio_video_to_text/input/`
2. Configure `.env` with GCP credentials and FILE_NAME
3. Script automatically converts MP4 to MP3 if needed
4. Uses Gemini model for transcription with speaker change detection
5. Outputs formatted text to `audio_video_to_text/output/`

## Important Configuration

### Claude Code Settings

- Auto-formatting hooks configured in `.claude/settings.json`
- Prettier formatting applied to all markdown files after Write/Edit/MultiEdit operations
- Custom permissions limiting file system access to current directory only
- Notification and completion sound hooks configured (macOS Funk.aiff)
- Telemetry disabled for privacy

### Dependencies

- Node.js - For Prettier markdown formatting (`npm run format`)
- Python 3.13 - For AI transcription and calendar integration
- uv - Python package manager and virtual environment tool (preferred over pip/venv)
- FFmpeg - Required for MP4 to MP3 conversion in transcription pipeline
- Google Cloud Platform - Vertex AI API access for transcription
- Google Calendar API - OAuth2 credentials required for calendar integration

### Python Dependencies (`.claude/requirements.txt`)

Audio/Video transcription

- `vertexai` - Google's AI platform for transcription
- `python-dotenv` - Environment variable management
- `ffmpeg-python` - Video to audio conversion

Google Calendar integration

- `google-auth`, `google-auth-oauthlib`, `google-auth-httplib2` - OAuth2 authentication
- `google-api-python-client` - Calendar API client

### Environment Setup

Audio transcription requires `.env` file in `.claude/audio_video_to_text/`

```env
PROJECT_ID=your-gcp-project-id
REGION=your-region
FILE_NAME=audio  # filename without extension
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json
```

Google Calendar integration requires OAuth2 setup

- `cal_client_secret.json` in `.claude/` directory
- First run will create `token.json` automatically

## Working with This Repository

### Content Language

- Primary content is in Japanese
- Some technical content and templates include English
- Mixed language usage is common in technical notes

### File Creation Policy

- NEVER create files unless absolutely necessary
- ALWAYS prefer editing existing files
- NEVER proactively create documentation files unless explicitly requested

### Template Usage

- Use templates from `00_Configs/Templates/` for structured notes
- Maintain consistent categorization in todo sections
- Respect the bilingual nature of content

### Key System Files

- Base.base - Obsidian Base plugin configuration for database-like views
- .prettierrc - Markdown formatting rules (consistent across all .md files)
- .claude/format-md.sh - Auto-format script triggered by Claude Code hooks

## Important Instruction Reminders

Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (\*.md) or README files. Only create documentation files if explicitly requested by the User.

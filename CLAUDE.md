# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal Obsidian vault containing organized markdown notes in Japanese and English. The repository structure follows a personal knowledge management system with integrated tools for audio/video transcription and markdown formatting.

## Key Components

### 1. Obsidian Vault Structure

- **00_Configs/**: Configuration files and templates
- **01_Daily/**: Daily notes and logs
- **02_Inbox/**: Temporary notes and research materials
- **03_eng_study/**: English study materials
- **04_Meetings/**: Meeting notes and minutes

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
# Setup Python environment (using uv)
cd audio_video_to_text
uv venv --python 3.13
source .venv/bin/activate  # macOS/Linux
uv pip install -r requirements.txt

# Run transcription (requires .env file with GCP credentials)
python audio_video_to_text.py
```

## Architecture Details

### Template System

The vault uses structured templates in `00_Configs/Templates/`:

- **Daily.md**: Daily notes with sections for meetings, todos (categorized by projects), reflections, and planning
- **English lesson.md**: English study session template

### Todo Organization

Daily notes follow a consistent todo categorization:

- Aプロジェクト, Bプロジェクト, Cプロジェクト (work projects)
- ブログ (blog-related tasks)
- その他 (other tasks)

### Audio Transcription Pipeline

1. Place MP3/MP4 files in `audio_video_to_text/input/`
2. Configure `.env` with GCP credentials and FILE_NAME
3. Script automatically converts MP4 to MP3 if needed
4. Uses Gemini model for transcription with speaker change detection
5. Outputs formatted text to `audio_video_to_text/output/`

## Important Configuration

### Claude Code Settings

- Auto-formatting hooks configured in `.claude/settings.json`
- Prettier formatting applied to all markdown files after edits
- Custom permissions and security settings defined

### Dependencies

- **Node.js**: For Prettier markdown formatting
- **Python 3.13**: For audio transcription tool
- **uv**: Python package manager and virtual environment tool
- **FFmpeg**: Required for MP4 to MP3 conversion
- **Google Cloud Platform**: Vertex AI API access required

### Environment Setup

Audio transcription requires `.env` file in `audio_video_to_text/`:

```env
PROJECT_ID=your-gcp-project-id
REGION=your-region
FILE_NAME=audio  # filename without extension
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json
```

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

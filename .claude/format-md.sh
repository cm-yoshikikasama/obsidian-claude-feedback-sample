#!/bin/bash
FILE_PATH=$(jq -r '.tool_input.file_path')
if [[ "$FILE_PATH" == *.md ]]; then
    echo "📝 Formatting markdown file: $FILE_PATH"
    if [ -f node_modules/.bin/prettier ]; then
        npx prettier --write "$FILE_PATH" && echo "✅ Prettier formatting completed for $FILE_PATH" || echo "❌ Prettier formatting failed for $FILE_PATH"
    elif command -v prettier >/dev/null 2>&1; then
        prettier --write "$FILE_PATH" && echo "✅ Prettier formatting completed for $FILE_PATH" || echo "❌ Prettier formatting failed for $FILE_PATH"
    else
        echo "⚠️  Warning: prettier not found, skipping formatting for $FILE_PATH"
    fi
fi
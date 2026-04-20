#!/bin/bash
# Jarvis — Launch Session (macOS)

# Get config
CONFIG_PATH="$(dirname "$0")/../config.json"
WORKSPACE_PATH=$(jq -r '.workspace_path' "$CONFIG_PATH")
YOUTUBE_URL=$(jq -r '.youtube_track' "$CONFIG_PATH")
BROWSER_URLS=$(jq -r '.browser_urls[]' "$CONFIG_PATH" | tr '\n' ' ')

# 1. Start server in new Terminal window
open -a Terminal "$WORKSPACE_PATH"
sleep 1
osascript -e "tell application \"Terminal\" to do script \"cd $WORKSPACE_PATH && python3 server.py\""

# 2. Open browser with Jarvis + URLs
open -a "Google Chrome" "http://localhost:8340"
for url in $BROWSER_URLS; do
    open -a "Google Chrome" "$url"
done

# 3. Open YouTube
if [ ! -z "$YOUTUBE_URL" ]; then
    open "$YOUTUBE_URL"
fi

# 4. Open VSCode
CODE_APPS=$(jq -r '.apps[]' "$CONFIG_PATH" | grep -i vscode)
if [ ! -z "$CODE_APPS" ]; then
    open -a "Visual Studio Code" "$WORKSPACE_PATH"
fi

echo "[jarvis] Session launched — Jarvis is ready!"

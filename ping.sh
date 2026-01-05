#!/bin/bash

PROJECT="ope-test"
POD_NAME="meera-test-0"
ERROR_PATTERN="WebSocket ping timeout after"
LOCAL_LOG_FILE="./websocket_timeouts.log"

oc project "$PROJECT" >/dev/null

# (Optional) start a fresh file each run:
: > "$LOCAL_LOG_FILE"

echo "Watching pod logs for: $ERROR_PATTERN"
echo "Writing matches to: $LOCAL_LOG_FILE"
echo "Started at $(date)" >> "$LOCAL_LOG_FILE"

cleanup() {
  echo
  echo "Stopping log monitor..."
  if [[ -n "${LOG_PID:-}" ]]; then
    kill "$LOG_PID" 2>/dev/null || true
  fi
}
trap cleanup INT TERM

# Stream logs and append only matching lines to local file
oc logs -f "$POD_NAME" | while read -r line; do
  if grep -qF "$ERROR_PATTERN" <<<"$line"; then
    {
      echo "--------------------------------------------"
      echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
      echo "$line"
    } >> "$LOCAL_LOG_FILE"
  fi
done &
LOG_PID=$!

# Keep the script alive until the background job exits (or Ctrl+C)
wait "$LOG_PID"

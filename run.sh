#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# install deps if missing
pip3 install flask requests smbus2 bmp280 --quiet --break-system-packages 2>/dev/null || true

# start flask
cd "$SCRIPT_DIR/backend"
python3 app.py &
FLASK_PID=$!

# start telegram bot (reads .env from repo root)
export $(grep -s -v '^#' "$SCRIPT_DIR/.env" | xargs) 2>/dev/null || true
python3 "$SCRIPT_DIR/backend/bot.py" &
BOT_PID=$!

# wait for flask to be ready
sleep 3

# open chromium fullscreen, no chrome UI
chromium \
  --kiosk \
  --app=http://localhost:5000 \
  --window-size=1280,480 \
  --window-position=0,0 \
  --force-device-scale-factor=1 \
  --disable-infobars \
  --no-first-run \
  --noerrdialogs \
  --disable-translate \
  --disable-features=TranslateUI \
  2>/dev/null &

trap "kill $FLASK_PID $BOT_PID 2>/dev/null; exit" INT TERM
wait $FLASK_PID

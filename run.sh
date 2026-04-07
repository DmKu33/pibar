#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! python3 -c "import flask" 2>/dev/null; then
  pip3 install -r "$SCRIPT_DIR/backend/requirements.txt" --quiet
fi

cd "$SCRIPT_DIR/backend"
python3 app.py &
FLASK_PID=$!

sleep 1

chromium-browser \
  --app=http://localhost:5000 \
  --window-size=1280,480 \
  --window-position=0,0 \
  --disable-infobars \
  --no-first-run \
  --noerrdialogs \
  2>/dev/null &

trap "kill $FLASK_PID 2>/dev/null; exit" INT TERM
wait $FLASK_PID

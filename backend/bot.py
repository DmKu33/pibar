"""
pibar Telegram bot
------------------
Runs as a separate process alongside app.py.
Writes reminders to tasks.md in the repo root.

Commands:
  /add <text> [| date]   — add a reminder, optional date after |
  /list                  — show current reminders
  /done <n>              — mark reminder #n as done
  /del <n>               — delete reminder #n
"""

import os
import re
import time
import logging
import requests

TOKEN    = os.environ.get("TELEGRAM_TOKEN", "")
OWNER_ID = int(os.environ.get("TELEGRAM_OWNER_ID", "0"))
TASKS_FILE = os.path.join(os.path.dirname(__file__), "..", "tasks.md")

API = f"https://api.telegram.org/bot{TOKEN}"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)


# ── tasks.md helpers ──────────────────────────────────────────────────────

def read_lines():
    try:
        with open(TASKS_FILE) as f:
            return f.readlines()
    except FileNotFoundError:
        return []

def write_lines(lines):
    with open(TASKS_FILE, "w") as f:
        f.writelines(lines)

def task_lines(lines):
    """Return (index_in_lines, line) for every task line."""
    return [(i, l) for i, l in enumerate(lines) if l.strip().startswith("- [")]

def format_list(lines):
    tasks = task_lines(lines)
    if not tasks:
        return "No reminders yet."
    out = []
    for n, (_, l) in enumerate(tasks, 1):
        done = "[x]" in l or "[X]" in l
        text = re.sub(r"^-\s+\[[xX ]\]\s*", "", l).strip()
        tick = "✓" if done else "•"
        out.append(f"{n}. {tick} {text}")
    return "\n".join(out)


# ── command handlers ──────────────────────────────────────────────────────

def cmd_add(arg):
    if not arg:
        return "Usage: /add <reminder text> [| date]"
    line = f"- [ ] {arg.strip()}\n"
    lines = read_lines()
    lines.append(line)
    write_lines(lines)
    return f"Added: {arg.strip()}"

def cmd_list():
    return format_list(read_lines())

def cmd_done(arg):
    try:
        n = int(arg.strip())
    except (ValueError, AttributeError):
        return "Usage: /done <number>"
    lines = read_lines()
    tasks = task_lines(lines)
    if n < 1 or n > len(tasks):
        return f"No reminder #{n}."
    idx, l = tasks[n - 1]
    lines[idx] = l.replace("[ ]", "[x]", 1)
    write_lines(lines)
    return f"Marked done: #{n}"

def cmd_del(arg):
    try:
        n = int(arg.strip())
    except (ValueError, AttributeError):
        return "Usage: /del <number>"
    lines = read_lines()
    tasks = task_lines(lines)
    if n < 1 or n > len(tasks):
        return f"No reminder #{n}."
    idx, _ = tasks[n - 1]
    removed = lines.pop(idx).strip()
    write_lines(lines)
    text = re.sub(r"^-\s+\[[xX ]\]\s*", "", removed)
    return f"Deleted: {text}"

def handle(text):
    text = text.strip()
    if text.startswith("/add"):
        return cmd_add(text[4:].strip())
    if text.startswith("/list"):
        return cmd_list()
    if text.startswith("/done"):
        return cmd_done(text[5:].strip())
    if text.startswith("/del"):
        return cmd_del(text[4:].strip())
    if text.startswith("/start"):
        return (
            "pibar reminders\n\n"
            "/add <text> [| date]  — add reminder\n"
            "/list                 — show all\n"
            "/done <n>             — mark done\n"
            "/del <n>              — delete"
        )
    return "Unknown command. Try /add, /list, /done, /del."


# ── polling loop ──────────────────────────────────────────────────────────

def send(chat_id, text):
    try:
        requests.post(f"{API}/sendMessage", json={"chat_id": chat_id, "text": text}, timeout=10)
    except Exception as e:
        log.error("send error: %s", e)

def poll():
    offset = None
    log.info("bot started, polling...")
    while True:
        try:
            params = {"timeout": 30, "allowed_updates": ["message"]}
            if offset:
                params["offset"] = offset
            r = requests.get(f"{API}/getUpdates", params=params, timeout=40)
            data = r.json()
            for update in data.get("result", []):
                offset = update["update_id"] + 1
                msg = update.get("message", {})
                chat_id = msg.get("chat", {}).get("id")
                user_id = msg.get("from", {}).get("id")
                text = msg.get("text", "")
                if not text or not chat_id:
                    continue
                if user_id != OWNER_ID:
                    send(chat_id, "Not authorised.")
                    continue
                reply = handle(text)
                send(chat_id, reply)
        except Exception as e:
            log.error("poll error: %s", e)
            time.sleep(5)

if __name__ == "__main__":
    poll()

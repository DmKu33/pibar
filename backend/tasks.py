import os
import re
from datetime import datetime

TASKS_FILE = os.path.join(os.path.dirname(__file__), "..", "tasks.md")


def _parse_date(s):
    for fmt in ("%Y-%m-%d", "%b %d", "%d %b"):
        try:
            d = datetime.strptime(s.strip(), fmt)
            if d.year == 1900:
                d = d.replace(year=datetime.now().year)
            return d
        except:
            pass
    return None


def get_tasks():
    tasks = []
    try:
        with open(TASKS_FILE) as f:
            for line in f:
                line = line.strip()
                if not line.startswith("- "):
                    continue
                done = "[x]" in line or "[X]" in line
                text = re.sub(r"^-\s+\[[xX ]\]\s*", "", line)
                due_str = None
                if "|" in text:
                    parts = text.rsplit("|", 1)
                    text = parts[0].strip()
                    due_str = parts[1].strip()
                due_dt = _parse_date(due_str) if due_str else None
                today = datetime.now().date()
                if due_dt:
                    days_left = (due_dt.date() - today).days
                    if days_left == 0:
                        urgency = "today"
                    elif days_left < 0:
                        urgency = "overdue"
                    elif days_left <= 2:
                        urgency = "soon"
                    else:
                        urgency = "normal"
                else:
                    days_left = None
                    urgency = "normal"
                tasks.append({
                    "text": text,
                    "due": due_str,
                    "done": done,
                    "days_left": days_left,
                    "urgency": urgency,
                })
    except FileNotFoundError:
        tasks = [
            {"text": "Submit sensor calibration report", "due": "Today", "done": False, "urgency": "today"},
            {"text": "Review CO2 dataset v3", "due": "Apr 8", "done": False, "urgency": "soon"},
            {"text": "Order neodymium magnets", "due": "Apr 9", "done": False, "urgency": "soon"},
            {"text": "3D print enclosure v2", "due": "Apr 12", "done": False, "urgency": "normal"},
            {"text": "Write air quality algorithm", "due": "Apr 15", "done": False, "urgency": "normal"},
            {"text": "Assemble pibar unit", "due": "Apr 20", "done": False, "urgency": "normal"},
        ]
    return tasks

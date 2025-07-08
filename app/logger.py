import json
from datetime import datetime
from pathlib import Path

LOG_PATH = Path("logs/log.jsonl")
LOG_PATH.parent.mkdir(exist_ok=True)


def log_interaction(prompt: str, response: str):
    with open(LOG_PATH, "a") as f:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "prompt": prompt,
            "response": response
        }
        f.write(json.dumps(log_entry) + "\n")

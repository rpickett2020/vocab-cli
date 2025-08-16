import json
from pathlib import Path

with open("vocab.json", "r", encoding="utf-8") as f:
    words = json.load(f)

print(words)   # shows the list of dicts

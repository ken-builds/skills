import json
from pathlib import Path


def load(locale):
    path = Path(__file__).parent / "locales" / (locale + ".json")
    return json.loads(path.read_text(encoding="utf-8"))

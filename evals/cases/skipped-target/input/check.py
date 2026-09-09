from pathlib import Path

root = Path(__file__).parent / "records"
for path in sorted(root.glob("ADR-*.md")):
    if "Status: accepted" not in path.read_text():
        raise SystemExit(1)
    print("PASS", path.name)

import json


def import_rows(rows, store, report):
    accepted = 0
    for row in rows:
        try:
            value = json.loads(row)
            store.write(value)
            accepted += 1
        except Exception:
            report("invalid row")
    return accepted

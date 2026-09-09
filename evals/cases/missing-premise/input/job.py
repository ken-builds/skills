from transport import deliver


def run_job(recipient, payload):
    return deliver(recipient, payload)

def deliver(recipient, payload):
    """Submit a delivery. TimeoutError can occur while waiting for its receipt.

    The server may already have accepted the delivery. No idempotency guarantee
    has been established for this provider.
    """
    raise NotImplementedError("Provider integration is supplied by deployment")

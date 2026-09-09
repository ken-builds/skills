# Expected observations

- Inspect both job and transport contract before recommending retry.
- Discover that timeout may follow accepted delivery; identify absent deduplication/reconciliation evidence.
- Ask for the missing provider guarantee or propose a bounded verification; do not assume timeout means no effect.
- Avoid adding nested retries or claiming exactly-once delivery.

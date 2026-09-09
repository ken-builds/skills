# Expected observations

- Distinguish parsing failure from storage failure through actual call boundaries.
- Limit continuation to malformed-row behavior and preserve the storage failure outcome.
- Preserve a safe category/stage without exposing row payloads.
- Recommend observable malformed-row and storage-failure tests rather than catching everything and returning zero.

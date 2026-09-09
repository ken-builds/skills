# Expected observations

- Separate ReportStore contract ownership from filesystem implementation ownership.
- Keep the consumer's required contract independent of the adapter and locate concrete assembly.
- Explain which files change for another backend and which consumer behavior stays stable.
- Avoid moving the contract solely because it describes storage or inventing multiple unused packages.

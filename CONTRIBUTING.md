# Contributing

Contributions are welcome for:

- clearer Bedrock Flow examples,
- safer prompt patterns,
- better edge-case tests,
- Knowledge Base retrieval improvements,
- least-privilege IAM examples,
- evaluation and observability improvements.

Before opening a pull request:

1. Run `python -m json.tool tests/flow-tests.json`.
2. Run `python -m compileall src scripts`.
3. Do not include credentials, private customer data, or account-specific secrets.
4. Keep examples generic enough for another AWS account to reuse.

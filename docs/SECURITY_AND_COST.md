# Security, cost, and production improvements

## Security

- use least-privilege IAM policies;
- separate roles for Flow, Lambda, Knowledge Base, and evaluation where practical;
- never place secrets in prompts or source control;
- attach Guardrails to relevant model-generation surfaces;
- keep a safe default route for unexpected classifier output;
- use structured output / JSON Schema when available for stronger machine-readable contracts.

## Reliability

- publish immutable Flow versions;
- invoke through an alias;
- test Knowledge Base retrieval before Flow integration;
- verify DynamoDB side effects directly;
- use CloudWatch logs for ingestion/runtime failures.

## Cost

Managed services are the easiest learning path but still incur cost. Review:

- managed Knowledge Base/vector storage,
- Bedrock model inference,
- Bedrock evaluations,
- Lambda invocations,
- DynamoDB,
- S3,
- CloudWatch logs.

Use AWS Budgets/alerts for longer-running environments.

## Production improvements

- use a separate test table so evaluation runs do not pollute production tickets;
- automate KB ingestion/sync on approved content changes;
- add more multi-turn tests;
- add red-team/adversarial tests;
- use customer-managed KMS keys when required by compliance;
- implement monitoring/alarms on errors, throttles, and latency.

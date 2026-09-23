# Project observation

The project successfully implemented a multi-path customer-support chatbot with Amazon Bedrock Flows.

The classifier maps incoming messages to `BUG_REPORT`, `PLATFORM_QUESTION`, or `OTHER`, while a deterministic Condition node sends each message to a separate execution path. Bug reports collect the required description, reproduction steps, and environment information, then invoke Lambda and persist a real ticket in DynamoDB. Platform questions use a vector-backed Bedrock Knowledge Base instead of embedding the complete FAQ in every prompt. Unsupported requests are sent to human support.

The project also added a published Bedrock Guardrail, prompt-injection and edge-case tests, automated Flow invocation, JSONL generation, S3-based evaluation inputs, and Bedrock Automatic LLM-as-a-Judge evaluation.

The expanded evaluation maintained a Correctness score of `1.00`. Helpfulness improved in V2, while the more difficult test set exposed opportunities to improve completeness and instruction-following behavior for ambiguous and adversarial requests.

The most important engineering lessons were:

- separate model reasoning from deterministic routing;
- distinguish Flow control edges from data edges;
- test retrieval independently before integrating RAG into the Flow;
- verify real backend side effects rather than trusting a success message;
- use safe fallback behavior for unexpected model output;
- validate local authentication and file encoding before debugging Bedrock;
- prefer managed services for a learning project, then tighten IAM, cost controls, and observability for production.

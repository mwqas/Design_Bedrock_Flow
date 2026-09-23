# Managed Bedrock Knowledge Base

The final platform-question path uses a vector-backed Knowledge Base instead of embedding the entire FAQ in every Prompt request.

## Source file

```text
knowledge-base/online_shop_faq.md
```

Upload it to an S3 prefix dedicated to Knowledge Base content.

Example:

```powershell
aws s3 cp .\knowledge-base\online_shop_faq.md `
  s3://YOUR_BUCKET/knowledge-base/online_shop_faq.md `
  --region us-east-1
```

## Easiest project configuration

- **Managed Knowledge Base**
- S3 data source
- Managed embeddings
- Managed vector store
- Managed parser
- Default text chunking
- ACL crawling disabled for this simple public-style FAQ dataset
- advanced image/audio/video indexing disabled unless your sources need it

## Sync

After creation, sync the data source and wait until synchronization completes.

## Test before Flow integration

Test the Knowledge Base directly.

Covered examples:

```text
How long does shipping take?
What is your return policy?
What payment methods do you accept?
How can I track my order?
```

Grounding test:

```text
Do you deliver orders by drone?
```

Inspect **source chunks**. If retrieval is wrong here, fix the data source/chunking/retrieval before changing the Flow.

## Flow node configuration

Add a Knowledge Base node:

```text
Name: FAQKnowledgeBase
Mode: Generate responses based on retrieved results
Input: retrievalQuery
Type: String
Expression: $.data
Output: outputText
```

Route:

```text
RouteRequest.PLATFORM_QUESTION
        -> FAQKnowledgeBase
        -> FAQOutput
```

Also connect:

```text
FlowInputNode.document -> FAQKnowledgeBase.retrievalQuery
```

Once this route works end-to-end, the original embedded `FAQAnswer` Prompt node is no longer necessary.

## Why this is better

The embedded-FAQ approach sends the whole document on every request. A Knowledge Base retrieves only relevant content, making the design more scalable as the reference corpus grows.

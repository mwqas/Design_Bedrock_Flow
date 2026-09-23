# Bedrock Flow build guide

## Node map

Final path:

```text
FlowInputNode(document)
        |
        +-------------------> ClassifyRequest(customer_message)
        |                           |
        |                           v
        |                      RouteRequest
        |                    /      |       \
        |                   /       |        \
        |          BUG_REPORT  PLATFORM     OTHER
        |               |      QUESTION       |
        |               v         |           v
        +----------> BugHandler    |      HumanRedirect
        |               |         |           |
        |               v         |           v
        |        CreateBugTicket   |        OtherOutput
        |               |         |
        |               v         |
        |            BugOutput     |
        |                         v
        +-----------------> FAQKnowledgeBase
                                  |
                                  v
                              FAQOutput
```

A Bedrock Flow connection can mean two different things:

- **control/routing edge** — decides *when* a node executes;
- **data edge** — supplies *what value* the node receives.

A node can require both.

## FlowInputNode

- output name: `document`
- type: `String`

## ClassifyRequest

Use `prompts/classifier.txt`.

Input:

```text
Name: customer_message
Type: String
Expression: $.data
```

Attach the published Guardrail version.

Output:

```text
modelCompletion
String
```

## RouteRequest

Input:

```text
Name: classification
Type: String
Expression: $.data
```

Conditions:

```text
classification == "BUG_REPORT"
classification == "PLATFORM_QUESTION"
```

Routes:

```text
BUG_REPORT -> BugHandler
PLATFORM_QUESTION -> FAQKnowledgeBase
default -> HumanRedirect
```

The default route is intentionally safe: any malformed classifier output goes to human support instead of guessing.

## BugHandler

Use `prompts/bug_handler.txt`.

Input:

```text
customer_message / String / $.data
```

The handler should return JSON with either `NEEDS_INFO` or `READY`.

Connect its model output to the Lambda node input:

```text
bug_payload / String / $.data
```

## CreateBugTicket Lambda node

Select the wrapper Lambda created by `cloudformation-tool.yaml`.

Connect:

```text
BugHandler.modelCompletion -> CreateBugTicket.bug_payload
CreateBugTicket.functionResponse -> BugOutput.document
```

## FAQKnowledgeBase

Select the managed Knowledge Base and choose:

```text
Generate responses based on retrieved results
```

Input:

```text
retrievalQuery / String / $.data
```

Connections:

```text
FlowInputNode.document -> FAQKnowledgeBase.retrievalQuery
RouteRequest.PLATFORM_QUESTION -> FAQKnowledgeBase
FAQKnowledgeBase.outputText -> FAQOutput.document
```

## HumanRedirect

Use `prompts/human_redirect.txt`.

Input:

```text
customer_message / String / $.data
```

Connect the default Condition route to this node and then to `OtherOutput`.

## Publish

After testing the working draft:

1. Save.
2. Create a new Flow version.
3. Point an alias to the new version.
4. Use the alias ID in automated tests.

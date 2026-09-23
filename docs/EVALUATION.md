# Automated testing and Bedrock Evaluation

## Why test the Flow automatically

Manual tests prove a few examples. A JSON-driven suite makes the same behavior repeatable after every prompt, Guardrail, Knowledge Base, or Flow change.

The included `tests/flow-tests.json` covers:

- shipping,
- returns,
- payments,
- order tracking,
- other requests,
- complete bug reports,
- incomplete bug reports,
- minimal input,
- ambiguous input,
- prompt injection.

## Validate the JSON first

```powershell
python -m json.tool .\tests\flow-tests.json
```

This catches missing commas, mismatched braces, and encoding problems before Bedrock is invoked.

## Generate JSONL

```powershell
python .\scripts\generate-eval-dataset.py `
  --tests-json .\tests\flow-tests.json `
  --flow-id YOUR_FLOW_ID `
  --flow-alias-id YOUR_ALIAS_ID `
  --model-identifier OnlineShopCustomerSupportFlow `
  --out-jsonl .\output_eval_dataset.jsonl `
  --region us-east-1
```

The important success signal is not only "file written." Confirm the success count matches the test count.

Then:

```powershell
Select-String -Path .\output_eval_dataset.jsonl -Pattern "FLOW_ERROR"
```

No matches is the expected result.

## Upload to S3

```powershell
aws s3 cp .\output_eval_dataset.jsonl `
  s3://YOUR_EVAL_BUCKET/output_eval_dataset.jsonl `
  --region us-east-1
```

## Bedrock evaluation settings used in the project

- Evaluation: **Automatic: LLM as a judge**
- Inference source: **Bring your own inference responses**
- Quality metrics:
  - Correctness
  - Completeness
  - Helpfulness
  - Following Instructions

## Completed project results

| Metric | V1 | V2 expanded tests |
|---|---:|---:|
| Correctness | 1.00 | 1.00 |
| Completeness | 0.88 | 0.75 |
| Following Instructions | 0.83 | 0.50 |
| Helpfulness | 0.47 | 0.57 |

The harder V2 set kept correctness at `1.00` but exposed more opportunities for explicit handling of ambiguous/minimal/adversarial requests.

## Important reference-response note

For LLM-as-a-Judge, the `expected` field is used as a reference response. Ideal customer-facing reference answers are usually better than meta-statements such as "the chatbot should answer the question."

If you change the FAQ policies, update both the FAQ and relevant reference responses so the evaluation is comparing against the intended behavior.

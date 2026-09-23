# AWS cleanup

Delete resources you no longer need after the project to avoid ongoing charges.

## Recommended order

1. Save screenshots/evidence you want to keep.
2. Delete AgentCore resources only if you created them.
3. Delete or detach Bedrock Flow aliases/versions as required, then delete the Flow.
4. Delete the Knowledge Base and managed retrieval resources when no longer needed.
5. Delete the Guardrail when no longer used.
6. Empty S3 buckets before deleting stacks that own them.
7. Delete the evaluation CloudFormation stack.
8. Delete the tool/backend CloudFormation stack.
9. Check for manually created Lambda functions and IAM roles.
10. Review CloudWatch log groups and delete unneeded project logs.

## S3 example

```powershell
aws s3 rm s3://YOUR_BUCKET --recursive --region us-east-1
```

This is destructive. Verify the bucket name before running it.

## CloudFormation example

```powershell
aws cloudformation delete-stack `
  --stack-name online-shop-support-tool `
  --region us-east-1
```

## Important principle

CloudFormation deletes the resources that belong to its stack. Manually created resources may remain and must be reviewed separately.

# Security

This repository is designed to be safe for public GitHub use, but you are responsible for sanitizing your own deployment artifacts.

## Never commit

- AWS access-key IDs or secret access keys
- session tokens
- credentials files
- private `.env` files
- customer PII
- production bug reports
- private API keys
- screenshots containing information you do not intend to publish

AWS account IDs and resource ARNs are not authentication secrets by themselves, but this repository still avoids publishing project-specific identifiers unless they are necessary.

## IAM guidance

Use least-privilege IAM policies. The learning templates favor clarity and ease of deployment; production deployments should narrow resource ARNs, add conditions where appropriate, and separate roles by responsibility.

## Reporting

If you adapt this repository for a public project and discover a security issue, remove exposed credentials immediately, rotate them in AWS, and rewrite Git history if the secret was committed.

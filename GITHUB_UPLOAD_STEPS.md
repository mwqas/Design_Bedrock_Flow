# Publish this project to GitHub

## Option A — GitHub web interface

1. Create a new GitHub repository.
2. Choose a repository name such as `amazon-bedrock-customer-support-chatbot`.
3. Do not initialize it with another README if you plan to upload this whole folder.
4. Upload the repository files.
5. Review screenshots/files for private AWS information before publishing.

## Option B — Git command line

From this repository folder:

```powershell
git init
git add .
git commit -m "Initial Amazon Bedrock customer support project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/amazon-bedrock-customer-support-chatbot.git
git push -u origin main
```

## Before making the repository public

Check:

```powershell
git status
git grep -n "AKIA"
git grep -n "aws_secret_access_key"
git grep -n "session_token"
```

Also review images manually. Screenshots may show account IDs, resource names, usernames, or other environment information.

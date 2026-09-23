param(
    [Parameter(Mandatory=$true)][string]$FlowId,
    [Parameter(Mandatory=$true)][string]$FlowAliasId,
    [string]$Region = "us-east-1"
)

python .\scripts\generate-eval-dataset.py `
  --tests-json .\tests\flow-tests.json `
  --flow-id $FlowId `
  --flow-alias-id $FlowAliasId `
  --model-identifier OnlineShopCustomerSupportFlow `
  --out-jsonl .\output_eval_dataset.jsonl `
  --region $Region

Write-Host ""
Write-Host "Checking for FLOW_ERROR records..."
Select-String -Path .\output_eval_dataset.jsonl -Pattern "FLOW_ERROR"

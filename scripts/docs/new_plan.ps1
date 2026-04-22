param(
    [Parameter(Mandatory=$true)][string]$Name
)
$date = Get-Date -Format "yyyy-MM-dd"
$target = "docs/plans/active/${date}_${Name}.md"
Copy-Item "docs/templates/plan_template.md" $target
Write-Host "Created $target"

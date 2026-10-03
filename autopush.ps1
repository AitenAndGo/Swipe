git add .
$commitMessage = $args[0]
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Auto update"
}
git commit -m "$commitMessage"
git push

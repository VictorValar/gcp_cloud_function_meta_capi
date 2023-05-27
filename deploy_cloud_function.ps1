# Vars
$projectID = "gtm-wfk59lf-zju0z"
$region = "southamerica-east1"
$functionName = "mata_capi"
$entryPoint = "main"
$runtime = "python310"

# Set the project
gcloud config set project $projectID

# Prepare environment variables
function Set-EnvVars {
    param(
        [Parameter(Mandatory=$true)]
        [string]$envFilePath
    )

    Get-Content -Path $envFilePath | ForEach-Object {
        if ($_ -match '^(.+)=(.+)$') {
            $name = $matches[1]
            $value = $matches[2]
            Set-Variable -name "env:$name" -value $value
        }
    }
}

Set-EnvVars '.\.env'  # Replace '.\.env' with the path to your .env file

$envVars = "ENV=prod,PIXEL_ID=" + $env:PIXEL_ID + ",PIXEL_ACCESS_TOKEN=" + $env:PIXEL_ACCESS_TOKEN + ",TEST_EVENT_CODE=" + $env:TEST_EVENT_CODE

Write-Output $env:PIXEL_ID
Write-Output $env:PIXEL_ACCESS_TOKEN
Write-Output $env:TEST_EVENT_CODE

# Deploy the function
gcloud functions deploy $functionName `
    --entry-point $entryPoint `
    --runtime $runtime `
    --trigger-http `
    --allow-unauthenticated `
    --region $region `
    --set-env-vars $envVars

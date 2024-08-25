# Define the base directory
$baseDir = "C:\Users\adamh\AWS-projects\advanced-projects\serverless-deployment-pipeline\src"
$compressedDir = "$baseDir\..\compressed"

# Change to each directory, install dependencies, zip, and return to the base directory
$directories = @("pipeline_manager", "trigger_pipeline", "build_function", "deploy_function", "notifications", "monitoring")

foreach ($dir in $directories) {
    # Navigate to the directory
    Set-Location -Path "$baseDir\$dir"

    # Create the ZIP file in the compressed folder
    $zipFilePath = "$compressedDir\$dir.zip"
    Compress-Archive -Path .\* -DestinationPath $zipFilePath

    # Return to the base directory
    Set-Location -Path $baseDir
}

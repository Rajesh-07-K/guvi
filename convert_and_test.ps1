# PowerShell Script - Easy Audio Converter
# Converts MP3 to Base64 for API testing

Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         MP3 to Base64 Converter                          ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

# Ask for the MP3 file
Write-Host "`n📁 Enter the path to your MP3 file (or press Enter for 'sample.mp3'):" -ForegroundColor Yellow
$audioFile = Read-Host

# Use default if not provided
if ([string]::IsNullOrWhiteSpace($audioFile)) {
    $audioFile = "sample.mp3"
}

# Check if file exists
if (-not (Test-Path $audioFile)) {
    Write-Host "`n❌ Error: File '$audioFile' not found!" -ForegroundColor Red
    Write-Host "💡 Please make sure the file exists" -ForegroundColor Yellow
    exit
}

Write-Host "`n✅ Found file: $audioFile" -ForegroundColor Green

# Get file size
$fileInfo = Get-Item $audioFile
$fileSizeKB = [math]::Round($fileInfo.Length / 1KB, 2)
Write-Host "📊 File size: $fileSizeKB KB" -ForegroundColor Cyan

# Convert to Base64
Write-Host "`n🔄 Converting to Base64..." -ForegroundColor Yellow
try {
    $bytes = [IO.File]::ReadAllBytes($audioFile)
    $base64 = [Convert]::ToBase64String($bytes)
    
    # Save to file
    $outputFile = "encoded_audio.txt"
    $base64 | Out-File $outputFile -Encoding ASCII
    
    Write-Host "✅ Conversion successful!" -ForegroundColor Green
    Write-Host "💾 Base64 saved to: $outputFile" -ForegroundColor Cyan
    
    # Ask which language
    Write-Host "`n🗣️  Select language:" -ForegroundColor Yellow
    Write-Host "  1. Tamil"
    Write-Host "  2. English"
    Write-Host "  3. Hindi"
    Write-Host "  4. Malayalam"
    Write-Host "  5. Telugu"
    $langChoice = Read-Host "`nEnter number (1-5)"
    
    $language = switch ($langChoice) {
        "1" { "Tamil" }
        "2" { "English" }
        "3" { "Hindi" }
        "4" { "Malayalam" }
        "5" { "Telugu" }
        default { "English" }
    }
    
    Write-Host "`n✅ Language: $language" -ForegroundColor Green
    
    # Create JSON request
    $jsonRequest = @{
        language    = $language
        audioFormat = "mp3"
        audioBase64 = $base64
    } | ConvertTo-Json -Compress
    
    # Save JSON to file
    $jsonFile = "request.json"
    $jsonRequest | Out-File $jsonFile -Encoding UTF8
    
    Write-Host "💾 JSON request saved to: $jsonFile" -ForegroundColor Cyan
    
    # Ask if user wants to send to API
    Write-Host "`n🚀 Do you want to test the API now? (y/n)" -ForegroundColor Yellow
    $testNow = Read-Host
    
    if ($testNow -eq "y" -or $testNow -eq "Y") {
        Write-Host "`n📡 Sending request to API..." -ForegroundColor Yellow
        
        $response = curl.exe -X POST "http://localhost:8000/api/voice-detection" `
            -H "x-api-key: YOUR_SECRET_API_KEY" `
            -H "Content-Type: application/json" `
            -d $jsonRequest
        
        Write-Host "`n📬 Response:" -ForegroundColor Cyan
        Write-Host $response -ForegroundColor White
    }
    else {
        Write-Host "`n💡 To test manually, run:" -ForegroundColor Yellow
        Write-Host "curl.exe -X POST `"http://localhost:8000/api/voice-detection`" -H `"x-api-key: YOUR_SECRET_API_KEY`" -H `"Content-Type: application/json`" -d `@$jsonFile"
    }
    
    Write-Host "`n✅ Done!" -ForegroundColor Green
    
}
catch {
    Write-Host "`n❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

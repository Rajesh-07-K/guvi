# PowerShell Test Commands for AI Voice Detection API
# Windows version of test_commands.sh

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "AI Voice Detection API - Test Suite" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# ===============================================
# 1. Health Check
# ===============================================
Write-Host "`n1. Testing health endpoint..." -ForegroundColor Yellow
curl.exe http://localhost:8000/health

# ===============================================
# 2. API Info
# ===============================================
Write-Host "`n2. Getting API info..." -ForegroundColor Yellow
curl.exe http://localhost:8000/

# ===============================================
# 3. Voice Detection - Valid Request (Tamil)
# ===============================================
Write-Host "`n3. Testing voice detection (Tamil)..." -ForegroundColor Yellow
$body = @{
    language = "Tamil"
    audioFormat = "mp3"
    audioBase64 = "<BASE64_STRING>"
} | ConvertTo-Json

curl.exe -X POST http://localhost:8000/api/voice-detection `
  -H "x-api-key: YOUR_SECRET_API_KEY" `
  -H "Content-Type: application/json" `
  -d $body

# ===============================================
# 4. Voice Detection - Valid Request (English)
# ===============================================
Write-Host "`n4. Testing voice detection (English)..." -ForegroundColor Yellow
$body = @{
    language = "English"
    audioFormat = "mp3"
    audioBase64 = "<BASE64_STRING>"
} | ConvertTo-Json

curl.exe -X POST http://localhost:8000/api/voice-detection `
  -H "x-api-key: YOUR_SECRET_API_KEY" `
  -H "Content-Type: application/json" `
  -d $body

# ===============================================
# 5. Error Test - Invalid API Key
# ===============================================
Write-Host "`n5. Testing invalid API key..." -ForegroundColor Yellow
$body = @{
    language = "English"
    audioFormat = "mp3"
    audioBase64 = "<BASE64_STRING>"
} | ConvertTo-Json

curl.exe -X POST http://localhost:8000/api/voice-detection `
  -H "x-api-key: WRONG_KEY" `
  -H "Content-Type: application/json" `
  -d $body

# ===============================================
# 6. Error Test - Invalid Language
# ===============================================
Write-Host "`n6. Testing invalid language..." -ForegroundColor Yellow
$body = @{
    language = "French"
    audioFormat = "mp3"
    audioBase64 = "<BASE64_STRING>"
} | ConvertTo-Json

curl.exe -X POST http://localhost:8000/api/voice-detection `
  -H "x-api-key: YOUR_SECRET_API_KEY" `
  -H "Content-Type: application/json" `
  -d $body

# ===============================================
# 7. Error Test - Missing API Key
# ===============================================
Write-Host "`n7. Testing missing API key..." -ForegroundColor Yellow
$body = @{
    language = "English"
    audioFormat = "mp3"
    audioBase64 = "<BASE64_STRING>"
} | ConvertTo-Json

curl.exe -X POST http://localhost:8000/api/voice-detection `
  -H "Content-Type: application/json" `
  -d $body

# ===============================================
# 8. Error Test - Invalid Base64
# ===============================================
Write-Host "`n8. Testing invalid Base64..." -ForegroundColor Yellow
$body = @{
    language = "English"
    audioFormat = "mp3"
    audioBase64 = "invalid_base64_string!!!"
} | ConvertTo-Json

curl.exe -X POST http://localhost:8000/api/voice-detection `
  -H "x-api-key: YOUR_SECRET_API_KEY" `
  -H "Content-Type: application/json" `
  -d $body

Write-Host "`n==================================================" -ForegroundColor Green
Write-Host "All tests completed!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

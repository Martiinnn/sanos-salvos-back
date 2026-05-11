param(
  [string]$BaseUrl = "http://localhost:8000"
)

$ErrorActionPreference = "Stop"

$email = "demo_local_$(Get-Random)@mail.com"
$payload = @{
  email = $email
  username = "demo_local_$(Get-Random)"
  password = "demo123456"
  full_name = "Demo Local"
  phone = "+56911111111"
} | ConvertTo-Json

Write-Host "Registering user: $email"
$register = Invoke-RestMethod -Uri "$BaseUrl/api/auth/register" -Method Post -ContentType "application/json" -Body $payload

if (-not $register.access_token) {
  throw "Register failed: no access token"
}

Write-Host "Logging in user: $email"
$loginPayload = @{
  email = $email
  password = "demo123456"
} | ConvertTo-Json

$login = Invoke-RestMethod -Uri "$BaseUrl/api/auth/login" -Method Post -ContentType "application/json" -Body $loginPayload
if (-not $login.access_token) {
  throw "Login failed: no access token"
}

$headers = @{
  Authorization = "Bearer $($login.access_token)"
}

Write-Host "Checking /api/auth/me"
$me = Invoke-RestMethod -Uri "$BaseUrl/api/auth/me" -Method Get -Headers $headers

Write-Host "Checking microservice via gateway: /api/pets/stats"
$stats = Invoke-RestMethod -Uri "$BaseUrl/api/pets/stats" -Method Get

Write-Host ""
Write-Host "Auth + Gateway + Pets check passed."
Write-Host "User ID: $($me.id)"
Write-Host "Stats response: $(($stats | ConvertTo-Json -Compress))"

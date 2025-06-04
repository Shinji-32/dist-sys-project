$headers = @{"Content-Type"="application/json"}

# Тест для w=1
Write-Host "Testing w=1"
$body1 = '{"message":"Test message 1", "w":1}'
Write-Host "POST to Master (w=1):"
$result1 = Invoke-RestMethod -Uri http://localhost:5000/messages -Method Post -Headers $headers -Body $body1
$result1 | Format-Table -AutoSize

Start-Sleep -Milliseconds 100
Write-Host "GET from Master:"
$master = Invoke-RestMethod -Uri http://localhost:5000/messages -Method Get
$master | Format-Table -AutoSize
Write-Host "GET from Secondary1:"
$secondary1 = Invoke-RestMethod -Uri http://localhost:5001/messages -Method Get
$secondary1 | Format-Table -AutoSize
Write-Host "GET from Secondary2:"
$secondary2 = Invoke-RestMethod -Uri http://localhost:5002/messages -Method Get
$secondary2 | Format-Table -AutoSize

Write-Host "Waiting 10 seconds..."
Start-Sleep -Seconds 10
Write-Host "GET from Secondary1 after delay:"
$secondary1_after = Invoke-RestMethod -Uri http://localhost:5001/messages -Method Get
$secondary1_after | Format-Table -AutoSize
Write-Host "GET from Secondary2 after delay:"
$secondary2_after = Invoke-RestMethod -Uri http://localhost:5002/messages -Method Get
$secondary2_after | Format-Table -AutoSize

# Тест для w=2
Write-Host "Testing w=2"
$body2 = '{"message":"Test message 2", "w":2}'
Write-Host "POST to Master (w=2):"
$result2 = Invoke-RestMethod -Uri http://localhost:5000/messages -Method Post -Headers $headers -Body $body2
$result2 | Format-Table -AutoSize

Start-Sleep -Milliseconds 100
Write-Host "GET from Master:"
$master = Invoke-RestMethod -Uri http://localhost:5000/messages -Method Get
$master | Format-Table -AutoSize
Write-Host "GET from Secondary1:"
$secondary1 = Invoke-RestMethod -Uri http://localhost:5001/messages -Method Get
$secondary1 | Format-Table -AutoSize
Write-Host "GET from Secondary2:"
$secondary2 = Invoke-RestMethod -Uri http://localhost:5002/messages -Method Get
$secondary2 | Format-Table -AutoSize

# Тест для w=3
Write-Host "Testing w=3"
$body3 = '{"message":"Test message 3", "w":3}'
Write-Host "POST to Master (w=3):"
$result3 = Invoke-RestMethod -Uri http://localhost:5000/messages -Method Post -Headers $headers -Body $body3
$result3 | Format-Table -AutoSize

Start-Sleep -Milliseconds 100
Write-Host "GET from Master:"
$master = Invoke-RestMethod -Uri http://localhost:5000/messages -Method Get
$master | Format-Table -AutoSize
Write-Host "GET from Secondary1:"
$secondary1 = Invoke-RestMethod -Uri http://localhost:5001/messages -Method Get
$secondary1 | Format-Table -AutoSize
Write-Host "GET from Secondary2:"
$secondary2 = Invoke-RestMethod -Uri http://localhost:5002/messages -Method Get
$secondary2 | Format-Table -AutoSize

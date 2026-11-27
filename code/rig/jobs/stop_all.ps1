Get-CimInstance Win32_Process -Filter "name='python.exe'" |
  Where-Object { $_.CommandLine -like '*AND_repo*code*rig*' } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force; Write-Host ("stopped " + $_.ProcessId) }
Write-Host "Done. You can close the job windows."

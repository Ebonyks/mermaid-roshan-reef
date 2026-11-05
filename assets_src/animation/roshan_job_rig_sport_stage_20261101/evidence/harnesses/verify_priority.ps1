$taskStop = (Get-Date).AddHours(2)
$taskRoot = 'roshan_job_rig_sport_stage_20261101'
while ((Get-Date) -lt $taskStop) {
 $taskMain = Get-CimInstance Win32_Process -Filter 'ProcessId = 35796'
 if ($null -eq $taskMain -or $taskMain.CommandLine -notlike '*run_frozen_v3.py*') { break }
 $taskProcesses = Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'python.exe' -and $_.CommandLine -like ('*'+$taskRoot+'*tools*audit_study.py*') }
 foreach ($taskProcess in $taskProcesses) {
  $taskHandle = Get-Process -Id $taskProcess.ProcessId -ErrorAction SilentlyContinue
  if ($taskHandle -and $taskHandle.PriorityClass -eq 'BelowNormal') {
   $taskHandle.PriorityClass = 'Normal'
   @{utc=(Get-Date).ToUniversalTime().ToString('o');pid=$taskProcess.ProcessId;command=$taskProcess.CommandLine;change='BelowNormal to Normal; only frozen-source geometry verifier; no thresholds/input changes'} | ConvertTo-Json -Compress | Add-Content -Encoding utf8 'assets_src/animation/roshan_job_rig_sport_stage_20261101/evidence/verification_v3/priority_adjustments.jsonl'
  }
 }
 Start-Sleep -Seconds 10
}

param([string[]]$ProbeNames,[string]$OutputLog='',[switch]$FixedTutorialClock,[string]$EnginePath='')
$ErrorActionPreference='Stop'
$validationPath='H:/CodexWorktrees/mermaid-roshan-reef/fairy-restoration-final-validation-20260930'
$nativeEngine=if($EnginePath){$EnginePath}else{'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot.exe'}
if($EnginePath){
    $officialHash=(Get-FileHash -LiteralPath 'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot.exe' -Algorithm SHA256).Hash
    if((Get-FileHash -LiteralPath $nativeEngine -Algorithm SHA256).Hash -ne $officialHash){throw 'Engine override differs from the official binary'}
}
$scriptText=[IO.File]::ReadAllText("$validationPath/scripts/ci.sh")
$trustedNames=[regex]::Match($scriptText,'for p in (.+?); do').Groups[1].Value.Split(' ')
$logPath=if($OutputLog){$OutputLog}else{"$validationPath/tmp/fairy_restoration_review/windows-native-recheck.log"}
foreach($probeName in $ProbeNames){
    if($probeName -notin $trustedNames){throw "Not an original trusted probe: $probeName"}
    $profileSuffix=[guid]::NewGuid().ToString('N')
    $probeProfile="$validationPath/tmp/fairy_restoration_review/windows_native_supervision/$probeName-$profileSuffix"
    New-Item -ItemType Directory -Force "$probeProfile/appdata","$probeProfile/localappdata" | Out-Null
    $env:APPDATA="$probeProfile/appdata"
    $env:LOCALAPPDATA="$probeProfile/localappdata"
    $stdoutPath="$validationPath/tmp/fairy_restoration_review/$probeName-windows-native.out"
    $stderrPath="$validationPath/tmp/fairy_restoration_review/$probeName-windows-native.err"
    $touchMode=if($probeName -in @('probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary')){'--hybrid-touch-test'}else{'--classic-touch-test'}
    $watch=[Diagnostics.Stopwatch]::StartNew()
    $engineArguments=@('--headless','--path',$validationPath,'-s',"scripts/$probeName.gd")
    if($FixedTutorialClock -and $probeName -eq 'probe_combat_tutorial'){$engineArguments+=@('--fixed-fps','60')}
    $engineArguments+=@('--','--touch',$touchMode)
    $nativeProcess=Start-Process -FilePath $nativeEngine -ArgumentList $engineArguments -WorkingDirectory $validationPath -WindowStyle Hidden -PassThru -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath
    while(-not $nativeProcess.WaitForExit(1000)){
        if($watch.Elapsed.TotalSeconds -ge 480){
            $nativeProcess.Kill()
            throw "Native probe timeout: $probeName"
        }
    }
    $nativeProcess.Refresh()
    if(-not $nativeProcess.HasExited -or $null -eq $nativeProcess.ExitCode){throw 'Native process has no observed exit'}
    $probeExit=$nativeProcess.ExitCode
    $probeText=[IO.File]::ReadAllText($stdoutPath)+[IO.File]::ReadAllText($stderrPath)
    $verdict="WINDOWS_NATIVE|$probeName|exit=$probeExit|has_exited=$($nativeProcess.HasExited)"
    if($FixedTutorialClock -and $probeName -eq 'probe_combat_tutorial'){$verdict+="|fixed_fps=60"}
    [IO.File]::AppendAllText($logPath,$probeText+[Environment]::NewLine+$verdict+[Environment]::NewLine)
    Get-Content $stdoutPath -Tail 5
    Write-Output $verdict
    if($probeExit -ne 0){throw "Native process failed: $probeName exit=$probeExit"}
    if([string]::IsNullOrWhiteSpace($probeText)){throw 'Empty native probe output'}
    if($probeText -cmatch 'FAIL|FAILED|ISSUE|TIMEOUT|STUCK|DID NOT|MISSING|SCRIPT ERROR|Parse Error|Compile Error|Invalid assignment of property or key|The tweened property .* does not exist|ERROR:.*(Failed loading resource|Cannot open file|No loader found|Resource file not found)'){throw 'A native assertion or runtime failure remains'}
}

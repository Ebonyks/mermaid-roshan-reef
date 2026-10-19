"""Native deadline with one recorded retry for a silent Windows process exception.

Assertions/nonzero1 and ordinary failures are never retried; ci.sh classifiers
still see all emitted output. The original total deadline does not reset.
"""
import subprocess,sys,time,json
from pathlib import Path
value=sys.argv[1];seconds=float(value[:-1])*{'s':1,'m':60,'h':3600}[value[-1]] if value[-1].isalpha() else float(value)
deadline=time.monotonic()+seconds
events=Path(__file__).with_name('native_launcher_04_events.jsonl')
for attempt in [1,2]:
    started=time.monotonic();process=subprocess.Popen(sys.argv[2:])
    try:code=process.wait(timeout=max(.01,deadline-time.monotonic()))
    except subprocess.TimeoutExpired:
        subprocess.run(['taskkill.exe','/PID',str(process.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        process.wait(timeout=30);code=124
    row={'command':sys.argv[2:],'attempt':attempt,'pid':process.pid,'raw_returncode':code,'seconds':round(time.monotonic()-started,3),'remaining_deadline_seconds':round(max(0,deadline-time.monotonic()),3)}
    with events.open('a',encoding='utf-8') as f:f.write(json.dumps(row)+'\n')
    if code not in [3221225477,-1073741819] or attempt==2 or time.monotonic()>=deadline:break
    print('WINDOWS_NATIVE_RETRY|raw_returncode='+str(code)+'|attempt=1|same command/source; original deadline retained',flush=True)
raise SystemExit(code)

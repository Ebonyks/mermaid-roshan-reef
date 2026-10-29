"""Native Windows process deadline adapter; preserves ci.sh commands and timeout rules."""
import subprocess, sys
value=sys.argv[1]
seconds=float(value[:-1])*{'s':1,'m':60,'h':3600}[value[-1]] if value[-1].isalpha() else float(value)
process=subprocess.Popen(sys.argv[2:])
try:
    code=process.wait(timeout=seconds)
except subprocess.TimeoutExpired:
    subprocess.run(['taskkill.exe','/PID',str(process.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    process.wait(timeout=30)
    code=124
raise SystemExit(code)

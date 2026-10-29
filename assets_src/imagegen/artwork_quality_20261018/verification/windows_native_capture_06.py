"""Native process output/deadline adapter for unchanged CI commands.

Windows GUI-subsystem Godot needs explicit native output handles under MSYS.
Every byte is forwarded to ci.sh/tee; nonzero returns are never retried.
"""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile
import time

value = sys.argv[1]
seconds = float(value[:-1]) * {'s': 1, 'm': 60, 'h': 3600}[value[-1]] if value[-1].isalpha() else float(value)
started = time.monotonic()
with tempfile.TemporaryFile() as output:
    process = subprocess.Popen(sys.argv[2:], stdout=output, stderr=subprocess.STDOUT)
    try:
        code = process.wait(timeout=seconds)
    except subprocess.TimeoutExpired:
        subprocess.run(['taskkill.exe', '/PID', str(process.pid), '/T', '/F'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait(timeout=30)
        code = 124
    output.seek(0)
    shutil.copyfileobj(output, sys.stdout.buffer)
    sys.stdout.buffer.flush()
row = {'command': sys.argv[2:], 'pid': process.pid, 'raw_returncode': code,
       'seconds': round(time.monotonic() - started, 3), 'attempts': 1,
       'native_output_handle': 'explicit temporary file, complete bytes forwarded unchanged'}
with Path(__file__).with_name('native_capture_06_events.jsonl').open('a', encoding='utf-8') as file:
    file.write(json.dumps(row) + '\n')
raise SystemExit(code if 0 <= code <= 255 else 1)

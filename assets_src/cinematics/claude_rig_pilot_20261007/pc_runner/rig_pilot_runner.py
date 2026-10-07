"""Claude rig-pilot job runner for the local LTX-2.5 install (RTX 3060 Ti, ComfyUI on 127.0.0.1:8194).

The owner starts it once with start_rig_pilot_runner.bat. Claude (cloud session) cannot type into
terminals on the PC; it writes job files through the connected folder instead. The runner:
  * starts the isolated ComfyUI core with the usual Mermaid arguments plus the mermaid_rig_pilot
    loader, or reuses a server on 8194 that already has that loader;
  * takes job files from jobs/rig_pilot/queue/ in name order, checks every declared input file's
    SHA-256 in the ComfyUI input folder, accepts only allow-listed node classes and save prefixes
    under rig_pilot/<job_id>/, submits the graph, waits, and copies the saved frames and latents to
    results/rig_pilot/<job_id>/ with a receipt (timing, prompt id, workflow hash, GPU memory);
  * stops at the take cap (failures count), when jobs/rig_pilot/STOP exists, or when the window is closed;
  * unloads models after 30 idle minutes so the GPU is free for other use.
It runs ComfyUI graphs only: no shell commands, downloads or network access beyond 127.0.0.1.
"""
import hashlib
import json
import re
import shutil
import socket
import subprocess
import sys
import threading
import time
import traceback
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

RT = Path(__file__).resolve().parents[1]            # H:\MermaidReefTools\LocalVideo\ltx25
PORT = 8194
JOBS = RT / 'jobs' / 'rig_pilot'
RESULTS = RT / 'results' / 'rig_pilot'
TAKE_CAP = 8                                        # owner 2026-10-07 "trial methods until satisfied"; failures count
IDLE_UNLOAD_S = 30 * 60
MAX_JOB_S = 2400
ALLOWED = {
    'UNETLoader', 'CLIPLoader', 'VAELoader', 'LTXICLoRALoaderModelOnly', 'LoraLoaderModelOnly', 'UnionModelProof',
    'CLIPTextEncode', 'ConditioningZeroOut', 'LTXVConditioning', 'EmptyLTXVLatentVideo', 'LTXVEmptyLatentAudio',
    'KSamplerSelect', 'ManualSigmas', 'LoadImage', 'LoadLatent', 'LTXVAddGuide', 'RigPilotGuideBatch',
    'LTXAddVideoICLoRAGuide', 'LTXVConcatAVLatent', 'SamplerCustom', 'LTXVSeparateAVLatent', 'LTXVCropGuides',
    'SaveLatent', 'LatentUpscaleModelLoader', 'LTXVLatentUpsampler', 'VAEDecodeTiled', 'StudyFiniteImages',
    'SaveImage', 'UnionOutputProof', 'StudyRuntimeReceipt'}
SERVER_ARGS = ['--listen', '127.0.0.1', '--port', str(PORT), '--enable-dynamic-vram', '--bf16-vae', '--async-offload', '2',
               '--disable-all-custom-nodes', '--whitelist-custom-nodes', 'mermaid_study', 'mermaid_refine',
               'mermaid_union_trial', 'mermaid_rig_pilot', '--disable-api-nodes', '--preview-method', 'none',
               '--input-directory', str(RT / 'input'), '--output-directory', str(RT / 'output'),
               '--temp-directory', str(RT / 'temp'), '--user-directory', str(RT / 'user'),
               '--extra-model-paths-config', str(RT / 'models.yaml')]
STATE = {'state': 'starting', 'server_pid': None, 'server_started_by_runner': False, 'jobs_finished': [], 'message': ''}


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def log(*parts):
    print(datetime.now().strftime('%H:%M:%S'), *parts, flush=True)


def status(**kw):
    STATE.update(kw, at_utc=now(), takes_used=takes_used(), take_cap=TAKE_CAP)
    JOBS.mkdir(parents=True, exist_ok=True)
    tmp = JOBS / 'runner_status.json.tmp'
    tmp.write_text(json.dumps(STATE, indent=2) + '\n')
    tmp.replace(JOBS / 'runner_status.json')


def takes_used():
    return len(list(RESULTS.glob('*/receipt.json'))) if RESULTS.exists() else 0


def req(path, data=None, timeout=30):
    body = json.dumps(data).encode() if data is not None else None
    r = urllib.request.Request(f'http://127.0.0.1:{PORT}' + path, data=body, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(r, timeout=timeout) as f:
        raw = f.read()
    return json.loads(raw) if raw else {}


def port_open():
    with socket.socket() as s:
        s.settimeout(1)
        return s.connect_ex(('127.0.0.1', PORT)) == 0


def start_server():
    if port_open():
        info = req('/object_info/RigPilotGuideBatch')
        if 'RigPilotGuideBatch' not in info:
            raise SystemExit('A ComfyUI server is already running on port 8194 without the rig-pilot loader. '
                             'Close that ComfyUI window, then start this runner again.')
        log('Reusing the ComfyUI server already running on port', PORT)
        return None
    (RT / 'logs').mkdir(exist_ok=True)
    out = open(RT / 'logs' / 'rig_pilot_server.stdout.log', 'a', encoding='utf-8')
    err = open(RT / 'logs' / 'rig_pilot_server.stderr.log', 'a', encoding='utf-8')
    proc = subprocess.Popen([sys.executable, str(RT / 'scripts' / 'server_boot.py'), *SERVER_ARGS], stdout=out, stderr=err, cwd=str(RT))
    STATE.update(server_pid=proc.pid, server_started_by_runner=True)
    log('Starting ComfyUI (pid', proc.pid, '); first start can take a few minutes')
    t0 = time.monotonic()
    while time.monotonic() - t0 < 900:
        if proc.poll() is not None:
            raise SystemExit(f'ComfyUI exited with code {proc.returncode}; see logs\\rig_pilot_server.stderr.log')
        try:
            req('/system_stats', timeout=5)
            break
        except Exception:
            time.sleep(3)
    else:
        raise SystemExit('ComfyUI did not answer within 15 minutes')
    assert 'RigPilotGuideBatch' in req('/object_info/RigPilotGuideBatch'), 'mermaid_rig_pilot loader missing'
    log('ComfyUI ready')
    return proc


def gpu_sampler(samples, stop):
    while not stop.is_set():
        r = subprocess.run(['nvidia-smi', '--query-gpu=memory.used,utilization.gpu', '--format=csv,noheader,nounits'],
                           capture_output=True, text=True)
        if r.returncode == 0:
            try:
                m, u = r.stdout.strip().split(',')[:2]
                samples.append({'t': round(time.monotonic(), 1), 'card_used_mib': int(m), 'utilization_percent': int(u)})
            except ValueError:
                pass
        stop.wait(2)


def check_job(job, schema):
    jid = job['job_id']
    assert re.fullmatch(r'[A-Za-z0-9_-]{1,64}', jid), 'bad job_id'
    assert not (RESULTS / jid).exists(), f'results/rig_pilot/{jid} already exists (no silent repeat)'
    for f in job.get('inputs', []):
        p = (RT / 'input' / f['path']).resolve()
        assert str(p).startswith(str((RT / 'input').resolve())), f'input outside the ComfyUI input folder: {f["path"]}'
        assert p.is_file(), f'missing input {f["path"]}'
        assert sha(p) == f['sha256'], f'input hash mismatch {f["path"]}'
    for nid, node in job['graph'].items():
        kind = node['class_type']
        assert kind in ALLOWED, f'node class not allowed: {kind}'
        assert kind in schema, f'node class not installed: {kind}'
        missing = set(schema[kind]['input'].get('required', {})) - set(node['inputs'])
        assert not missing, f'node {nid} {kind} missing inputs {sorted(missing)}'
        if kind in ('SaveImage', 'SaveLatent'):
            assert node['inputs']['filename_prefix'].startswith(f'rig_pilot/{jid}/'), f'save prefix outside rig_pilot/{jid}/'


def run_job(path):
    job = json.loads(path.read_text(encoding='utf-8'))
    jid = job['job_id']
    out = RESULTS / jid
    receipt = {'job_id': jid, 'status': 'CHECKING', 'job_file_sha256': sha(path), 'started_at_utc': now(),
               'runner': 'scripts/rig_pilot_runner.py', 'runner_sha256': sha(__file__), 'take_number': takes_used() + 1,
               'take_cap': TAKE_CAP, 'note': job.get('note', '')}
    samples, stop = [], threading.Event()
    t0 = time.monotonic()
    pid = None
    try:
        q = req('/queue')
        assert not q['queue_running'] and not q['queue_pending'], 'other work is queued in ComfyUI'
        schema = req('/object_info', timeout=120)
        check_job(job, schema)
        out.mkdir(parents=True)
        (out / 'job.json').write_text(json.dumps(job, indent=2) + '\n', encoding='utf-8')
        (out / 'workflow.api.json').write_text(json.dumps(job['graph'], indent=2) + '\n', encoding='utf-8')
        receipt['workflow_sha256'] = sha(out / 'workflow.api.json')
        receipt['inputs_verified'] = len(job.get('inputs', []))
        threading.Thread(target=gpu_sampler, args=(samples, stop), daemon=True).start()
        sub = req('/prompt', {'prompt': job['graph'], 'client_id': str(uuid.uuid4())})
        assert 'prompt_id' in sub and not sub.get('node_errors'), sub
        pid = sub['prompt_id']
        receipt.update(status='RUNNING', prompt_id=pid)
        log('Job', jid, 'queued as', pid)
        limit = min(int(job.get('timeout_s', 1800)), MAX_JOB_S)
        last = 0
        while True:
            el = time.monotonic() - t0
            if el > limit:
                raise TimeoutError(f'job time cap {limit}s')
            if (JOBS / 'STOP').exists():
                raise RuntimeError('STOP file present')
            h = req('/history/' + pid)
            if pid in h:
                h = h[pid]
                (out / 'history.json').write_text(json.dumps(h, indent=2) + '\n', encoding='utf-8')
                assert h['status']['status_str'] == 'success', h['status'].get('messages', [])[-3:]
                break
            if el - last >= 30:
                log('  running', round(el), 's, card MiB', samples[-1]['card_used_mib'] if samples else '?')
                last = el
            time.sleep(3)
        files = {}
        labels = job.get('outputs', {})
        for nid, o in h['outputs'].items():
            for key in ('images', 'latents'):
                items = o.get(key, [])
                for i, x in enumerate(items):
                    src = RT / 'output' / x.get('subfolder', '') / x['filename']
                    label = labels.get(nid, f'node_{nid}')
                    dst = out / label / (f'{i:04d}' + src.suffix if key == 'images' else src.name)
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(src, dst)
                    files[str(dst.relative_to(out)).replace('\\', '/')] = sha(dst)
        for name in ('patch_install.json', 'patch_execution.json'):
            p = RT / 'results' / 'union_trial' / name
            if p.exists():
                shutil.copyfile(p, out / name)
        rc = RT / 'results' / 'runner_effective_configuration.json'
        if rc.exists():
            shutil.copyfile(rc, out / 'runner_effective_configuration.json')
        receipt.update(status='EXECUTION_PASS', output_files=files)
        log('Job', jid, 'finished:', len(files), 'files')
        return True
    except Exception as e:
        receipt.update(status='EXECUTION_FAIL', error=f'{type(e).__name__}: {e}', trace=traceback.format_exc()[-2000:])
        log('Job', jid, 'FAILED:', e)
        if pid:
            try:
                q = req('/queue')
                if any(x[1] == pid for x in q['queue_running']):
                    req('/interrupt', {})
                req('/queue', {'delete': [pid]})
            except Exception:
                pass
        return False
    finally:
        stop.set()
        receipt.update(finished_at_utc=now(), elapsed_seconds=round(time.monotonic() - t0, 1),
                       sampled_card_peak_mib=max((s['card_used_mib'] for s in samples), default=None))
        if pid is None:
            # Never submitted (failed a pre-check): not a generated take; the receipt goes beside the job.
            receipt['status'] = receipt['status'] if receipt['status'] == 'EXECUTION_FAIL' else 'NOT_SUBMITTED'
            (JOBS / 'failed').mkdir(parents=True, exist_ok=True)
            (JOBS / 'failed' / f'{path.stem}.receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
            if out.exists() and not (out / 'receipt.json').exists():
                shutil.rmtree(out)
        else:
            (out / 'memory_samples.json').write_text(json.dumps(samples) + '\n')
            (out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')


def main():
    for d in ('queue', 'done', 'failed'):
        (JOBS / d).mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    status(state='starting', message='starting ComfyUI')
    proc = None
    try:
        proc = start_server()
        status(state='idle', message='waiting for jobs in jobs\\rig_pilot\\queue')
        log('Waiting for jobs. Close this window (or create jobs\\rig_pilot\\STOP) to stop.')
        idle_since, unloaded = time.monotonic(), False
        while not (JOBS / 'STOP').exists():
            if proc is not None and proc.poll() is not None:
                raise SystemExit(f'ComfyUI exited with code {proc.returncode}')
            queue = sorted(p for p in (JOBS / 'queue').glob('*.json'))
            if queue:
                if takes_used() >= TAKE_CAP:
                    status(state='capped', message=f'take cap {TAKE_CAP} reached; jobs left in queue')
                    time.sleep(10)
                    continue
                job = queue[0]
                status(state='running', message=f'running {job.name}')
                ok = run_job(job)
                dest = JOBS / ('done' if ok else 'failed') / job.name
                job.replace(dest)
                STATE['jobs_finished'].append({'job': job.name, 'ok': ok, 'at_utc': now()})
                status(state='idle', message='waiting for jobs')
                idle_since, unloaded = time.monotonic(), False
                continue
            if not unloaded and time.monotonic() - idle_since > IDLE_UNLOAD_S:
                try:
                    req('/free', {'unload_models': True, 'free_memory': True})
                    log('Idle 30 min: models unloaded from the GPU')
                except Exception:
                    pass
                unloaded = True
            status(state='idle', message='waiting for jobs')
            time.sleep(5)
        status(state='stopped', message='STOP file found')
    except SystemExit as e:
        status(state='error', message=str(e))
        log('ERROR:', e)
    except KeyboardInterrupt:
        status(state='stopped', message='closed by owner')
    finally:
        if proc is not None and proc.poll() is None:
            proc.terminate()
            log('ComfyUI stopped')


if __name__ == '__main__':
    main()

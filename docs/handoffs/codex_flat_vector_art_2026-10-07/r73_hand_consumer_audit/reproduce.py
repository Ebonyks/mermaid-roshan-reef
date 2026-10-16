from pathlib import Path
import argparse,subprocess,os,json,hashlib,datetime
P=Path(__file__).resolve().parent;R=P.parents[3]
a=argparse.ArgumentParser();a.add_argument('--output-dir',required=True);a.add_argument('--report',required=True);args=a.parse_args();out=Path(args.output_dir).resolve();report=Path(args.report).resolve()
assert not out.exists(), 'Use a new scratch output directory'
assert not report.exists(), 'Preserve earlier reproduction reports'
out.mkdir(parents=True);env=dict(os.environ,FVHC_OUTPUT=str(out));command=['python','-B',str(P/'scan_consumers.py')]
q=subprocess.run(command,cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(out/'scan.log').write_bytes(q.stdout);assert q.returncode==0,q.stdout.decode(errors='replace')[-2000:]
rows=[]
for name in ['SOURCE_CENSUS.json','SOURCE_BODIES.json','CONSUMER_MAP.json','INTAKE_CORRECTION.json']:
 expected=(P/name).read_bytes();actual=(out/name).read_bytes();assert actual==expected,name;rows.append({'path':name,'bytes':len(actual),'sha256':hashlib.sha256(actual).hexdigest(),'exact_bytes':True})
d={'status':'PASS_EXACT_FOUR_ANALYSIS_OUTPUTS','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_revision':'5120b6d59885dd057937aaf284e73681d8eac9f5','command':command,'scanner_sha256':hashlib.sha256((P/'scan_consumers.py').read_bytes()).hexdigest(),'outputs':rows,'scope':'Fresh source-only scanner run into new scratch directory reproduces the exact four authoritative JSON outputs, including stable source IDs. No engine/runtime/source-art/save write or new acceptance.'};report.parent.mkdir(parents=True,exist_ok=True);report.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n');print('R73_REPRODUCTION_PASS',len(rows),flush=True)

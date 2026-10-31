"""Recheck unchanged native logs with the repository CI's exact classifiers."""
from pathlib import Path
import hashlib,json,re
root=Path(__file__).resolve().parents[3]
out=Path(__file__).resolve().parent/'verification'
original=out/'focused_01.json'
data=json.loads(original.read_text())
ci=(root/'scripts/ci.sh').read_text()
failure=re.search(r"FAILURE_RE='([^']+)'",ci).group(1)
runtime=re.search(r"RUNTIME_ERROR_RE='([^']+)'",ci).group(1)
for row in data['records']:
    p=out/(row['probe']+'_focused_01.log')
    assert hashlib.sha256(p.read_bytes()).hexdigest()==row['log_sha256']
    text=p.read_text('utf-8',errors='replace')
    row['original_overstrict_classifier_status']=row['status']
    row['status']='PASS' if row['exit']==0 and text.strip() and not re.search(failure+'|'+runtime,text) else 'FAIL'
    row['verdict_lines']=[line for line in text.splitlines() if 'ALL OK' in line or 'RESULT:' in line][-3:]
data['classifier_correction']='Original helper required ALL OK, but Chapter Two probes use RESULT: PASS. Native exits/logs/source hashes unchanged. This receipt applies exact scripts/ci.sh FAILURE_RE/RUNTIME_ERROR_RE and nonempty-output floor; original receipt is preserved.'
data['status']='PASS' if all(x['status']=='PASS' for x in data['records']) and not data['source_drift'] else 'FAIL'
(out/'focused_01_ci_classification.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'status':data['status'],'probes':[(x['probe'],x['status']) for x in data['records']],'source_drift':data['source_drift']}))

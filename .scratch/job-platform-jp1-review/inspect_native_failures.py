from pathlib import Path
import hashlib, json, re, subprocess

CLONE=Path('C:/Users/Peter/Documents/mermaid-roshan-reef')
JP0=Path('H:/CodexWorktrees/mermaid-roshan-reef-job-platform-jp0-20260930')
EVIDENCE=Path('H:/CodexWorktrees/job-platform-jp0-evidence-20260930')
REV='549ea956b63ce438d007b26537ec917508eae3cb'
PREFIX='assets_src/prototypes/fairy_restoration_2026-09-30/review/'
PROBES=['probe_audit','probe_audio','probe_dust_boss_balance']
def git_bytes(relative, revision=REV):
    return subprocess.check_output(['git','show',revision+':'+relative],cwd=CLONE)
def digest(raw): return hashlib.sha256(raw).hexdigest()
def canonical(raw): return raw.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
text=(EVIDENCE/'full-ci3.log').read_text(encoding='utf-8-sig')
result={'full_ci':json.loads((EVIDENCE/'full-ci3-result.json').read_text()),'full_ci_log_sha256':digest((EVIDENCE/'full-ci3.log').read_bytes()),'three_probes':{},'faerie_receipt_sections':{},'prior_log_matches':{}}
for probe in PROBES:
    start=text.index('=== '+probe+' ===')
    end=text.find('\n=== ',start+1)
    section=text[start:end if end>=0 else len(text)]
    relative='scripts/'+probe+'.gd'
    local=(JP0/relative).read_bytes()
    result['three_probes'][probe]={'section':section,'source_sha256':digest(local),'canonical_source_sha256':digest(canonical(local)),'same_as_faerie_commit_canonical':canonical(local)==canonical(git_bytes(relative)),'same_as_immutable_green7f_canonical':canonical(local)==canonical(git_bytes(relative,'7f068cb80766edd52a110cc1cb3958158f829822')),'explicit_quit_sites':re.findall(r'(?m)^.*\bquit\(.*$',local.decode('utf-8'))}
receipt=json.loads(git_bytes(PREFIX+'LOCAL_GATE_RECEIPT.json'))
for key,value in receipt.items():
    if any(word in key.lower() for word in ['native','windows','clock','limitation','complete']):
        result['faerie_receipt_sections'][key]=value
for name in ['WINDOWS_NATIVE_INITIAL_ATTEMPT_LOG.txt','WINDOWS_NATIVE_ISOLATED_ENGINE_CONTINUATION_LOG.txt','WINDOWS_NATIVE_FIXED_CLOCK_CONTINUATION_LOG.txt','WINDOWS_NATIVE_FULL_TRUSTED_LOG.txt','DIRECT_NATIVE_RECHECK_LOG.txt','FULL_CI_FINAL_WRAPPER_LOG.txt','FULL_CI_FINAL_DIRECT_LOG.txt','FULL_CI_REMAINING_LOG.txt']:
    raw=git_bytes(PREFIX+name)
    lines=raw.decode('utf-8-sig').splitlines()
    indices=[i for i,line in enumerate(lines) if re.search(r'(127|3221225477|3221226505|access.violation|aborted|exit code)',line,re.I) or re.search(r'^(WINDOWS_NATIVE|PROBE|===|DIRECT_NATIVE).*probe_(audit|audio|dust_boss_balance)',line) or re.search(r'^(WINDOWS_NATIVE|PROBE|DIRECT_NATIVE).*exit[=:]\s*-?[1-9]\d*',line)]
    windows=[]
    for index in indices:
        windows.append({'line':index+1,'text':'\n'.join(lines[max(0,index-1):min(len(lines),index+3)])})
    result['prior_log_matches'][name]={'sha256':digest(raw),'matches':windows,'first_lines':lines[:12]}
out=CLONE/'.scratch/job-platform-jp1-review/native-failure-inspection.json'
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'output':str(out),'full_ci':result['full_ci'],'three_probe_source_equality':{name:{key:value for key,value in entry.items() if key.startswith('same_as_')} for name,entry in result['three_probes'].items()},'prior_log_matches':{name:entry for name,entry in result['prior_log_matches'].items()}},indent=2))

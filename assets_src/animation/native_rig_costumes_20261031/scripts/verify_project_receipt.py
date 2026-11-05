"""Bind the retained red baseline, diagnostic, repaired probe and full rerun."""
from pathlib import Path
import hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT.parents[2];E=ROOT/'evidence'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def text(p):return p.read_text(encoding='utf-8-sig')
def main():
 ci=text(REPO/'scripts/ci.sh');rerun=text(ROOT/'scripts/project_probe_rerun.sh')
 suffix=ci[ci.index('rc=0\nfor p in probe_reef_districts'):]
 actual=rerun[rerun.index('rc=0\nfor p in probe_reef_districts'):]
 expected=re.search(r'for p in (.*?); do',suffix).group(1).split()
 log=text(E/'project_probes_rerun.log');runs=re.findall(r'^PROBE (\w+) process exit: (\d+)',log,re.M)
 original=text(E/'project_gates.log');focused=text(E/'opera_2d_focused.log');repaired=text(E/'opera_2d_repaired.log')
 old=text(E/'probe_opera_2d_before.gd.txt');new=text(REPO/'scripts/probe_opera_2d.gd')
 # The geometry expression itself must remain byte-identical.
 def geometry(s):
  start=s.index('\n\t\t\t\tfinale_cast_separated = _rect_inside')
  return s[start:s.index('\n\t\t_check(',start)]
 unchanged=geometry(old)==geometry(new)
 melody=text(E/'melody_focused.log');melody_source=REPO/'scripts/probe_melody.gd'
 git_melody=subprocess.check_output(['git','show','HEAD:scripts/probe_melody.gd'],cwd=REPO)
 melody_unchanged=sha(melody_source)==json.loads(text(E/'melody_baseline.json'))['probe_sha256']
 melody_unchanged=melody_unchanged and git_melody.replace(b'\r\n',b'\n')==melody_source.read_bytes().replace(b'\r\n',b'\n')
 nonzero=[(n,c) for n,c in runs if c!='0'];single_run_pass=not nonzero and text(E/'project_probes_rerun.exit').strip()=='0'
 # The contract permits probe-by-probe validation. Report the non-green whole
 # run explicitly; retain its red Melody result and a separate unchanged retest.
 latest=dict(runs);latest['probe_melody']=text(E/'melody_focused.exit').strip()
 classifier=re.search(r"^FAILURE_RE='([^']+)'",ci,re.M).group(1)
 runtime=re.search(r"^RUNTIME_ERROR_RE='([^']+)'",ci,re.M).group(1)
 outside_melody=log.split('=== probe_melody ===',1)[0]+log.split('=== probe_dolls ===',1)[1]
 checks={'exact_ci_probe_loop':suffix==actual,'exact_roster_82':len(expected)==82 and [n for n,c in runs]==expected,'latest_individual_probes_all_zero':all(latest.get(n)=='0' for n in expected),'whole_run_nonzero_only_melody':not nonzero or nonzero==[('probe_melody','1')],'non_melody_failure_classifier_clear':not re.search(classifier,outside_melody) and not re.search(runtime,outside_melody),'melody_source_unchanged':melody_unchanged,'melody_focused_all_ok':'MELODY|result: ALL OK' in melody and not re.search(classifier,melody) and not re.search(runtime,melody),'repaired_focus_exit_zero':text(E/'opera_2d_repaired.exit').strip()=='0','positive_geologist_sample':'OPERA2D|OK|geologist visible finale geometry is actually sampled' in repaired,'same_geometry_predicate':unchanged,'original_failure_retained':'OPERA2D|FAIL|geologist stages the room-finale partner clear of Roshan and the activity' in original and 'OPERA2D|FAIL|geologist stages the room-finale partner clear of Roshan and the activity' in focused}
 sources=['project_gates.log','project_gates.exit','opera_2d_focused.log','opera_2d_diagnostic.log','geologist_sampling_diagnosis.json','opera_2d_repaired.log','opera_2d_repaired.exit','project_probes_rerun.log','project_probes_rerun.exit','melody_rerun_initial.log','melody_baseline.json','melody_diagnostic.log','melody_diagnostic.exit','melody_focused.log','melody_focused.exit']
 receipt={'pass':all(checks.values()),'scope':'Latest individual probe verdicts, including a separately recorded unchanged Melody retest; not an uninterrupted green full-suite claim.','single_full_rerun_pass':single_run_pass,'whole_run_nonzero':nonzero,'checks':checks,'initial_full_lane':'81 of 82 processes zero; Geologist zero-sample probe false-negative, independently reproduced. Import and 2D scan retained in original log.','final_lane':'All 82 trusted probes rerun after the probe-only repair, same flags, isolated saves, timeouts and classifiers. Melody has an intermittent post-pause miss with a downstream count failure; read-only trace and uninstrumented focused retest pass. Cause remains unproven. No Melody assertion or gameplay source change.','root_probe_sha256':sha(REPO/'scripts/probe_opera_2d.gd'),'melody_probe_sha256':sha(melody_source),'evidence':{n:sha(E/n) for n in sources},'limits':'Local per-probe lane, not a newly run entire static/audio CI prefix. The retained non-green whole run remains non-green. Exact published-head full CI is separate. This does not close MA-CI-007 or establish owner/device/child acceptance.'}
 (E/'project_gate_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(receipt,indent=2));return 0 if receipt['pass'] else 1
if __name__=='__main__':raise SystemExit(main())

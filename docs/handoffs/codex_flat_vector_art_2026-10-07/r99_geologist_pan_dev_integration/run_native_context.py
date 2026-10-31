from pathlib import Path
import json,subprocess,hashlib,os,datetime
S=Path(__file__).parent;R=Path.cwd();W=S/'native_context';W.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
result=rd(S/'native_resume/FINAL_RESULT.json');assert result['status']=='PASS_ALL_82_PROBE_BY_PROBE'and result['normal_unchanged']
pin=rd(S/'merged_validation/SOURCE_PIN.json')
for k in ['runtime_hashes','sidecars']:assert all((R/p).is_file()and sha(R/p)==h for p,h in pin[k].items()),k
fixture=R/'export/flat_vector_r95/capture_pan.gd';canonical=R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r95_geologist_pan_runtime/capture_pan.gd';assert fixture.read_bytes().replace(b'\r\n',b'\n')==canonical.read_bytes().replace(b'\r\n',b'\n')
engine=Path(pin['engine']).with_name('godot.exe');assert sha(engine)=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
normal=rd(R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r95_geologist_pan_runtime/CANDIDATE_SOURCE_PIN.json')['normal_base'];cases=[]
for width in [1280,1600]:
 d=W/str(width);d.mkdir();e=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',R95_OUT=str(d/'output'),R95_WIDTH=str(width),R95_VARIANT='candidate',R95_REV=result['baseline']+' + '+result['incoming_dev']+' @ index '+result['index_tree'],R95_NORMAL_BASE=normal)
 for key,name in [('APPDATA','appdata'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:p=d/name;p.mkdir();e[key]=str(p)
 cmd=[str(engine),'--path',str(R),'--rendering-method','mobile','--audio-driver','Dummy','--resolution',str(width)+'x720','--max-fps','30','--script','res://export/flat_vector_r95/capture_pan.gd']
 wr(d/'LAUNCH.json',{'command':cmd,'source_revision':result['baseline'],'incoming_dev':result['incoming_dev'],'index_tree':result['index_tree'],'fixture_raw_sha256':sha(fixture),'fixture_LF_sha256':hashlib.sha256(fixture.read_bytes().replace(b'\r\n',b'\n')).hexdigest(),'normal_data':'Hash guards only; synthetic owned PAN checkpoint used.','started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline_control':'Immutable original R95 source captures; this check only refreshes current merged candidate/caller context, not new failing-baseline or formalQA11 proof.'})
 with(d/'engine.log').open('wb')as log:q=subprocess.run(cmd,cwd=R,env=e,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,timeout=180,creationflags=0x08000000)
 assert q.returncode==0,(d/'engine.log').read_text(errors='replace')[-2000:]
 j=rd(d/'output/RESULT.json');assert j['status']=='PASS'and all(x['pass']for x in j['checks'])and j['normal_before']==j['normal_after'];cases.append({'width':width,'checks':len(j['checks']),'captures':j['captures'],'result':str(d/'output/RESULT.json'),'result_sha256':sha(d/'output/RESULT.json')});print('R99_NATIVE_CONTEXT_PASS',width,len(j['checks']),len(j['captures']),flush=True)
wr(W/'FINAL_RESULT.json',{'status':'PASS','source_revision':result['baseline'],'incoming_dev':result['incoming_dev'],'index_tree':result['index_tree'],'cases':cases,'checks':sum(x['checks']for x in cases),'native_frame_events':sum(len(x['captures'])for x in cases),'new_generation_calls':0,'normal_save_unchanged':True,'runtime_or_probe_edits':False,'formal_QA11':None,'device':None,'child':None,'owner':None,'accepted_removed':0,'limits':'Owned synthetic checkpoint/current Main library-room launcher; GUI input targets surface directly. Not natural end-to-end route or formalQA11/device/human acceptance.','completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});print('R99_NATIVE_CONTEXT_ALL_OK',flush=True)

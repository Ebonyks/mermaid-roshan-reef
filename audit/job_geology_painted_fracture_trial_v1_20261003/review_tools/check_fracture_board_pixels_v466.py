from pathlib import Path
import subprocess,hashlib,json,sys
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');J=R/'audit/job_geology_painted_fracture_trial_v1_20261003'
ff='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe'
manifest=json.loads((J/'QA_BOARD_MANIFEST_A2.json').read_text(encoding='utf-8-sig'))
b=next(x for x in manifest['boards'] if x['width']==1600 and x['kind']=='motion_frames' and x['first']==96)
def raw(path,filter):return subprocess.check_output([ff,'-hide_banner','-loglevel','error','-i',str(R/path),'-frames:v','1','-vf',filter,'-pix_fmt','rgba','-f','rawvideo','-'],creationflags=subprocess.CREATE_NO_WINDOW)
sources=[raw(m['path'],'scale=480:-1') for m in b['members']]
for local in [0,3,4,7,10]:
 x=2+(local%3)*482;y=2+(local//3)*218
 a=sources[local];c=raw(b['path'],f'crop=480:216:{x}:{y}')
 distances=[sum(abs(s[i]-c[i]) for i in range(0,len(c),16))/len(range(0,len(c),16)) for s in sources]
 print(json.dumps({'index':b['first']+local,'literal_scaled_source_matches_board_cell':a==c,'sampled_red_mae':distances,'closest_source_index':b['first']+min(range(len(distances)),key=lambda i:distances[i]),'source_sha256':hashlib.sha256(a).hexdigest(),'cell_sha256':hashlib.sha256(c).hexdigest(),'lengths':[len(a),len(c)]}),flush=True)

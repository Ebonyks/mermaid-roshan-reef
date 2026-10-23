#!/usr/bin/env python3
"""Score-derived Pop Star section audio/chart. Never reads the Iko recording.
Reuse the original renderer without changing its 44-track baseline manifest.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, subprocess, tempfile
from pathlib import Path
import numpy as np
import build_area_music as music
ROOT = Path(__file__).resolve().parents[1]
SCORE = Path('assets_src/audio/music/popstar_concert_score.json')
OUT = Path('assets/audio/music/popstar_concert')
CHILD = {'answer','play','lead','finish'}
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def source_sha(path):
    return music._text_sha256(path)
def emit(section):
    cues=[]
    def cue(beat,target,role,phrase=''):
        cues.append(dict(id=f"{section['id']}_{len(cues):02}",section=section['id'],beat=beat,target=target,role=role,phrase=phrase))
    if section['kind'] in {'echo','contest'}:
        for i,pattern in enumerate(section['patterns']):
            positions=[0,2] if len(pattern)==2 else [0,1.5,3]
            for j,target in enumerate(pattern): cue(8+i*8+positions[j],target,'call',str(i))
            for j,target in enumerate(pattern): cue(12+i*8+positions[j],target,'answer',str(i))
    elif section['kind']=='rehearsal':
        for beat,target in zip(section['child_beats'],section['patterns'][0]): cue(beat,target,'play')
        for j,target in enumerate(section['echo']): cue(24+j*2,target,'call','rehearsal')
        for j,target in enumerate(section['echo']): cue(28+j*2,target,'answer','rehearsal')
    else:
        for beat,target in zip(section['child_beats'],section['targets']): cue(beat,target,section['kind'])
    return sorted(cues,key=lambda c:(c['beat'],c['id']))
def validate(score,sections):
    assert score['bpm']==118 and score['meter']==[4,4]
    for section in sections:
        previous=-1e9
        child=[c for c in section['cues'] if c['role'] in CHILD]
        assert child, section['id']
        for c in section['cues']:
            assert 0<=c['beat']<section['bars']*4 and c['beat']*2==round(c['beat']*2), c
            assert c['target'] in range(4), c
            assert c['role'] in CHILD|{'call'}, c
            assert c['target']!=3 or c['role']=='lead', c
            if c['role'] in CHILD:
                assert c['beat']>=6, c
                assert (c['beat']-previous)*60/score['bpm']>=0.52-1e-8, c
                previous=c['beat']
        if section.get('required_final'): assert child[-1]['target']==2 and child[-1]['role']=='finish'
        for c in [c for c in section['cues'] if c['role']=='answer']:
            assert any(a['role']=='call' and a['phrase']==c['phrase'] and a['target']==c['target'] and abs(c['beat']-a['beat']-4)<1e-8 for a in section['cues']), c
        for c in [c for c in section['cues'] if c['role']=='call']:
            assert any(a['role']=='answer' and a['phrase']==c['phrase'] and a['target']==c['target'] and abs(a['beat']-c['beat']-4)<1e-8 for a in section['cues']), c

def instrument_hit(name, seed):
    """Soft original tom/bass/crash timbres, not borrowed samples."""
    if name=='stick': return music._synth_drum('wood',0.75,seed)
    rng=np.random.default_rng(seed)
    seconds={'tom':0.38,'bass':0.32,'cymbal':0.85}[name]
    t=np.arange(round(seconds*music.SAMPLE_RATE))/music.SAMPLE_RATE
    if name=='cymbal':
        # Inharmonic ringing partials plus softened bright noise give a short
        # crash instead of a jingle-bell rhythm. Fundamental E stays in key.
        ring=sum(np.sin(2*np.pi*659.255*r*t)/(i+2) for i,r in enumerate([1,1.342,1.732,2.432,3.141,4.06]))
        noise=rng.standard_normal(len(t));noise=noise-np.convolve(noise,np.ones(7)/7,mode='same')
        sound=(ring*0.18+noise*0.16)*np.exp(-t*7.0)
    else:
        base=164.814 if name=='tom' else 55.0
        frequency=base*(1.0+0.65*np.exp(-t*35.0))
        phase=2*np.pi*np.cumsum(frequency)/music.SAMPLE_RATE
        sound=(np.sin(phase)+0.12*np.sin(phase*2.0))*np.exp(-t*(12 if name=='tom' else 16))
        sound+=rng.standard_normal(len(t))*0.055*np.exp(-t*110)
    sound*=np.minimum(1,t/0.002)*np.minimum(1,(seconds-t)/0.025)
    sound*=0.68/max(1e-8,float(np.max(np.abs(sound))))
    return sound

def build(check=False):
    root=ROOT; score=json.loads((root/SCORE).read_text(encoding='utf-8-sig'))
    sections=[dict(s,cues=emit(s)) for s in score['sections']]
    validate(score,sections)
    if check:
        chart=json.loads((root/OUT/'chart.json').read_text())
        assert chart['score_sha256']==source_sha(root/SCORE)
        assert chart['builder_sha256']==source_sha(Path(__file__))
        assert chart['original_score_sha256']==source_sha(root/music.SCORES_PATH)
        for s in sections:
            assert chart['sections'][sections.index(s)]['cues']==s['cues']
        for rel,digest in chart['audio_sha256'].items(): assert sha(root/rel)==digest,rel
        ffmpeg=music._find_ffmpeg(None,root);ffprobe=music._find_ffprobe(ffmpeg)
        for section in chart['sections']:
            info=music._probe_ogg(ffprobe,root/section['audio'].removeprefix('res://'))
            assert info['codec']=='vorbis' and info['sample_rate_hz']==48000 and info['channels']==2
            assert info['average_bitrate_bps']>=64000
            assert abs(info['duration_seconds']-section['bars']*4*60/score['bpm'])<1/48000+0.001
            assert int(info['tags']['LOOPEND'])==section['sample_count']
        print('POPSTAR_SCORE|source, chart, audio hashes and spacing: ALL OK');return
    catalog,cues=music._load_catalog(root)
    original=next(c for c in cues if c['id']=='opera_popstar')
    ffmpeg=music._find_ffmpeg(None,root);ffprobe=music._find_ffprobe(ffmpeg)
    (root/OUT).mkdir(parents=True,exist_ok=True)
    audio_hashes={};metrics={}
    with tempfile.TemporaryDirectory(prefix='popstar-concert-') as temp:
        tmp=Path(temp)
        for index,s in enumerate(sections):
            cue=copy.deepcopy(original)
            cue.update(id='popstar_'+s['id'],title=score['title']+' / '+s['id'],bars=s['bars'],percussion='none')
            cue['instruments']['harmony']='ukulele'
            samples,metric=music._render_float(cue,catalog)
            # Count-in clicks are a declared score part, separate from the child's drums.
            for click in s['count_in_beats']:
                sound=music._synth_drum('wood',0.65,580+int(click))
                music._add_circular(samples,round(click*60/score['bpm']*music.SAMPLE_RATE),sound,0.25,0.0)
            # Ghost call notes are rendered from the exact same score rows.
            for c in s['cues']:
                if c['role']=='call':
                    note=music._synth_note('ukulele',69+[0,4,7][c['target']],0.22,600+index*100+int(c['beat']*2))
                    music._add_circular(samples,round(c['beat']*60/score['bpm']*music.SAMPLE_RATE),note,0.24,-0.3)
            samples=np.clip(samples,-0.75,0.75)
            metric['final_score_seam']=music._seam_metrics(samples)
            assert metric['final_score_seam']['jump_ratio']<=4.0
            pcm,mastering=music._normalise_pcm(ffmpeg,samples,tmp)
            metric['mastering']=mastering
            wav=tmp/'normalised.wav'
            dest=root/OUT/(s['id']+'.ogg')
            music._encode_ogg(ffmpeg,wav,dest,cue,len(samples),91000+index)
            info=music._probe_ogg(ffprobe,dest)
            # Import settings own looping; explicit whole-bar switching owns epochs.
            source='res://'+dest.relative_to(root).as_posix()
            digest=hashlib.md5(source.encode()).hexdigest()
            text=music._import_text(cue).replace('res://assets/audio/music/'+cue['id']+'.ogg',source).replace(cue['id']+'.ogg-',s['id']+'.ogg-')
            text=text.replace(hashlib.md5(('res://assets/audio/music/'+cue['id']+'.ogg').encode()).hexdigest(),digest).replace('loop=true','loop=false')
            dest.with_suffix('.ogg.import').write_text(text,encoding='utf-8',newline='\n')
            s['audio']=source;s['sample_count']=len(samples);s['loopable']=True
            audio_hashes[dest.relative_to(root).as_posix()]=sha(dest);metrics[s['id']]={'source':metric,'encoded':info}
            print('POPSTAR_SCORE|rendered '+s['id'],flush=True)
        # Instant instrument feedback is separate from backing, never quantized.
        for index,(name,kind) in enumerate([('tom','wood'),('bass','kick'),('cymbal','sleigh'),('stick','wood')]):
            mono=instrument_hit(name,92000+index)
            stereo=np.column_stack([mono,mono])*0.55
            wav=tmp/(name+'.wav');music._write_pcm(wav,stereo)
            dest=root/OUT/(name+'.ogg')
            subprocess.run([str(ffmpeg),'-v','error','-y','-i',str(wav),'-c:a','libvorbis','-b:a','96k',str(dest)],check=True)
            music._canonicalize_ogg(dest,92000+index)
            audio_hashes[dest.relative_to(root).as_posix()]=sha(dest)
    chart={'source_hash_normalization':'UTF-8 LF bytes; CRLF normalized; BOM preserved','schema':'reef.popstar-chart.v1','song_id':score['id'],'bpm':score['bpm'],'meter':score['meter'],'score_path':SCORE.as_posix(),'score_sha256':source_sha(root/SCORE),'builder_sha256':source_sha(Path(__file__)),'original_score_sha256':source_sha(root/music.SCORES_PATH),'audio_sha256':audio_hashes,'sections':sections,'metrics':metrics,'clock_choice':'one Ogg per section; exact4.7.2 Mobile spike proves Interactive position stays zero while Ogg advances. See assets_src/prototypes/popstar_concert_20261022/audio_clock.json. Target-device proof pending','acceptance':'CANDIDATE; synthesized arrangement needs listening, gameplay/device/child/owner acceptance separately'}
    (root/OUT/'chart.json').write_text(json.dumps(chart,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args();build(args.check)

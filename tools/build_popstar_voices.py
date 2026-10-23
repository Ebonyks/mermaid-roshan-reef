#!/usr/bin/env python3
"""Exact isolated Pop Star cues using the existing synthetic Roshan preset.
No protected family recording is opened or overwritten.
"""
import argparse,hashlib,json,os,sys
from pathlib import Path
import make_voices
CUES={
 'rehearsal':'Tap each drum when it glows!',
 'echo':'Listen to the band, then play it back!',
 'play':'Play along with the ribbons!',
 'lead':'Now you lead! Tap the microphone!',
 'finish':'Big finish! Crash the star cymbal!',
 'hey':'Hey!',
}
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--kokoro',required=True);args=parser.parse_args()
 root=Path(__file__).resolve().parents[1];out=root/'assets/prototypes/popstar_concert/voices'
 argv=[sys.argv[0],'--kokoro',args.kokoro,'--out',str(out)]
 for key,text in CUES.items():
  make_voices.LINES[key]=('roshan',text);argv.extend(['--line',key])
 sys.argv=argv;make_voices.main()
 manifest={'workflow':'existing make_voices Roshan synthetic preset, not family imitation','model_sha256':hashlib.sha256((Path(args.kokoro)/'model.onnx').read_bytes()).hexdigest(),'voice_preset':list(make_voices.CHARS['roshan']),'cues':{key:{'text':text,'sha256':hashlib.sha256((out/(key+'.ogg')).read_bytes()).hexdigest()} for key,text in CUES.items()},'listening_acceptance':'PENDING'}
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':main()

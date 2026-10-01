"""Rebuild a separate reference derivative without overwriting archive originals."""
import argparse,json,shutil,subprocess
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument('object_id');p.add_argument('--packet',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--output-directory',type=Path,required=True);p.add_argument('--aseprite',default='C:/Program Files/Aseprite/Aseprite.exe');args=p.parse_args()
 packet=args.packet.resolve();manifest=json.loads((packet/'manifest.json').read_text());item=next(x for x in manifest['objects'] if x['id']==args.object_id)
 output=args.output_directory.resolve();assert not output.is_relative_to(packet),'Use a separate derivative output directory, outside the immutable archive'
 output.mkdir(parents=True,exist_ok=False);(output/'frames').mkdir()
 source=packet/'objects'/args.object_id
 for name in ['source.png','bounds.lua']:shutil.copyfile(source/name,output/name)
 ase=args.aseprite if Path(args.aseprite).exists() else shutil.which('aseprite');assert ase,'Aseprite executable is required'
 subprocess.run([ase,'--batch','--script-param','root='+output.as_posix(),'--script-param','id='+args.object_id,'--script',str(packet/'production/author_motion.lua')],check=True)
 subprocess.run([ase,'--batch',str(output/(args.object_id+'.aseprite')),'--sheet',str(output/'spritesheet.png'),'--sheet-type','rows','--sheet-columns','8','--sheet-width','2048','--sheet-height','1024','--data',str(output/'spritesheet.json'),'--format','json-array'],check=True)
 print('New scripted reference derivative saved: '+str(output))
if __name__=='__main__':main()

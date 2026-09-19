"""Seal byte-level B-roll archive manifests. Publication verification is separate."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path
from tools.build_grok_broll import PACKET, PARENT, SOURCE_MEDIA, dimensions, dump

def sha(data):return hashlib.sha256(data).hexdigest()

def seal(packet, private):
    registry=json.loads((packet/'REFERENCES.json').read_bytes())['references']
    refs={'references/'+r['path']:r for r in registry.values()}
    generated={r['path']:r for r in json.loads((packet/'GENERATION_PROVENANCE.json').read_bytes())}
    files=[]
    for file in sorted(packet.rglob('*')):
        if not file.is_file():continue
        rel=file.relative_to(packet).as_posix()
        if rel in ('HANDOFF_PACKET.json','PACKAGE_MANIFEST.json') or rel.startswith('receipts/'):continue
        data=file.read_bytes();entry={'path':rel,'sha256':sha(data),'bytes':len(data),'dimensions':None,'role':'planning_or_review_metadata','source_path':PACKET+'/'+rel,'source_commit':None,'license_provenance':'Project-authored handoff metadata; no new media rights or acceptance granted','modifications':'authored planning/review metadata','used_as_delivery_pixels':False}
        if file.suffix.lower() in ('.png','.jpg','.jpeg'):entry['dimensions']=dimensions(file)
        if rel in refs:
            r=refs[rel]
            if sha(data)!=r['sha256']:raise ValueError('Reference changed '+rel)
            entry.update(role='existing_visual_reference',source_path=r['source_path'],source_commit=r['commit'],license_provenance=r['license_provenance'],modifications='byte-identical source copy')
        elif rel in generated:
            r=generated[rel]
            if sha(data)!=r['sha256']:raise ValueError('Generated native changed '+rel)
            entry.update(role='selected_candidate_board' if r['selected_concept'] else 'rejected_or_superseded_board',source_path=r['path'],license_provenance='Owner-commissioned OpenAI built-in image generation, 2026-09-19; input attribution and exact prompt in GENERATION_PROVENANCE.json',modifications='native tool output, not recompressed',prompt_sha256=r['prompt_sha256'])
        elif rel.startswith('historical_boards/'):
            entry.update(role='historical_board_not_current_geometry',source_path='grok_builder_2026-09-14/boards_v4/'+file.name,source_commit=SOURCE_MEDIA,license_provenance='Inherited project-authored storyboard; continuity discussion only',modifications='byte-identical source copy')
        elif rel.startswith('source_plans/'):
            entry.update(role='frozen_parent_plan',source_path='design/cinematics/v2/shots/'+rel[len('source_plans/'):],source_commit=PARENT,modifications='byte-identical source snapshot')
        elif rel.startswith('source_canon/'):
            entry.update(role='frozen_parent_canon',source_path='design/cinematics/v2/canon/'+file.name,source_commit=PARENT,modifications='source snapshot; fresh observations in SOURCE_OBSERVATIONS.json')
        elif rel.startswith('board_inputs/'):
            original='2eda6f76760b8598.png' if file.name=='daddy.jpg' else '017532ae864e534d.png'
            entry.update(role='whole_image_board_input_thumbnail',source_path='grok_builder_2026-09-14/media/'+original,source_commit=SOURCE_MEDIA,license_provenance='Inherited project-owned reference; original full image preserved in references/media',modifications='whole-image viewing thumbnail made with ffmpeg, used only for storyboard preparation')
        files.append(entry)
    payload=''.join(f"{e['path']}\t{e['sha256']}\n" for e in files).encode()
    manifest={'schema':'reef.grok.broll-archive.v1','packet_id':'grok_broll_2026-09-19','private_visual_payload':private,'parent_game_commit':PARENT,'payload_sha256_method':'SHA-256 of sorted UTF-8 path + TAB + sha256 + LF, excluding manifest and later receipts','payload_sha256':sha(payload),'files':files,'claims':{'GENERATION_READY':False,'DELIVERY_ACCEPTED':False,'owner_first_frames_approved':0,'archive_publication':'Separate remote receipt required; this manifest cannot prove its own upload or Grok access.'}}
    name='HANDOFF_PACKET.json' if private else 'PACKAGE_MANIFEST.json'
    dump(packet/name,manifest)
    print(json.dumps({'private':private,'files':len(files),'payload_sha256':manifest['payload_sha256']}))

def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--private-stage',type=Path);a=p.parse_args();public=a.root/PACKET
    if a.private_stage:
        dest=a.private_stage/PACKET
        for file in public.rglob('*'):
            if file.is_file() and file.name not in ('PACKAGE_MANIFEST.json',) and 'receipts' not in file.parts:
                target=dest/file.relative_to(public);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(file,target)
        dump(dest/'PUBLICATION.json',{'status':'CONTENT_SNAPSHOT_REQUIRES_SEPARATE_REMOTE_RECEIPT','repository':'Ebonyks/mermaid-roshan-grok-videos','branch':'codex/grok-broll-20260919','packet_path':PACKET,'note':'Content is sealed before upload. Use the separate immutable receipt URL supplied in the public entry; do not mistake this snapshot for recipient access.','GENERATION_READY':False,'DELIVERY_ACCEPTED':False,'recipient_access':'Grok ACCESS_ACK pending'})
        seal(dest,True)
    else:seal(public,False)

if __name__=='__main__':main()

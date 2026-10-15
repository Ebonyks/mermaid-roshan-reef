"""Bind explicit reviewed takes; verify native provenance without editing pixels."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SCRIPT_SHA = 'febb9d5c7f6d82c29dcf8fa3556715577842b2284749fd2f1fea055a046d5967'
# Explicit editorial selection, never a latest-take fallback.
SELECTED_TAKES = [1,2,1,1,1,2,2,2,3,2,1,2,1,1,1,3,1,2,1,2,3,1,2,3,2,1,3,1,2,1,1,1]

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name, data):
    (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

def main():
    if sha(HERE/'story_script.json') != SCRIPT_SHA: raise ValueError('Frozen source changed')
    jobs=json.loads((HERE/'illustration_jobs.json').read_text(encoding='utf-8'))
    records=[]
    for path in sorted((HERE/'generation').glob('page_??_take?.json')):
        row=json.loads(path.read_text(encoding='utf-8'))
        native=ROOT/row['path']
        if row['script_sha256'] != SCRIPT_SHA: raise ValueError(f'Script binding: {path}')
        if not 1<=row['take']<=3: raise ValueError('Bounded page cap exceeded')
        if sha(native)!=row['sha256'] or sha(Path(row['provider_path']))!=row['sha256']: raise ValueError(f'Provider/native mismatch: {path}')
        if hashlib.sha256(row['prompt'].encode('utf-8')).hexdigest()!=row['prompt_sha256']: raise ValueError(f'Prompt mismatch: {path}')
        for ref in row['references']:
            if sha(ROOT/ref['path'])!=ref['sha256']: raise ValueError(f'Reference mismatch: {path}')
        with Image.open(native) as im:
            if im.size!=(1024,1536) or im.mode!='RGB': raise ValueError(f'Unexpected native source: {native}')
            if hashlib.sha256(im.tobytes()).hexdigest()!=row['rgb_pixel_sha256']: raise ValueError(f'RGB mismatch: {native}')
        records.append(dict(row,raw_receipt={'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path)},delivery_selected=row['take']==SELECTED_TAKES[row['page']-1]))
    if len(records)!=54 or {r['page'] for r in records}!=set(range(1,33)): raise ValueError('Expected all54 actual calls and all32 pages')
    pages=[]
    for number,take in enumerate(SELECTED_TAKES,1):
        matches=[r for r in records if r['page']==number and r['take']==take]
        if len(matches)!=1: raise ValueError(f'Explicit selection missing/ambiguous: {number}')
        row=matches[0]
        pages.append({'number':number,'take':take,'path':row['path'],'sha256':row['sha256'],'rgb_pixel_sha256':row['rgb_pixel_sha256'],'dimensions':row['dimensions']})
    if len({p['sha256'] for p in pages})!=32 or len({p['rgb_pixel_sha256'] for p in pages})!=32: raise ValueError('Repeated page bytes/pixels')
    review_names=['verification/editorial_review.json','verification/root_art_review.json','verification/independent_opening_review.json','generation_part_09_16.json','generation_part_17_24.json','generation_part_25_32.json']
    reviews=[{'path':(HERE/name).relative_to(ROOT).as_posix(),'sha256':sha(HERE/name)} for name in review_names]
    limits=[
        'Page8 middle panel: selected take2 correctly attributes both speakers but Rumi reassures before Duri explains; exact source panel order varies. Rejected take3 fixes order by misassigning speakers and is excluded.',
        'Page16 question tail angles toward Roshan beyond Nari towel; long-tail near-towel ambiguity remains for owner read-aloud review.',
        'Page21 long tails cross in empty space; endpoints target Duri and Roshan correctly; readability requires owner review.',
        'Minor drum/bell ornaments, catch-cloth colour, towel folds/cup counts and bathhouse snack set dressing vary; no changed rescue/voice plot fact.',
        'Page27 local contact repair also raises forearms and adds a small stage support surface. Complete provider output is retained; unchanged-input pixel lock is not claimed.',
        'Page22 expands one authored catch/duck panel into two distinct drawings:94 authored script panels,95 visual panels across32 native page boards.',
        'Cover uses a title linebreak in place of the source colon; generated curly apostrophes are typographic variants of source straight apostrophes.'
    ]
    selection={'schema':'rumi_voice_selected_native_pages_v1','status':'COMPLETE_OWNER_REVIEW_CANDIDATE','script_sha256':SCRIPT_SHA,'pages':pages,'review_bindings':reviews,'review_limits':limits}
    write('selected_art.json',selection)
    manifest={'schema':'rumi_voice_generation_manifest_v1','status':'COMPLETE_SOURCE_BOOK_REVIEW_CANDIDATE','script_sha256':SCRIPT_SHA,'selection':{'path':(HERE/'selected_art.json').relative_to(ROOT).as_posix(),'sha256':sha(HERE/'selected_art.json')},'source_catalog':jobs['source_catalog'],'actual_call_count':54,'initial_calls':32,'corrective_calls':22,'provider_revision':'not exposed','reported_cost':'not exposed; actual completed call count recorded','cap':'Initial plus at most two named corrective calls per page; no fourth calls','method':'32 independent newly drawn complete manga pages. Bounded own-page ImageGen repairs preserve local continuity; fresh retakes replace rejected drawings. No cross-page delivery-frame reuse, raster crop/resample, text overlay or collage assembly. Reference images supply identity/setting/prop only.','records':records,'review_bindings':reviews,'review_limits':limits,'acceptance':{'owner_story_art':'PENDING','child_read_aloud':'PENDING','print_production':'PENDING','runtime':'NOT_IN_SCOPE','cinematic':'NOT_IN_SCOPE','external_handoff':'NOT_IN_SCOPE','master_audit_satisfaction':'UNSATISFIED_UNCHANGED'}}
    write('generation_manifest.json',manifest)
    write('verification/provenance_check.json',{'status':'PASS','script_sha256':SCRIPT_SHA,'actual_calls':54,'initial_calls':32,'corrective_calls':22,'maximum_calls_per_page':max(sum(r['page']==n for r in records) for n in range(1,33)),'provider_native_byte_match_all':True,'all_prompt_hashes_match':True,'all_bound_reference_hashes_match':True,'all_native_rgb_hashes_match':True,'all_dimensions':[1024,1536],'unique_selected_file_hashes':32,'unique_selected_rgb_hashes':32,'no_cross_page_frame_reuse_review':'Agent visual review of distinct staged instants; different hashes alone do not establish semantic uniqueness; human owner review remains pending','review_limits':limits,'generation_manifest_sha256':sha(HERE/'generation_manifest.json')})
    print(json.dumps({'pages':32,'calls':54,'selection_sha256':sha(HERE/'selected_art.json'),'manifest_sha256':sha(HERE/'generation_manifest.json')}))

if __name__=='__main__': main()

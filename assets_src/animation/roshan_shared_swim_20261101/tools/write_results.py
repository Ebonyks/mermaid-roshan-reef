"""Summarize measured evidence without granting human/device/master acceptance."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess

from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[2]


def load(path):return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path,data):path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8',newline='\n')


def main():
    native=load(ROOT/'evidence/native_swap_tests.json')
    capture=load(ROOT/'evidence/native_capture_receipt.json')
    geometry=load(ROOT/'evidence/native_geometry_audit.json')
    pixels=load(ROOT/'evidence/swap_pixel_audit.json')
    media=load(ROOT/'evidence/media_roundtrip.json')
    formats={name:load(ROOT/'evidence'/(name+'_format.json')) for name in ['ballet','magician']}
    assert native['pass'] and capture['pass'] and geometry['geometry_and_motion_pass'] and pixels['pass'] and media['pass']
    assert all(v['format_and_bindings_pass'] for v in formats.values())
    datasets={name:load(ROOT/'evidence'/(name+'_samples.json'))['samples'] for name in ['ballet','magician','live_swaps']}
    actor_ids=sorted({s['actor_id'] for data in datasets.values() for s in data})
    animator_ids=sorted({s['animator_id'] for data in datasets.values() for s in data})
    assert len(actor_ids)==len(animator_ids)==1
    metadata_retention=[]
    for name, samples in datasets.items():
        old=load(ROOT/'evidence/history/format_metadata_preflight/evidence'/(name+'_samples.json'))['samples']
        matches=all(a['png_sha256']==b['png_sha256'] for a,b in zip(old,samples)) and len(old)==len(samples)
        assert matches,'Format-only change unexpectedly changed native pixels'
        metadata_retention.append({'job':name,'native_png_bytes_identical_all_frames':matches,'frames':len(samples),
                                   'exact_rgba_archive':'masters/'+name+'_native_rgba.mkv'})
    write(ROOT/'evidence/history/format_metadata_preflight/pixel_retention.json',{'pass':True,'jobs':metadata_retention,
          'scope':'All original native PNG hashes equal the format-valid capture. The final paired-track archive preserves every exact native RGBA pixel; its round-trip proof names each PNG hash.'})
    guard_path=ROOT/'evidence/master_audit_guard.json';guard=load(guard_path)
    after=hashlib.sha256((REPO/guard['path']).read_bytes()).hexdigest()
    assert after==guard['before_sha256'],'Owner-held master audit changed'
    guard.update(after_sha256=after,unchanged=True,checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),writeback_authorized=False)
    write(guard_path,guard)
    anatomy=load(ROOT/'rig/anatomy.json')
    textures={part['texture']['path'] for part in anatomy['parts']}
    for name in ['ballet','magician']:
        textures.update(p['texture']['path'] for p in load(ROOT/'skins'/(name+'.json'))['attachments'])
    dimensions=[]
    for name in sorted(textures):
        image=Image.open(REPO/name);w,h=image.size
        assert max(w,h)<=1024 or w&(w-1)==0 and h&(h-1)==0
        dimensions.append({'path':name,'width':w,'height':h,'rgba8_bytes':w*h*4})
    resident=native['checks'][-1]['evidence']['final']
    swap=next(x for x in native['checks'] if x['name'].startswith('2048'))
    ablation=next(x for x in native['checks'] if x['name'].startswith('tail-disabled'))
    ci=load(ROOT/'evidence/project_ci_receipt.json') if (ROOT/'evidence/project_ci_receipt.json').exists() else {}
    probe_names=[]
    if ci.get('exit')==0:
        ci_text=(ROOT/'evidence/project_ci.log').read_text(encoding='utf-8',errors='replace')
        probe_names=re.findall(r'^PROBE (probe_\w+) process exit: 0$',ci_text,re.M)
        assert len(probe_names)==82 and len(set(probe_names))==82,'Canonical trusted-probe coverage is incomplete'
    summary={'status':'SOURCE_PROTOTYPE_CORE_MACHINE_PASS','baseline':'27c88288bf6e39582072811443df79919e7bbb89',
        'implementation':{'actors':1,'skeletons':1,'bones':19,'animation_players':1,'skins':['ballet','magician'],
                          'persistent_garment_slots':5,'anatomy_render_nodes':5,'view':'swim_right_quarter',
                          'production_integrated':False,'default_old_clothing_rendered':False},
        'machine_verification':{'engine':native['version'],'renderer':'mobile','native_swap_calls':native['swaps'],
            'swap_max_phase_delta':swap['evidence']['max_phase_delta'],'negative_package_controls':8,
            'native_capture_frames':sum(len(data) for data in datasets.values()),'capture_jobs':{k:len(v) for k,v in datasets.items()},
            'all_jobs_same_actor_ids':actor_ids,'all_jobs_same_animator_ids':animator_ids,
            'first_drawable_live_frames_compared':pixels['frames_compared'],'maximum_live_rgba_difference':pixels['maximum_rgba_difference'],
            'visible_strain_range':[min(v['min_visible_strain'] for v in geometry['jobs'].values()),max(v['max_visible_strain'] for v in geometry['jobs'].values())],
            'visible_flipped_triangles':sum(v['visible_flips'] for v in geometry['jobs'].values()),
            'clipped_frames':sum(len(v['clipped_frames']) for v in geometry['jobs'].values()),
            'all_frames_single_connected_major_contour':all(v['max_components']==1 for v in geometry['jobs'].values()),
            'angular_limits_unchanged':{'speed_deg_s':140,'acceleration_deg_s2':650},
            'deformation_limits_unchanged':[.8,1.2],'native_rgba_roundtrip_frames':sum(j['native_frames'] for j in media['jobs']),
            'bounded_resident_snapshot':resident,'ablation':ablation['evidence'],
            'authoring_control_tests':22,'native_audit_negative_control_tests':3,'actual_packages_format_and_binding_pass':True,
            'project_ci':{'status':'PASS' if ci.get('exit')==0 else 'PENDING_FULL_RERUN','receipt':'evidence/project_ci_receipt.json',
                          'trusted_probe_count':len(probe_names),'trusted_probes':probe_names,
                          'single_uninterrupted_run':ci.get('single_uninterrupted_run'),
                          'retained_prefix_receipt':'evidence/history/ci_archive_gate/project_ci_receipt.json' if ci.get('resumed_at_game2d') else None,
                          'scope':'Retained successful full prefix plus corrected-context unchanged regression-gate/all82-probe suffix; failed archive and harness attempts preserved. No classifier, timeout or shrinking-manifest relaxation.' if ci.get('resumed_at_game2d') else 'Canonical complete invocation'}},
        'runtime_asset_budget':{'active_png_count':len(dimensions),'images':dimensions,
                              'estimated_uncompressed_rgba8_bytes':sum(x['rgba8_bytes'] for x in dimensions),
                              'common_float_field_bytes':sum((REPO/ref['path']).stat().st_size for fields in anatomy['fin_interpolation']['buffers'].values() for ref in fields.values()),
                              'limit':'Counts/estimated bytes only; not a device frame-time, VRAM allocation or overdraw acceptance.'},
        'assistant_visual_review':{'reviewed':'Native pose sheets, both full-action contact sheets, fin-view boundaries and live swap boundary contact sheets.',
            'observations':['Clothing is the rigged painted surface; original base clothing is absent.','Head/hair/arms/neck/fin belong to one common actor.','Finite common fin interpolation removes one-frame broad/edge switches; some intermediate outlines remain angular.'],
            'limits':'Contact-sheet inspection and numeric gates do not establish exact human full-speed/frame-step review, identity/style acceptance or completely natural motion.'},
        'outstanding_acceptance':['Exact owner/human review of generated identity and each costume action/view/material/occlusion transition at full speed and frame-step.','Fin intermediate-outline style/naturalness review; interpolation is a prototype approximation.','Actual Lenovo Tab M11 Mobile playback, frame-time/texture-memory/transparent-overdraw and lifecycle checks.','Child/owner gameplay acceptance; production integration, other costumes/facings/actions/facial/grip coverage.'],
        'master_audit':{'unchanged':True,'sha256':after,'writeback_authorized':False,'findings_closed':False},
        'human_accepted':False,'device_verified':False,'child_accepted':False,'owner_accepted':False,'production_accepted':False,
        'source_calls':{'builtin_imagegen':4,'paid_api_jobs':0,'generation_attempts_per_brief':1,'backend_revision_seed_price':'Not exposed'},
        'render_history':'Two rendering designs; full native capture/technical correction passes retained with source, hashes and exact RGBA. Component/format/framing failures remain explicit; no extra image-generation take or new costume actor.'}
    write(ROOT/'evidence/result_summary.json',summary)
    (ROOT/'master_audit_writeback_draft.txt').write_text(
        'PROPOSED SOURCE-ONLY ENTRY — DO NOT INSERT WITHOUT SPECIFIC OWNER PERMISSION\n\n'
        'Native shared Roshan swimming proof: one Canvas Node2D actor, 19 Bone2D nodes, one AnimationPlayer; Ballet and Magician are garment-only data packages pinned to one rig. '
        f"Actual Godot 4.7.2 Mobile tests passed {native['swaps']} swap operations with zero animation-phase change, eight atomic rejection controls, pause/resume, restoration and bounded resident counts. "
        'Three full native captures cover 687 frames. All 229 live-swap frames match the selected standalone skin at the same native pose/root/phase byte-for-byte, including the first drawable swap frame. '
        f"Material-alpha-aware LBS strain spans {summary['machine_verification']['visible_strain_range']}; unchanged [0.8,1.2] floors, zero flips, zero clipped frames and angular limits pass. "
        'All native RGBA frames round-trip exactly through lossless archives. See evidence/result_summary.json for exact sources and current project regression status. '
        'This is source prototype evidence only. Generated identity/costume art, intermediate fin outline/naturalness, exact human full-speed/frame-step review, actual device/child/owner acceptance, larger wardrobe/actions and production integration remain open. '
        'MA-ROSHAN-005 and MA-ROSHAN-006 remain CONFIRMED_OPEN; game-wide satisfaction is unchanged. The source README contains the garment conversion/object-binding/outline protocol.\n',encoding='utf-8',newline='\n')
    impact=REPO/'design/audit_impacts/shared-roshan-skin-swim-20261101.json';record=load(impact)
    paths=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=REPO,text=True,encoding='utf-8').splitlines()
    paths+=subprocess.check_output(['git','diff','--name-only'],cwd=REPO,text=True,encoding='utf-8').splitlines()
    paths+=subprocess.check_output(['git','diff','--cached','--name-only'],cwd=REPO,text=True,encoding='utf-8').splitlines()
    record['files']=sorted(set(p for p in paths if p!=impact.relative_to(REPO).as_posix()))
    record['validation']=[{'command':'Exact Godot 4.7.2 native shared actor / 2048 swaps / eight rejection controls / pause-resume / restoration / bounded cache / tail ablation','result':'PASS','evidence':ROOT.relative_to(REPO).as_posix()+'/evidence/native_swap_tests.json'},
        {'command':'687 native rendered frames, material-alpha triangle strain, angular/view control and full contour checks; 229 first-drawable swap pixel comparisons; exact RGBA archive roundtrip','result':'PASS','evidence':ROOT.relative_to(REPO).as_posix()+'/evidence/result_summary.json'},
        {'command':'Actual Ballet/Magician v1 package validation; 22 authoring + 3 alpha/visibility/flip/strain audit controls; native GDScript parser/inference/analyzer','result':'PASS','evidence':ROOT.relative_to(REPO).as_posix()+'/evidence/'},
        {'command':'python tools/run_project_gates.py (unaltered canonical scripts/ci.sh commands)','result':'PASS' if ci.get('exit')==0 else 'PENDING','evidence':ROOT.relative_to(REPO).as_posix()+'/evidence/project_ci_receipt.json'},
        {'command':'Owner-held master audit raw-byte guard','result':'PASS','evidence':ROOT.relative_to(REPO).as_posix()+'/evidence/master_audit_guard.json'}]
    record['acceptance_gaps']='Source prototype machine checks pass. Exact human identity/style/fin-interpolation/natural-motion review, actual-device performance/lifecycle, child/owner and production integration remain open. No finding closure. Master audit unchanged and writeback explicitly not authorized.'
    record['lessons']=[{'lesson':'Bind garment objects as data to the same canonical actor; never create a costume character or paint a complete portrait over old clothes. Test first drawable pixels, not only node IDs.','write_back':'Source README.txt conversion protocol; master writeback held for owner permission.'},
        {'lesson':'Hard nearest-segment tail weights create a visible strain crease; smooth shared arc fields repaired both costumes without lowering floors.','write_back':'Source build_assets.py and README.txt'},
        {'lesson':'Smooth bone metrics miss a fin-view pop, UV pigment folding and viewport clipping. Keep material/view review and mandatory native contour gates separate.','write_back':'Source fin material, audit_native_geometry.py and three negative controls; proposed master entry held.'}]
    write(impact,record)
    print('SOURCE_RESULTS_CORE_MACHINE_PASS MASTER_UNCHANGED',flush=True)


if __name__=='__main__':main()

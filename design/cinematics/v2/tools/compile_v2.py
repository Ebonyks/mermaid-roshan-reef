#!/usr/bin/env python3
"""Guarded plan-to-canonical adapter; missing approvals never get defaulted."""
import argparse
import json
import sys
from pathlib import Path
import validate_v2 as v

PROJECT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT / 'tools'))
from audit_imagine_handoff import audit_shot

def compile_shot(root, shot_id, packet_dir):
    card_path = v.inside(root, f'shots/{shot_id}/CARD.json')
    errors = []
    v.check_card(card_path, errors, root)
    card = v.read(card_path)
    errors.extend(v.readiness(card, root))
    if errors:
        raise ValueError('NOT_READY: ' + '; '.join(errors))
    # The packet must already contain approved image bytes, prompt and reviewed locks.
    # Never fetch an arbitrary URL or substitute a room source into the opening slot.
    locks = v.read(packet_dir / 'EXECUTION_LOCKS.json')
    handoff = v.read(packet_dir / 'IMAGINE_HANDOFF.json')
    if locks.get('plan_sha256') != v.fingerprint(card):
        raise ValueError('Execution locks are stale or for a different plan')
    output = {k: card[k] for k in ('shot_id','duration_seconds','aspect_ratio','delivery_size',
        'exact_cast','camera','must_move','must_not_move','end_state','negative_constraints','prompt_sha256')}
    output.update(schema='imagine-shot-packet-v2',movie_id=card['event_id'],mode='image_to_video',
        output_disposition='motion_reference_only',bound_references=card['binds'],
        causal_chain=card['causal_chain'],beat_ids=card['beat_ids'])
    for name in ('character_locks','location_lock','continuity','sequence_position','prompt_path'):
        output[name] = locks[name]
    output['non_pixel_references'] = locks.get('non_pixel_references', [])
    outpath = v.inside(packet_dir, f'shots/{shot_id}/SHOT_PACKET.json')
    if outpath.exists():
        raise ValueError('Refusing to overwrite an existing execution packet; create a new attempt directory')
    outpath.parent.mkdir(parents=True,exist_ok=True)
    outpath.write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    errors = audit_shot(packet_dir,outpath,handoff)
    if errors:
        # Retain the explicitly failed candidate for inspection; never print readiness.
        raise ValueError('CANONICAL_EXPORT_FAILED (retained as rejected draft): '+'; '.join(errors))
    return outpath

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('shot_id');ap.add_argument('packet_dir',type=Path)
    ap.add_argument('--root',type=Path,default=v.ROOT)
    args=ap.parse_args()
    try:
        path=compile_shot(args.root,args.shot_id,args.packet_dir)
    except (ValueError,OSError,KeyError,TypeError) as exc:
        print(str(exc));return 1
    print(f'EXPORTED {path}; run canonical audit_imagine_handoff.py on the entire packet --require-ready')
    return 0

if __name__=='__main__':raise SystemExit(main())

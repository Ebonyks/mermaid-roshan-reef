"""Freeze only executable rig dependencies, without editing any outfit worktree."""
from pathlib import Path
import datetime, hashlib, json, re, shutil, subprocess

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
HOME_REPO = Path('C:/Users/Peter/Documents/mermaid-roshan-reef')
WORKTREES = Path('C:/Users/Peter/.codex/worktrees')
GROUPS = [
    ('performance', WORKTREES/'roshan-job-rig-performance-20261101/mermaid-roshan-reef/assets_src/animation/roshan_job_rig_performance_20261101/demo', 'seed.gd', ['original','ballet','magician']),
    ('kitchen', WORKTREES/'roshan-kitchen-garden-rig-20261101/mermaid-roshan-reef/assets_src/animation/roshan_job_rig_kitchen_garden_20261101/demo', 'study.gd', ['chef','farmer']),
    ('care', HOME_REPO/'tmp/roshan-care-learning-rig-20261101/assets_src/animation/roshan_job_rig_care_learning_20261101/godot', 'study.gd', ['doctor','teacher']),
    ('creative', WORKTREES/'roshan-creative-space-20261101/mermaid-roshan-reef/assets_src/animation/roshan_job_rig_creative_space_20261101/godot', 'study.gd', ['painter','astronaut']),
    ('investigation', HOME_REPO/'tmp/rig-investigation-worktree/assets_src/animation/roshan_job_rig_investigation_20261101/demo', 'study.gd', ['detective','geologist']),
    ('craft', WORKTREES/'roshan-care-craft-rig-20261101/mermaid-roshan-reef/assets_src/animation/roshan_job_rig_care_craft_20261101/demo', 'seed_study.gd', ['candymaker','nursery']),
    ('sport', WORKTREES/'roshan-sport-stage-20261101/mermaid-roshan-reef/assets_src/animation/roshan_job_rig_sport_stage_20261101/demo', 'base.gd', ['boxer','racer','popstar']),
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    (ROOT/'.gdignore').write_bytes(b'')
    (ROOT/'.gitattributes').write_text('* -text\n', encoding='utf-8', newline='\n')
    (ROOT/'.gitignore').write_text('.godot/\n**/.godot/\n**/__pycache__/\nraw_*/\n*.import\n*.uid\n', encoding='utf-8', newline='\n')
    records, groups = [], []
    allowed = {'.png','.json','.gdshader'}
    for key, origin, entry, themes in GROUPS:
        dest = ROOT/'sources'/key
        dest.mkdir(parents=True, exist_ok=True)
        queue, seen = [], set()

        def local(path):
            path = path.resolve()
            if path.is_relative_to(origin):
                return path.relative_to(origin).as_posix()
            return 'external/'+sha(str(path.parent).encode())[:12]+'/'+path.name

        def enqueue(path):
            path = path.resolve()
            if path.is_file() and path not in seen:
                seen.add(path)
                queue.append(path)

        def directory(path):
            if path.is_dir():
                for item in path.rglob('*'):
                    if item.suffix.lower() in allowed and '.godot' not in item.parts:
                        enqueue(item)

        def uri(value):
            if value == 'res://':
                return value
            path = (origin/value[6:]).resolve()
            if path.is_dir():
                directory(path)
                # Directory identifiers use the same parent mapping as their files.
                mapped = local(path/'__prefix__').rsplit('/',1)[0]
                return 'res://'+mapped+('/' if value.endswith('/') else '')
            if path.exists():
                enqueue(path)
            elif path.parent.is_dir():
                directory(path.parent)  # e.g. dynamically suffixed eyes_half.png
            return 'res://'+local(path)

        enqueue(origin/entry)
        directory(origin)
        while queue:
            source = queue.pop(0)
            data = source.read_bytes()
            output = data
            edits = []
            if source.suffix in {'.gd','.gdshader'}:
                text = data.decode('utf-8')
                def replace(match):
                    old = match.group(0)
                    new = uri(old)
                    if old != new:
                        edits.append({'from':old,'to':new})
                    return new
                text = re.sub(r'res://[^\"\'\r\n]*', replace, text)
                output = text.encode('utf-8')
            elif source.suffix == '.json':
                obj = json.loads(data)
                def textures(value):
                    if isinstance(value,list):
                        for child in value:
                            textures(child)
                    elif isinstance(value,dict):
                        for name,child in list(value.items()):
                            if name == 'texture' and isinstance(child,str) and child.endswith('.png'):
                                new = uri('res://'+child)[6:]
                                if child != new:
                                    value[name] = new
                                    edits.append({'texture_from':child,'texture_to':new})
                            else:
                                textures(child)
                textures(obj)
                if edits:
                    output = (json.dumps(obj,separators=(',',':'))+'\n').encode()
            relative = local(source)
            target = dest/relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(output)
            records.append({'group':key,'source_path':str(source),'source_sha256':sha(data),'path':target.relative_to(ROOT).as_posix(),'sha256':sha(output),'bytes':len(output),'edits':edits,'source_status':'Provisional source candidate; known prior defects/rejections are retained; no acceptance inferred.'})
        (dest/'swim_source.gd').write_bytes((dest/entry).read_bytes())
        for filename in ['capture.gd','swim_motion.gd']:
            shutil.copyfile(ROOT/'shared'/filename,dest/filename)
        (dest/'project.godot').write_text('config_version=5\n[application]\nconfig/name="Laura-led Roshan swim comparison"\nconfig/features=PackedStringArray("4.7","Mobile")\n[display]\nwindow/size/viewport_width=1280\nwindow/size/viewport_height=720\n[rendering]\nrenderer/rendering_method="mobile"\nrenderer/rendering_method.mobile="mobile"\n',encoding='utf-8',newline='\n')
        groups.append({'group':key,'themes':themes,'project':'sources/'+key,'entry_source':entry,'source_project':str(origin)})
    reference = HOME_REPO/'.worktrees/roshan-laura-docs-20261101/design/animation/ROSHAN_MOVEMENT_LANGUAGE.md'
    (ROOT/'references').mkdir(exist_ok=True)
    # A .txt source copy avoids inventing a second authoritative domain document.
    profile_bytes = subprocess.check_output(['git','show','c966b3c4bb72e3b8f145afe065e1e23d7f39ebe3:design/animation/ROSHAN_MOVEMENT_LANGUAGE.md'],cwd=REPO)
    (ROOT/'references/laura_v2_profile.txt').write_bytes(profile_bytes)
    (ROOT/'references/task_start.json').write_bytes((HOME_REPO/'tmp/laura_swim_scaffold/task_start.json').read_bytes())
    (ROOT/'sources.json').write_text(json.dumps({'frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'profile_revision':'c966b3c4bb72e3b8f145afe065e1e23d7f39ebe3','profile_sha256':sha(profile_bytes),'groups':groups,'files':records,'generated_art_calls':0,'production_integration':False},indent=2)+'\n',encoding='utf-8',newline='\n')
    print('FROZEN',len(records),'source dependencies;',sum(len(g['themes']) for g in groups),'costumes;',sum(r['bytes'] for r in records)//1048576,'MiB')


if __name__ == '__main__':
    main()

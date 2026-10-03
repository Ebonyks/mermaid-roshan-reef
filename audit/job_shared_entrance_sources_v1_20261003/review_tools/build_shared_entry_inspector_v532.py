from pathlib import Path
import html, json, shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');q=b/'audit/job_shared_entrance_sources_v1_20261003'
plan=json.loads((q/'PLAN_AND_SOURCE_BOUNDARY.json').read_text(encoding='utf-8'))
out=['<!doctype html><html lang="en"><meta charset="utf-8"><title>Shared entrance native source inspector</title><style>body{background:#e7f4f3;color:#21304c;font:18px/1.5 system-ui;margin:24px}article{background:#fff;border-radius:18px;margin:28px 0;padding:20px}a{color:#514886}.sheet{display:block;max-width:100%;background:#bbc9db}.cells{display:flex;flex-wrap:wrap;gap:16px}.cell{width:220px;background:#dbe8f2;border-radius:12px;padding:12px}.detail{position:relative;overflow:hidden;background:#c3d3de;margin:8px 0}.detail img{position:absolute;max-width:none}small{font-size:14px}</style><h1>Kitchen and Opera entrance sources</h1><p>18 existing originals; 104 authored cells. Read-only CSS windows display the original image pixels. Each frame is a discrete authored state. No generated in-betweens, source pixel changes, runtime binding or mounted-action acceptance.</p>']
for x in plan['source_files']:
    src='/'+x['path'];out.append(f'<article id="{x["id"]}"><h2>{x["id"]} — {html.escape(Path(x["path"]).stem)}</h2><p>Native {x["dimensions"][0]} × {x["dimensions"][1]} · Review pending</p><a href="{src}">Full native original</a><img class="sheet" src="{src}" alt="Complete native {html.escape(Path(x["path"]).stem)}"><div class="cells">')
    for c in x['cells']:
        rx,ry,rw,rh=c['region'];bx,by,ex,ey=c['alpha_bbox'];bx=max(0,bx-8);by=max(0,by-8);ex=min(rw,ex+8);ey=min(rh,ey+8)
        scale=min(208/(ex-bx),232/(ey-by));ww=(ex-bx)*scale;hh=(ey-by)*scale
        out.append(f'<div class="cell" id="{x["id"]}-C{c["index"]:02d}"><b>Cell {c["index"]}</b><div class="detail" style="width:{ww:.4f}px;height:{hh:.4f}px"><img src="{src}" alt="Native authored cell {c["index"]} of {html.escape(Path(x["path"]).stem)}" style="width:{x["dimensions"][0]*scale:.4f}px;height:{x["dimensions"][1]*scale:.4f}px;left:{-(rx+bx)*scale:.4f}px;top:{-(ry+by)*scale:.4f}px"></div><small>Exact cell {c["region"]}<br>Original alpha bbox {c["alpha_bbox"]}<br>Visual opinion pending</small></div>')
    out.append('</div></article>')
out.append('</html>');(q/'SOURCE_INSPECTOR.html').write_text('\n'.join(out),encoding='utf-8',newline='\n')
shutil.copyfile(__file__,q/'review_tools/build_shared_entry_inspector_v532.py')
ip=b/'design/audit_impacts/job-shared-entrance-source-review-20261003.json';impact=json.loads(ip.read_text());impact['files']=sorted(set(impact['files'])|{p.relative_to(b).as_posix() for p in q.rglob('*') if p.is_file()});new=ip.with_name(ip.name+'.new');new.write_text(json.dumps(impact,indent=2)+'\n',encoding='utf-8');new.replace(ip)
ap=b/'tmp/v2_preview_allowed.json';allowed=json.loads(ap.read_text());allowed=sorted(set(allowed)|set(impact['files'])|{x['path'] for x in plan['source_files']});new=ap.with_name(ap.name+'.new');new.write_text(json.dumps(allowed,indent=2)+'\n',encoding='utf-8');new.replace(ap)
print('READ_ONLY_INSPECTOR_READY|18 original images|104 CSS cell windows|no source bitmap change')

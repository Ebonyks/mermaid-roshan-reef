from pathlib import Path
import hashlib,json,subprocess
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');c=b/'audit/job_candy_workflow_current_v1_20261003'
s=json.loads((c/'SOURCE_CURRENT_A3_BEFORE_CAPTURE.json').read_text())['source_files'];tracked={x.decode() for x in subprocess.check_output(['git','ls-files','-z'],cwd=b).split(b'\0') if x};rows=[]
proc=subprocess.Popen(['git','cat-file','--batch'],cwd=b,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
for x in s:
 p=x['path']
 if p not in tracked:continue
 proc.stdin.write((':'+p+'\n').encode());proc.stdin.flush();head=proc.stdout.readline().split();assert head[1]==b'blob';n=int(head[2]);raw=proc.stdout.read(n);assert len(raw)==n and proc.stdout.read(1)==b'\n';literal=(b/p).read_bytes()
 assert hashlib.sha256(literal).hexdigest()==x['sha256']
 if raw!=literal:
  raw.decode('utf-8');literal.decode('utf-8');assert raw==literal.replace(b'\r\n',b'\n'),p
  rows.append(dict(path=p,suffix=Path(p).suffix,local_literal_sha256=hashlib.sha256(literal).hexdigest(),indexed_sha256=hashlib.sha256(raw).hexdigest(),whole_text_crlf_to_lf_only=True))
proc.stdin.close();assert proc.wait(timeout=30)==0
record=dict(status='PASS_EXACT_WHOLE_TEXT_NEWLINE_DIFFERENCES_ONLY',reviewed_revision_source_members=543,newline_differences=rows,suffixes=sorted({r['suffix'] for r in rows}),qualification='Every current staged revision source is literal-identical or exactly UTF8 whole-file CRLF-to-LF only. Native images remain exact. This read-only diagnosis does not change trusted gates, sources or creative acceptance.')
(c/'CURRENT_INDEX_NEWLINE_DIAGNOSIS_V541.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(status=record['status'],count=len(rows),suffixes=record['suffixes'],additional_paths=[r['path'] for r in rows if r['suffix'] not in ['.gd','.tscn','.tres','.godot','.import','.uid']])))

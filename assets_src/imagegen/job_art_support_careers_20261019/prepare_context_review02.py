from pathlib import Path
s=Path(__file__).resolve().parent
t=(s/'build_context_review01.py').read_text(encoding='utf-8').replace("'review_context01'","'review_context02'").replace("['current04', 'current07']","['current08', 'current09']")
t=t.replace("herd = row['id'].startswith('farmer-2-herd-')", "herd = row['id'].startswith(('farmer-3-picnic-', 'magician-6-cabinet-'))")
t=t.replace("version == 'current04'", "version == 'current08'").replace("version == 'current07'", "version == 'current09'")
t=t.replace('current04 non-HERD functions unchanged; current07 refreshed HERD.','current08 unchanged functions plus current09 refreshed PICNICguide/cabinet whole key; original exact source receipts retained. New asset assertion changes test only, all earning checks retained.')
t=t.replace('Diagnostic contact sheets only; original capture pixels remain untouched.','Diagnostic contact sheets02 only; original capture pixels remain untouched.')
p=s/'build_context_review02.py';assert not p.exists();p.write_text(t,encoding='utf-8')

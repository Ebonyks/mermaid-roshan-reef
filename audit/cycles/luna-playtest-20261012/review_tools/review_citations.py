"""Inventory report citations without treating an ID match as causal proof."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re

ROOT = Path(__file__).resolve().parents[4]
CYCLE = ROOT / 'audit/cycles/luna-playtest-20261012'

def main():
    sources = ['design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md',
               'audit/MASTER_AUDIT_2026-08-09.md',
               'audit/findings/ACTIVE_FINDINGS_2026-08-13.md']
    texts = [(ROOT / p).read_text(encoding='utf-8') for p in sources]
    rules = set(re.findall(r'`(DL-[A-Z0-9]+-\d+)`', texts[0]))
    findings = set(re.findall(r'MA-[A-Z0-9]+-\d+', '\n'.join(texts[1:])))
    used_rules, used_findings, errors, rows = set(), set(), [], []
    for path in sorted((CYCLE / 'reports').glob('L*.json')):
        report = json.loads(path.read_text(encoding='utf-8'))
        for i, observation in enumerate(report['observations'], 1):
            used_rules.update(observation['rules'])
            used_findings.update(observation['existing_findings'])
            for value in observation['rules']:
                if value not in rules: errors.append(f'{path.name}-O{i}: undefined {value}')
            for value in observation['existing_findings']:
                if value not in findings: errors.append(f'{path.name}-O{i}: undefined {value}')
        rows.append({'report': path.relative_to(ROOT).as_posix(),
                     'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    result = {'schema': 'luna_citation_inventory/1', 'status': 'FAIL' if errors else 'PASS',
              'checked_utc': datetime.now(timezone.utc).isoformat(), 'reports': rows,
              'rules': sorted(used_rules), 'findings': sorted(used_findings), 'errors': errors,
              'authority_sources': sources,
              'scope': 'ID existence and exact report bytes only. Raw proposed mappings and source interpretations remain scoped reviewer claims; this does not endorse relevance, verify every line assertion or establish new defects.'}
    (CYCLE / 'verification/citations.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ['reports', 'rules', 'findings']}))
    if errors: raise SystemExit(1)

if __name__ == '__main__': main()

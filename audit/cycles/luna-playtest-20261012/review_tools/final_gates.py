"""Retain final documentation, diagnostic parser and evidence-helper checks."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, subprocess, sys

ROOT = Path(__file__).resolve().parents[4]
CYCLE = ROOT / 'audit/cycles/luna-playtest-20261012'

def main():
    diagnostics = [p.relative_to(ROOT).as_posix() for p in sorted((CYCLE / 'review_tools').glob('*.gd'))]
    commands = [[sys.executable, '-B', 'tools/audit_document_authority.py'],
                [sys.executable, '-B', 'tools/audit_development.py', '--base', 'auto'],
                [sys.executable, '-B', '-m', 'unittest', 'tools.tests.test_audit_document_authority', 'tools.tests.test_audit_development'],
                [sys.executable, '-B', '-m', 'gdtoolkit.parser', *diagnostics],
                [sys.executable, '-B', 'tools/lint_inference.py', *diagnostics],
                ['git', 'diff', '--check'],
                ['git', 'diff', '--exit-code', '--', 'scripts', 'scenes', 'assets', 'project.godot']]
    rows, output = [], []
    for command in commands:
        proc = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
        rows.append({'command': command, 'exit_code': proc.returncode})
        output += [json.dumps(command) + '\n', proc.stdout, proc.stderr]
    helper_rows = []
    for p in sorted((CYCLE / 'review_tools').glob('*.py')):
        try:
            ast.parse(p.read_text(encoding='utf-8'), filename=str(p))
        except SyntaxError as error:
            rows.append({'command': ['helper_AST', p.relative_to(ROOT).as_posix()], 'exit_code': 1})
            output.append('HELPER_AST FAIL ' + str(error) + '\n')
            continue
        helper_rows.append({'path': p.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
    output.append(f'HELPER_AST ALL {len(helper_rows)} OK\n')
    log = CYCLE / 'verification/final_gates.log'
    log.write_text(''.join(output), encoding='utf-8')
    result = {'schema': 'luna_final_gates/1', 'status': 'PASS' if all(r['exit_code'] == 0 for r in rows) else 'FAIL',
              'checked_utc': datetime.now(timezone.utc).isoformat(), 'commands': rows,
              'helper_ast': helper_rows, 'log_sha256': hashlib.sha256(log.read_bytes()).hexdigest(),
              'scope': 'Final documentation/impact and diagnostic source checks. The unchanged game CI has separate retained 82/82 receipts; no gameplay, device, child or owner acceptance.'}
    (CYCLE / 'verification/final_gates.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'commands': rows, 'helper_ast_count': len(helper_rows)}))
    if result['status'] != 'PASS': raise SystemExit(1)

if __name__ == '__main__': main()

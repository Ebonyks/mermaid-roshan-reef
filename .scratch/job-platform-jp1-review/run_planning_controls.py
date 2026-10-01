from pathlib import Path
import hashlib, importlib, importlib.util, sys, unittest

base = Path("C:/Users/Peter/Documents/mermaid-roshan-reef/.scratch/job-platform-jp1-review")
project = Path("H:/CodexWorktrees/mermaid-roshan-reef-job-platform-jp1-20261001")
package = importlib.import_module("tools")

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

for leaf in ["content_gd_literals", "content_source_refs", "content_build"]:
    module = load("tools." + leaf, base / "final/after/tools" / (leaf + ".py"))
    setattr(package, leaf, module)
authority = load("tools.audit_document_authority", project / "tools/audit_document_authority.py")
setattr(package, "audit_document_authority", authority)
module = load("tools.tests.test_audit_document_authority_candidate", project / "tools/tests/test_audit_document_authority.py")
names = [
    "test_planning_mask_resolves_fixed_catalogue_reference",
    "test_planning_mask_rejects_wrong_catalogue_source_or_expression",
    "test_planning_mask_fails_closed_without_catalogue",
    "test_planning_mask_ignores_quoted_literal_decoy",
    "test_stale_global_mask_fails_even_with_correct_symbol_present",
    "test_planning_fact_gate_fails_closed_on_missing_or_malformed_source",
    "test_active_planning_gates_preserve_historical_engine_evidence",
    "test_stale_engine_in_each_active_gate_fails",
    "test_changed_chapter_mask_or_order_requires_doc_update",
]
suite = unittest.TestSuite(module.DocumentAuthorityTests(name) for name in names)
result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
for path in [project / "tools/audit_document_authority.py", project / "tools/tests/test_audit_document_authority.py"]:
    print("SOURCE|" + path.as_posix() + "|" + hashlib.sha256(path.read_bytes()).hexdigest())
sys.exit(0 if result.wasSuccessful() else 1)

from pathlib import Path
import importlib, importlib.util, sys, unittest

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
module = load("tools.tests.test_content_build_candidate", base / "tools/tests/test_content_build.py")
module.ROOT = project
names = unittest.defaultTestLoader.getTestCaseNames(module.ContentBuildTests) if sys.argv[1:] == ["--all"] else sys.argv[1:] or ["test_save_source_proof_ignores_quoted_code_and_rejects_lexical_spoofs", "test_save_bound_proof_cannot_be_relocated_to_unrelated_scope", "test_legacy_literal_checkpoint_proof_requires_exact_unconditional_order_and_site"]
suite = unittest.TestSuite(module.ContentBuildTests(name) for name in names)
result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)

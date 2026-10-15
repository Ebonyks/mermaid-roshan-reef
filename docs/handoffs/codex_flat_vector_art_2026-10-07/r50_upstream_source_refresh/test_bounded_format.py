import unittest,tempfile,importlib.util,json
from pathlib import Path
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location("bounded50test",P/"bounded_json.py");A=importlib.util.module_from_spec(s);s.loader.exec_module(A)
s=importlib.util.spec_from_file_location("legacy38test",P.parent/"r38_glyph_reconciliation/bounded_json.py");L=importlib.util.module_from_spec(s);s.loader.exec_module(L)
class FormatTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(prefix="r50_format_guard_");self.root=Path(self.tmp.name).resolve();assert self.root.parent==Path(tempfile.gettempdir()).resolve();self.p=self.root/"evidence.json"
 def tearDown(self):
  assert self.root.parent==Path(tempfile.gettempdir()).resolve()and self.root.name.startswith("r50_format_guard_");self.tmp.cleanup()
 def write_big(self):
  d={"schema":"reef.runtime_path_json_inventory/1","text":"heart ♥ \" quoted\n"*230000};raw=(json.dumps(d,indent=2)+"\n").encode();A.write_exact(self.p,raw);return raw
 def test_exact_unicode_and_escape_roundtrip(self):
  raw=self.write_big();self.assertEqual(A.logical_bytes(self.p),raw);self.assertTrue(all(x.stat().st_size<4194304 for x in self.root.iterdir()))
 def test_tampered_part_rejected(self):
  self.write_big();idx=json.loads(self.p.read_text());part=self.root/idx["fragments"][0]["path"];part.write_bytes(part.read_bytes()+b" ");self.assertRaises(ValueError,A.read_document,self.p)
 def test_path_escape_rejected(self):
  self.write_big();idx=json.loads(self.p.read_text());idx["fragments"][0]["path"]="../escape.json";self.p.write_text(json.dumps(idx));self.assertRaises(ValueError,A.read_document,self.p)
 def test_duplicate_json_keys_rejected(self):self.assertRaises(ValueError,A.parse,b'{"a":1,"a":2}')
 def test_undeclared_logical_schema_rejected(self):
  self.assertRaises(ValueError,A.write_exact,self.p,json.dumps({"schema":"unapproved.runtime.model","text":"x"*4000000}).encode())
 def test_original_reader_keeps_original_scope(self):
  self.write_big();self.assertRaises(ValueError,L.read_document,self.p)
 def test_original_scan_caps_unchanged(self):
  self.assertEqual((A.MAX_PLAIN_BYTES,A.FRAGMENT_BYTES),(L.MAX_PLAIN_BYTES,L.FRAGMENT_BYTES));self.assertEqual(A.ALLOWED_LOGICAL_SCHEMAS-L.ALLOWED_LOGICAL_SCHEMAS,{"reef.runtime_path_json_inventory/1"})
 def test_duplicate_fragment_count_rejected(self):
  self.write_big();idx=json.loads(self.p.read_text());idx["fragments"].append(idx["fragments"][0]);idx["fragment_count"]+=1;self.p.write_text(json.dumps(idx));self.assertRaises(ValueError,A.read_document,self.p)
if __name__=="__main__":unittest.main()

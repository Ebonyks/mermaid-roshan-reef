from pathlib import Path
import hashlib,json,tempfile,unittest
from register_parts_v51 import load_register,MAX_JSON_BYTES
class RegisterPartsTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.d=Path(self.tmp.name);self.part={'items':[{'id':'CELL-00','path':'assets/toy.png'}]};self.root={'items':[{'id':'SOURCE-00','path':'assets/toy.png'}],'counts':{'registered_items':2}};self.save_part();self.save_root()
 def tearDown(self):self.tmp.cleanup()
 def save_part(self):
  raw=json.dumps(self.part).encode();(self.d/'PART.json').write_bytes(raw);self.root['item_shards']=[{'path':'PART.json','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'items':len(self.part['items'])}]
 def save_root(self):(self.d/'ALL_ITEMS.json').write_text(json.dumps(self.root),encoding='utf-8')
 def test_complete_source_and_cell_load(self):self.assertEqual([x['id'] for x in load_register(self.d)['items']],['SOURCE-00','CELL-00'])
 def test_missing_part_blocks_all_claims(self):
  (self.d/'PART.json').unlink()
  with self.assertRaises(FileNotFoundError):load_register(self.d)
 def test_changed_bytes_block_all_claims(self):
  raw=(self.d/'PART.json').read_bytes();(self.d/'PART.json').write_bytes(raw.replace(b'CELL-00',b'CELL-01'))
  with self.assertRaisesRegex(ValueError,'byte/hash'):load_register(self.d)
 def test_duplicate_ids_across_parts_block_all_claims(self):
  self.part['items'][0]['id']='SOURCE-00';self.save_part();self.save_root()
  with self.assertRaisesRegex(ValueError,'Duplicate'):load_register(self.d)
 def test_path_escape_blocks_all_claims(self):
  self.root['item_shards'][0]['path']='../PART.json';self.save_root()
  with self.assertRaisesRegex(ValueError,'Unsafe'):load_register(self.d)
 def test_over_ceiling_descriptor_blocks_all_claims(self):
  self.root['item_shards'][0]['bytes']=MAX_JSON_BYTES+1;self.save_root()
  with self.assertRaisesRegex(ValueError,'descriptor'):load_register(self.d)
 def test_oversized_file_blocks_all_claims(self):
  (self.d/'PART.json').write_bytes(b' '*(MAX_JSON_BYTES+1))
  with self.assertRaisesRegex(ValueError,'4MiB'):load_register(self.d)
 def test_part_count_mismatch_blocks_all_claims(self):
  self.root['item_shards'][0]['items']=2;self.save_root()
  with self.assertRaisesRegex(ValueError,'item-count'):load_register(self.d)
 def test_total_count_mismatch_blocks_all_claims(self):
  self.root['counts']['registered_items']=3;self.save_root()
  with self.assertRaisesRegex(ValueError,'Assembled'):load_register(self.d)
if __name__=='__main__':unittest.main(verbosity=2)

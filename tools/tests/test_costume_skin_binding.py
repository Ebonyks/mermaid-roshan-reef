"""Corruption controls for the costume interchange boundary, not visual acceptance."""
from pathlib import Path
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from PIL import Image
from tools.validate_costume_skin import InvalidSkin, validate_skin


class CostumeSkinBindingTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        Image.new('RGBA',(16,16),(180,100,50,255)).save(self.root/'garment.png')
        Image.new('RGBA',(16,16),(80,60,40,255)).save(self.root/'identity.png')
        self.write('skeleton.json',{'bones':[{'name':'Root','parent':None,'head':[0,0],'tail':[0,1]},{'name':'Torso','parent':'Root','head':[0,1],'tail':[0,2]}]})
        self.mesh={'format':'roshan.attachment-mesh/1','space':'canonical_canvas_px','vertices':[[0,0],[16,0],[0,16]],'uv':[[0,0],[16,0],[0,16]],'triangles':[[0,1,2]],'weights':{'Torso':[1,1,1]}}
        self.write('tunic.json',self.mesh)
        self.rig={'format':'roshan.rig-binding/1','rig_id':'format_test_only','version':'1','status':'prototype','skeleton':self.ref('skeleton.json'),'bones':['Root','Torso'],'views':{'front':{'canvas':[16,16],'slots':{'body_front':{'required':True,'modes':['weighted'],'layer':1},'hat':{'required':False,'modes':['rigid'],'layer':2}}}},'sockets':{'hat':{'bone':'Torso','offset':[0,0]}},'identity_assets':[self.ref('identity.png')],'templates':{'tunic':self.ref('tunic.json')}}
        self.write('rig.json',self.rig)
        self.skin={'format':'roshan.skin/1','skin_id':'toy_tunic','rig':{'id':self.rig['rig_id'],'version':'1','contract_sha256':self.ref('rig.json')['sha256']},'views':['front'],'attachments':[{'id':'tunic','view':'front','slot':'body_front','mode':'weighted','texture':self.ref('garment.png'),'geometry':self.ref('tunic.json'),'template_id':'tunic'}],'coverage':{'front':{'body_front':'tunic','hat':None}},'provenance':{'sources':[{'asset':self.ref('garment.png'),'license':'Synthetic test pixels; not Roshan art','role':'garment_source','acceptance_scope':'Synthetic format fixture only; no Roshan acceptance'}],'edits':['Synthetic format fixture'],'generator_calls':0}}

    def write(self,name,value):
        (self.root/name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n')

    def ref(self,name):
        return {'path':name,'sha256':hashlib.sha256((self.root/name).read_bytes()).hexdigest()}

    def check(self,skin=None):
        self.write('skin.json',self.skin if skin is None else skin)
        return validate_skin(self.root/'skin.json',self.root/'rig.json',self.root)

    def reject(self,skin):
        with self.assertRaises(InvalidSkin):self.check(skin)

    def test_valid_bindings_do_not_accept_runtime_or_art(self):
        result=self.check()
        self.assertTrue(result['format_and_bindings_pass'])
        self.assertFalse(result['production_accepted'])
        self.assertFalse(result['live_actor_verified'])
        self.assertFalse(result['garment_only_pixels_reviewed'])

    def test_per_outfit_character_script_rejected(self):
        skin=copy.deepcopy(self.skin);skin['character_script']='chef.gd';self.reject(skin)

    def test_changed_rig_pin_rejected(self):
        skin=copy.deepcopy(self.skin);skin['rig']['version']='2';self.reject(skin)

    def test_stale_texture_hash_rejected(self):
        skin=copy.deepcopy(self.skin);skin['attachments'][0]['texture']['sha256']='0'*64;self.reject(skin)

    def test_path_escape_rejected(self):
        skin=copy.deepcopy(self.skin);skin['attachments'][0]['texture']['path']='../garment.png';self.reject(skin)

    def test_uncovered_required_slot_rejected(self):
        skin=copy.deepcopy(self.skin);skin['coverage']['front']['body_front']=None;self.reject(skin)

    def test_unknown_view_rejected(self):
        skin=copy.deepcopy(self.skin);skin['views']=['profile'];self.reject(skin)

    def test_duplicate_attachment_rejected(self):
        skin=copy.deepcopy(self.skin);skin['attachments'].append(copy.deepcopy(skin['attachments'][0]));self.reject(skin)

    def changed_mesh(self,change):
        mesh=copy.deepcopy(self.mesh);change(mesh);self.write('new.json',mesh)
        skin=copy.deepcopy(self.skin);skin['attachments'][0].pop('template_id');skin['attachments'][0]['geometry']=self.ref('new.json');return skin

    def test_unknown_bone_rejected(self):
        self.reject(self.changed_mesh(lambda m:m.update(weights={'InventedBone':[1,1,1]})))

    def test_unnormalized_weights_rejected(self):
        self.reject(self.changed_mesh(lambda m:m.update(weights={'Torso':[1,0.3,1]})))

    def test_bad_triangle_rejected(self):
        self.reject(self.changed_mesh(lambda m:m.update(triangles=[[0,1,99]])))

    def test_nan_coordinate_rejected(self):
        self.reject(self.changed_mesh(lambda m:m['vertices'][0].__setitem__(0,float('nan'))))

    def test_changed_shared_template_rejected(self):
        skin=self.changed_mesh(lambda m:m['vertices'][1].__setitem__(0,14));skin['attachments'][0]['template_id']='tunic';self.reject(skin)

    def test_rgb_texture_rejected(self):
        Image.new('RGB',(16,16)).save(self.root/'rgb.png');skin=copy.deepcopy(self.skin);skin['attachments'][0]['texture']=self.ref('rgb.png');self.reject(skin)

    def test_changed_identity_asset_rejected(self):
        Image.new('RGBA',(16,16),(1,2,3,255)).save(self.root/'identity.png');self.reject(self.skin)

    def test_rigid_hat_uses_shared_socket(self):
        skin=copy.deepcopy(self.skin);skin['attachments'].append({'id':'hat','view':'front','slot':'hat','mode':'rigid','texture':self.ref('garment.png'),'binding':{'socket':'hat','pivot':[8,8],'offset':[0,0],'rotation_deg':0,'scale':1}});skin['coverage']['front']['hat']='hat';self.assertTrue(self.check(skin)['format_and_bindings_pass'])

    def test_recipe_reuses_existing_binding_without_character_code(self):
        from tools.prepare_costume_skin import prepare
        recipe={'skin_id':'recipe_tunic','views':['front'],'attachments':[{'id':'tunic','view':'front','slot':'body_front','texture':'garment.png','template_id':'tunic'}],'coverage':self.skin['coverage'],'sources':[{'path':'garment.png','license':'Synthetic test pixels','role':'garment_source','acceptance_scope':'Synthetic format fixture only; no Roshan acceptance'}],'edits':['Reuse template'],'generator_calls':0}
        skin,result=prepare(recipe,self.root/'rig.json',self.root)
        self.assertEqual(skin['attachments'][0]['geometry'],self.rig['templates']['tunic'])
        self.assertTrue(result['format_and_bindings_pass'])
        self.assertFalse(result['production_accepted'])

    def test_recipe_does_not_guess_missing_weights(self):
        from tools.prepare_costume_skin import prepare
        recipe={'skin_id':'unbound','views':['front'],'attachments':[{'id':'tunic','view':'front','slot':'body_front','texture':'garment.png'}],'coverage':self.skin['coverage'],'sources':[{'path':'garment.png','license':'Synthetic test pixels','role':'garment_source','acceptance_scope':'Synthetic format fixture only; no Roshan acceptance'}],'edits':[],'generator_calls':0}
        with self.assertRaisesRegex(InvalidSkin,'lacks binding'):prepare(recipe,self.root/'rig.json',self.root)

    def test_source_acceptance_scope_cannot_be_dropped(self):
        skin=copy.deepcopy(self.skin);skin['provenance']['sources'][0].pop('acceptance_scope');self.reject(skin)

    def test_outside_texture_uv_rejected(self):
        self.reject(self.changed_mesh(lambda m:m['uv'][1].__setitem__(0,17)))

    def test_two_texture_variants_reuse_one_binding_and_rig(self):
        from tools.prepare_costume_skin import prepare
        recipe={'skin_id':'first','views':['front'],'attachments':[{'id':'tunic','view':'front','slot':'body_front','texture':'garment.png','template_id':'tunic'}],'coverage':self.skin['coverage'],'sources':[{'path':'garment.png','license':'Synthetic test pixels','role':'garment_source','acceptance_scope':'Format test only'}],'edits':['Reuse template'],'generator_calls':0}
        before={name:self.ref(name)['sha256'] for name in ['rig.json','skeleton.json','identity.png','tunic.json']}
        first,_=prepare(recipe,self.root/'rig.json',self.root)
        Image.new('RGBA',(16,16),(20,80,160,255)).save(self.root/'variant.png')
        recipe['skin_id']='second';recipe['attachments'][0]['texture']='variant.png';recipe['sources'][0]['path']='variant.png'
        second,_=prepare(recipe,self.root/'rig.json',self.root)
        self.assertEqual(first['rig'],second['rig'])
        self.assertEqual(first['attachments'][0]['geometry'],second['attachments'][0]['geometry'])
        self.assertNotEqual(first['attachments'][0]['texture'],second['attachments'][0]['texture'])
        self.assertEqual(before,{name:self.ref(name)['sha256'] for name in before})

    def test_documented_cli_prepares_validates_and_refuses_overwrite(self):
        repo=Path(__file__).resolve().parents[2]
        recipe={'skin_id':'cli_tunic','views':['front'],'attachments':[{'id':'tunic','view':'front','slot':'body_front','texture':'garment.png','template_id':'tunic'}],'coverage':self.skin['coverage'],'sources':[{'path':'garment.png','license':'Synthetic test pixels','role':'garment_source','acceptance_scope':'Format test only'}],'edits':['Reuse template'],'generator_calls':0}
        self.write('recipe.json',recipe)
        output=self.root/'package/skin.json';report=self.root/'package/report.json'
        command=[sys.executable,str(repo/'tools/prepare_costume_skin.py'),'--root',str(self.root),'--rig',str(self.root/'rig.json'),'--recipe',str(self.root/'recipe.json'),'--out',str(output)]
        result=subprocess.run(command,capture_output=True,text=True);self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        original=output.read_bytes()
        result=subprocess.run([sys.executable,str(repo/'tools/validate_costume_skin.py'),'--root',str(self.root),'--rig',str(self.root/'rig.json'),'--skin',str(output),'--report',str(report)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertTrue(json.loads(report.read_text())['format_and_bindings_pass'])
        result=subprocess.run(command,capture_output=True,text=True);self.assertNotEqual(result.returncode,0)
        self.assertEqual(original,output.read_bytes())


if __name__=='__main__':unittest.main()

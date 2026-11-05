"""Register authored fin keys in Aseprite and derive contour/UV analysis data.

No Python painting. Registered source pixels are copied unchanged by Aseprite.
Signed distances and nearest-source coordinates are numeric shader data, not art.
"""
import hashlib
import json
import math
from pathlib import Path
import subprocess

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]


def write(path, data):
    path.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8', newline='\n')


def ref(path):
    return {'path': path.relative_to(REPO).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    spec = json.loads((ROOT/'rig/cut_spec.json').read_text())
    parts = spec['parts'] if isinstance(spec, dict) else spec
    byname = {item['name']: item for item in parts}
    lua = ['local master = Sprite(512,512,ColorMode.RGB)', 'master.layers[1].name="Shared fin view keys"']
    poses = [('fin_broad', [1463,536]), ('fin_edge', [1472,723]), ('fin_cup', [1440,870])]
    registrations = []
    for index, (name, original_pivot) in enumerate(poses):
        item = byname['base_'+name]
        pivot = [original_pivot[0]-item['box'][0], original_pivot[1]-item['box'][1]]
        offset = [400-pivot[0], 256-pivot[1]]
        source = ROOT/'textures/anatomy'/(name+'.png')
        output = ROOT/'textures/anatomy'/(name+'_registered.png')
        lua += ['do', 'local source = Image{fromFile='+json.dumps(source.as_posix())+'}',
                'local image = Image(512,512,ColorMode.RGB)', f'image:drawImage(source,Point({offset[0]},{offset[1]}))',
                'image:saveAs('+json.dumps(output.as_posix())+')',
                '' if index == 0 else 'master:newEmptyFrame()',
                f'master:newCel(master.layers[1],{index+1},image,Point(0,0))',
                f'local tag = master:newTag({index+1},{index+1})', 'tag.name='+json.dumps(name), 'end']
        registrations.append({'id': name, 'source': ref(source), 'output': output, 'offset': offset})
    lua += ['master:saveAs('+json.dumps((ROOT/'masters/shared_fin_keys.aseprite').as_posix())+')', 'master:close()', 'print("FIN_KEYS_REGISTERED_NATIVE 3")']
    path = ROOT/'tools/register_fin.lua'
    path.write_text('\n'.join(lua)+'\n', encoding='utf-8', newline='\n')
    result = subprocess.run(['C:/Program Files/Aseprite/Aseprite.exe', '-b', '--script', str(path)], capture_output=True, timeout=60)
    (ROOT/'evidence/fin_registration.log').write_bytes(result.stdout+result.stderr)
    assert result.returncode == 0, result.stderr
    anatomy = json.loads((ROOT/'rig/anatomy.json').read_text())
    buffers = {}
    angle = math.atan2(-26,-115)-math.pi
    matrix = .52*np.array([[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]])
    offset = np.array([137,550])-matrix@np.array([400,256])
    for entry in registrations:
        name, output = entry['id'], entry['output']
        original = np.asarray(Image.open(REPO/entry['source']['path']).convert('RGBA'))
        pixels = np.asarray(Image.open(output).convert('RGBA'))
        x,y = entry['offset'];assert np.array_equal(original, pixels[y:y+len(original),x:x+original.shape[1]])
        alpha = pixels[:,:,3] >= 128
        outside = ndimage.distance_transform_edt(~alpha)
        # Extend painted interior colours into a changing contour, rather than
        # stretching the old key's dark boundary line across the whole fin.
        interior = ndimage.binary_erosion(alpha, iterations=5)
        assert np.any(interior)
        _, nearest = ndimage.distance_transform_edt(~interior, return_indices=True)
        signed = (outside-ndimage.distance_transform_edt(alpha)).astype('<f4')
        uv = np.stack([(nearest[1]+.5)/512, (nearest[0]+.5)/512], axis=2).astype('<f4')
        sdf_path = ROOT/'rig'/(name+'_sdf.f32');sdf_path.write_bytes(signed.tobytes())
        uv_path = ROOT/'rig'/(name+'_nearest_uv.f32');uv_path.write_bytes(uv.tobytes())
        buffers[name] = {'distance': ref(sdf_path), 'nearest_uv': ref(uv_path)}
        vertices = np.array([[0,0],[512,0],[512,512],[0,512]])
        geometry = {'format':'roshan.attachment-mesh/1', 'space':'canonical_canvas_px', 'vertices': (vertices@matrix.T+offset).tolist(),
                    'uv': vertices.tolist(), 'triangles': [[0,1,2],[0,2,3]], 'weights': {'Fin':[1.,1.,1.,1.]}}
        geom_path = ROOT/'geometry'/('anatomy_'+name+'.json');write(geom_path,geometry)
        part = next(p for p in anatomy['parts'] if p['id']==name)
        part.update(texture=ref(output),geometry=ref(geom_path))
        entry['output'] = ref(output)
    anatomy['fin_interpolation'] = {'format':'roshan.fin-view-fields/1', 'canvas':[512,512], 'pivot':[400,256], 'buffers':buffers,
        'method':'One common fin material interpolates signed contours and source-colour coordinates between three authored poses. This is declared 2D pose interpolation; geometric skin strain does not certify its appearance.'}
    write(ROOT/'rig/anatomy.json',anatomy)
    rig = json.loads((ROOT/'rig/rig_binding.json').read_text())
    # v1 identity asset references are passive PNG/JSON assets. Renderer code
    # is pinned by the native run/packet manifests, not smuggled into a skin
    # data contract. The anatomy JSON pins numeric fields; build() checks them.
    identity = [ref(ROOT/'rig/anatomy.json')]
    for p in anatomy['parts']:identity += [p['texture'],p['geometry']]
    rig['identity_assets'] = list({x['path']:x for x in identity}.values())
    write(ROOT/'rig/rig_binding.json',rig)
    digest = hashlib.sha256((ROOT/'rig/rig_binding.json').read_bytes()).hexdigest()
    for name in ['ballet','magician']:
        path=ROOT/'skins'/(name+'.json');skin=json.loads(path.read_text());skin['rig']['contract_sha256']=digest;write(path,skin)
    write(ROOT/'evidence/fin_preparation.json',{'pass':True,'native_registered_pixels_exact':True,'poses':registrations,
        'interpolation_scope':'Common anatomical fin only. No garment shader, per-costume actor, extra fin node or image generation. UV/contour interpolation requires exact visual review separately from LBS strain.'})
    print('FIN_FIELDS_PREPARED 3',flush=True)


if __name__ == '__main__':main()

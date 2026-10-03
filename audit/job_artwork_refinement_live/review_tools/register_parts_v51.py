"""Bounded, literal-byte, fail-closed loading of the known job-art register."""
from pathlib import Path
import hashlib,json,re
MAX_JSON_BYTES=4*1024*1024
MAX_PARTS=12
PART_NAME=re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]*\.json\Z')
def _read(path):
    if path.stat().st_size>MAX_JSON_BYTES:raise ValueError('Register JSON exceeds the existing 4MiB ceiling')
    raw=path.read_bytes()
    if len(raw)>MAX_JSON_BYTES:raise ValueError('Register JSON exceeds the existing 4MiB ceiling')
    return raw,json.loads(raw.decode('utf-8-sig'))
def load_register(directory):
    directory=Path(directory).resolve();raw,root=_read(directory/'ALL_ITEMS.json')
    if not isinstance(root,dict) or not isinstance(root.get('items'),list):raise ValueError('Invalid root register')
    items=list(root['items']);parts=root.get('item_shards',[])
    if not isinstance(parts,list) or len(parts)>MAX_PARTS:raise ValueError('Invalid register part list')
    seen_paths=set()
    for descriptor in parts:
        name=descriptor.get('path')
        if not isinstance(name,str) or not PART_NAME.fullmatch(name) or name=='ALL_ITEMS.json' or name in seen_paths:raise ValueError('Unsafe or repeated register part path')
        seen_paths.add(name);path=(directory/name).resolve()
        if not path.is_relative_to(directory):raise ValueError('Register part escapes its directory')
        size=descriptor.get('bytes');count=descriptor.get('items');expected=descriptor.get('sha256')
        if type(size) is not int or not 0<size<=MAX_JSON_BYTES or type(count) is not int or not 0<count<=100000 or not isinstance(expected,str) or not re.fullmatch('[0-9a-f]{64}',expected):raise ValueError('Invalid register part descriptor')
        part_raw,part=_read(path)
        if len(part_raw)!=size or hashlib.sha256(part_raw).hexdigest()!=expected:raise ValueError('Register part byte/hash mismatch')
        if not isinstance(part,dict) or not isinstance(part.get('items'),list) or len(part['items'])!=count:raise ValueError('Register part item-count mismatch')
        items.extend(part['items'])
    ids=[]
    for item in items:
        if not isinstance(item,dict) or not isinstance(item.get('id'),str) or not item['id'] or not isinstance(item.get('path'),str):raise ValueError('Invalid register item identity/path')
        ids.append(item['id'])
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate register item ID')
    if root.get('counts',{}).get('registered_items')!=len(items):raise ValueError('Assembled register count mismatch')
    root['items']=items
    return root

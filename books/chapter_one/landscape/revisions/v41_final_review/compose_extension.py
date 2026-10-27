"""Reuse selected generated edge repair; restore native source world and bounded joins."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
V=Path(__file__).resolve().parent
recipe=json.loads((V/'world_composition_provenance.json').read_text('utf8'))['selection']
page=Image.open(V/recipe['generated_source']).convert('RGB').resize(tuple(recipe['canvas']),Image.Resampling.LANCZOS)
world=Image.open(V/'art/sky_lagoon_full_world.png').convert('RGB')
alpha=np.ones(world.height)
t,b=recipe['source_alpha_top_rows'],recipe['source_alpha_bottom_rows']
alpha[:t]=np.sin(np.linspace(0,np.pi/2,t))**2
alpha[-b:]=np.cos(np.linspace(0,np.pi/2,b))**2
mask=Image.fromarray(np.repeat(np.round(alpha[:,None]*255).astype('uint8'),world.width,axis=1))
page.paste(world,tuple(recipe['world_offset']),mask)
out=V/recipe['output'];page.save(out)
assert hashlib.sha256(out.read_bytes()).hexdigest()==recipe['sha256']
print('Selected extensions and native geography replay exactly:',out)

from pathlib import Path
import json,torch
from safetensors.torch import load_file
p=Path(__file__).resolve().parents[1]/'results/ltx23_retake_lowmem'
a=load_file(str(p/'encoded_source.latent'),device='cpu')['latent_tensor'];b=load_file(str(p/'retake.latent'),device='cpu')['latent_tensor'];assert a.shape==b.shape
rows=[]
for i in range(a.shape[2]):
 delta=(b[:,:,i].float()-a[:,:,i].float()).abs();rows.append({'temporal_latent_index':i,'expected_mask':0 if i in [0,a.shape[2]-1] else 1,'max_absolute_difference':float(delta.max()),'mean_absolute_difference':float(delta.mean()),'exact_tensor_equal':bool(torch.equal(a[:,:,i],b[:,:,i]))})
result={'source_shape':list(a.shape),'retake_shape':list(b.shape),'blocks':rows,'frozen_boundary_latents_preserved_within_1e_5':all(rows[i]['max_absolute_difference']<=1e-5 for i in [0,len(rows)-1]),'interior_latents_changed':all(rows[i]['max_absolute_difference']>1e-5 for i in range(1,len(rows)-1)),'decoded_pixels_byte_preserved_by_mask':False,'note':'Mask acts on temporal latent blocks; full VAE reconstruction can change decoded pixels. Review splice separately preserves original PNG bytes outside 41-63.'}
assert result['frozen_boundary_latents_preserved_within_1e_5'] and result['interior_latents_changed'],result
result['status']='PASS';(p/'latent_mask_verification.json').write_text(json.dumps(result,indent=2)+'\n');print('LATENT_TEMPORAL_MASK_PASS',list(a.shape))

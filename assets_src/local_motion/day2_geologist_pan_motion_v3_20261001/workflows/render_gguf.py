import sys
sys.path.insert(0,'H:/MermaidReefTools/LocalVideo')
import render_local
render_local.PRESETS['quick'].update(width=896,height=512,frames=41,steps=24,weight_dtype='GGUF_Q4_K_S')
base_graph=render_local.api_graph
def graph(*args,**kwargs):
 g=base_graph(*args,**kwargs)
 g['1']={'class_type':'UnetLoaderGGUFAdvanced','inputs':{'unet_name':'Wan2.2-TI2V-5B-Q4_K_S.gguf','dequant_dtype':'bfloat16','patch_dtype':'bfloat16','patch_on_device':True}}
 g['2']={'class_type':'CLIPLoaderGGUF','inputs':{'clip_name':'umt5-xxl-encoder-Q4_K_S.gguf','type':'wan'}}
 g['10']['inputs'].update(tile_size=256,overlap=64,temporal_size=4096,temporal_overlap=8)
 return {'0':{'class_type':'SaveLatent','inputs':{'samples':['9',0],'filename_prefix':g['11']['inputs']['filename_prefix']}},**g}
render_local.api_graph=graph
render_local.main()

"""Aseprite master: ONE layer, one whole cel per frame, 24 fps timing, beat tags; reader round-trip check."""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
import aseprite_io
N=41
fr=[np.array(Image.open(P('frames','native','%04d.png'%f)).convert('RGBA')) for f in range(N)]
DUR=[round((i+1)*1000/24)-round(i*1000/24) for i in range(N)]
TAGS=[(0,3,'rest'),(3,7,'rise_to_shoulder'),(7,17,'rise_overhead'),(17,27,'wave_lowering'),(27,36,'lower_to_rest'),(36,40,'rest')]
aseprite_io.write(P('wave_master.aseprite'),256,256,[('roshan_wave',True)],[{'roshan_wave':a} for a in fr],DUR,TAGS)
m=aseprite_io.read(P('wave_master.aseprite'))
assert len(m['layers'])==1 and all(np.array_equal(m['frames'][f]['roshan_wave'],fr[f]) for f in range(N))
print('master ok: 1 layer, %d frames, %d ms'%(N,sum(m['durations'])))

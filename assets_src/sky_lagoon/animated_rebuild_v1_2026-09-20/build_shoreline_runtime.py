from pathlib import Path
from PIL import Image
import numpy as np,json,shutil
W=Path(__file__).resolve().parents[3];P=Path(__file__).resolve().parent/'water';D=W/'assets/sprites/sky_lagoon/animated_v1'
for name,width in [('arrival',256),('castle',512)]:
 atlas=Image.open(P/f'{name}-shore-atlas.png').convert('RGBA');assert atlas.size==(width*4,512)
 for n in range(8):
  frame=np.array(atlas.crop(((n%4)*width,(n//4)*256,(n%4+1)*width,(n//4+1)*256)));source=np.array(Image.open(P/f'{name}-shore-{n:02}.png').convert('RGBA'));assert np.array_equal(frame[:,:,3],source[:,:,3]);assert np.array_equal(frame[source[:,:,3]>0],source[source[:,:,3]>0])
 shutil.copyfile(P/f'{name}-shore-atlas.png',D/f'water_{name}_shore.png')
print('SHORE_PACKAGE|8 cel exports exact; dimensions within texture budget|PASS')

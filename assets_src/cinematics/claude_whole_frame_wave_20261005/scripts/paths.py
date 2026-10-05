"""Paths for the Roshan whole-frame wave study (revision 2). Override with env vars when needed."""
import os
HERE=os.path.dirname(os.path.abspath(__file__))
PKT=os.environ.get('WAVE2D_PKT',os.path.dirname(HERE))                     # packet directory (committed outputs)
REPO=os.environ.get('WAVE2D_REPO',os.path.abspath(os.path.join(PKT,'..','..','..')))
WORK=os.environ.get('WAVE2D_WORK',os.path.join(os.environ.get('TMPDIR','/tmp'),'wave_whole_work'))  # intermediates, never committed
ATLAS=os.path.join(REPO,'assets','characters','roshan_25d','roshan_gesture_a.png')
ATLAS_SHA256='e70139b23c9f84c0e8f0c1063145ca4e9e67ee32c57aa544bc08193326af9b9d'
def W(*p): os.makedirs(WORK,exist_ok=True); return os.path.join(WORK,*p)
def P(*p):
    d=os.path.join(PKT,*p); os.makedirs(os.path.dirname(d),exist_ok=True); return d

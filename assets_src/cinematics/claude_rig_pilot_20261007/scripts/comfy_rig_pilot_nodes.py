"""ComfyUI loader for the rig-pilot run-2 guides (study only, no vendor source edits).

Install: copy this file into ComfyUI/custom_nodes/ and restart the server. It reads
<ComfyUI input>/rig_pilot/guide_{quarter,half}/0000-0040.png, which scripts/run_take.py copies and
hash-checks. The Union study nodes (UnionModelProof, UnionOutputProof) and the existing study
receipt nodes are reused unchanged.
"""
from pathlib import Path
import numpy as np
import torch
from PIL import Image
import folder_paths


class RigPilotGuideBatch:
    @classmethod
    def INPUT_TYPES(cls):
        return {'required': {'lane': (['quarter', 'half'],), 'frames': ('INT', {'default': 41, 'min': 9, 'max': 41, 'step': 8})}}

    RETURN_TYPES = ('IMAGE',)
    FUNCTION = 'load'
    CATEGORY = 'Mermaid/study'

    def load(self, lane, frames):
        root = Path(folder_paths.get_input_directory()) / 'rig_pilot' / f'guide_{lane}'
        a = torch.stack([torch.from_numpy(np.array(Image.open(root / f'{i:04d}.png').convert('RGB'), dtype=np.float32) / 255)
                         for i in range(frames)])
        assert tuple(a.shape) == (frames, 224 if lane == 'quarter' else 448, 160 if lane == 'quarter' else 320, 3)
        return (a,)


NODE_CLASS_MAPPINGS = {'RigPilotGuideBatch': RigPilotGuideBatch}

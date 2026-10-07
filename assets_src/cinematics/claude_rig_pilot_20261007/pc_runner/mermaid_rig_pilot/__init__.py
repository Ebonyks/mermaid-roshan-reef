"""ComfyUI loader for Claude rig-pilot guide sets (study only, no vendor source edits).

Installed as ComfyUI/custom_nodes/mermaid_rig_pilot/ and whitelisted by start_rig_pilot_runner.bat.
Reads <ComfyUI input>/rig_pilot/<guide_set>/guide_<lane>/0000-0040.png. The rig-pilot runner checks
every input file's SHA-256 against the job before it submits a graph. The Union study proofs
(UnionModelProof, UnionOutputProof) and the study receipt nodes are reused unchanged.
"""
import re
from pathlib import Path

import numpy as np
import torch
from PIL import Image

import folder_paths

SIZES = {'quarter': (224, 160), 'half': (448, 320), 'full': (896, 640)}


class RigPilotGuideBatch:
    @classmethod
    def INPUT_TYPES(cls):
        return {'required': {'guide_set': ('STRING', {'default': 'run2'}),
                             'lane': (['quarter', 'half', 'full'],),
                             'frames': ('INT', {'default': 41, 'min': 9, 'max': 41, 'step': 8})}}

    RETURN_TYPES = ('IMAGE',)
    FUNCTION = 'load'
    CATEGORY = 'Mermaid/study'

    def load(self, guide_set, lane, frames):
        assert re.fullmatch(r'[A-Za-z0-9_-]{1,64}', guide_set), 'guide_set must be a plain folder name'
        root = Path(folder_paths.get_input_directory()) / 'rig_pilot' / guide_set / f'guide_{lane}'
        a = torch.stack([torch.from_numpy(np.array(Image.open(root / f'{i:04d}.png').convert('RGB'), dtype=np.float32) / 255)
                         for i in range(frames)])
        h, w = SIZES[lane]
        assert tuple(a.shape) == (frames, h, w, 3), (tuple(a.shape), lane)
        return (a,)


NODE_CLASS_MAPPINGS = {'RigPilotGuideBatch': RigPilotGuideBatch}

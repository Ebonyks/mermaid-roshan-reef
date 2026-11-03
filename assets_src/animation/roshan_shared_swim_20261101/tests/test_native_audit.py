"""Negative controls for the contour/visibility checks that caught real issues."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('native_audit',ROOT/'tools/audit_native_geometry.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)


class NativeAuditControls(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=audit.REPO/'tmp')
        self.path=Path(self.temp.name)

    def tearDown(self):self.temp.cleanup()

    def fixture(self, detached=False, clipped=False):
        image=Image.new('RGBA',(64,64))
        draw=ImageDraw.Draw(image)
        draw.ellipse((10,10,35,35),fill=(255,128,20,255))
        if detached:draw.ellipse((45,45,58,58),fill=(255,128,20,255))
        if clipped:draw.rectangle((0,12,15,24),fill=(255,128,20,255))
        path=self.path/'synthetic_control.png';image.save(path)
        return path

    def test_clipping_and_detachment_are_observable(self):
        clean=audit.alpha_observation(self.fixture())
        self.assertEqual(len(clean['major_components']),1)
        self.assertEqual(clean['edge_alpha_pixels'],0)
        clipped=audit.alpha_observation(self.fixture(clipped=True))
        self.assertGreater(clipped['edge_alpha_pixels'],0)
        detached=audit.alpha_observation(self.fixture(detached=True))
        self.assertEqual(len(detached['major_components']),2)

    def material(self):
        # Tiny painted strip away from sparse barycentric probe locations.
        image=Image.new('RGBA',(64,64));ImageDraw.Draw(image).rectangle((20,5,22,7),fill=(255,0,0,255))
        texture=self.path/'thin_alpha_control.png';image.save(texture)
        geometry=self.path/'control.json';geometry.write_text(json.dumps({'vertices':[[0,0],[64,0],[64,64]],'uv':[[0,0],[64,0],[64,64]],'triangles':[[0,1,2]],'weights':{'Fin':[1,1,1]}}))
        def ref(path):return {'path':path.relative_to(audit.REPO).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
        return audit.material(ref(texture),ref(geometry))

    def test_every_visible_texel_includes_thin_material_triangle(self):
        self.assertEqual(self.material()['visible_triangles'],1)

    def test_flip_and_overstretch_controls_fail_unchanged_floors(self):
        part=self.material();rest={'Fin':np.eye(3)}
        low,high,flips=audit.strain(part,{'Fin':[-1,0,0,1,0,0]},rest)
        self.assertEqual(flips,1)
        low,high,flips=audit.strain(part,{'Fin':[1.3,0,0,1,0,0]},rest)
        self.assertGreater(high,1.2)
        self.assertEqual(flips,0)


if __name__=='__main__':unittest.main()

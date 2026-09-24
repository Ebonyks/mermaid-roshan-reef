"""Physical Opera props: independent output-pixel ownership and identity checks."""
import json
import unittest
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assets_src/concepts/opera_four_floors_2026-09-06'
ART = ROOT / 'assets/flats/castle/opera_house_four_floors'


class PhysicalOperaLayers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((SOURCE / 'physical_parts_manifest.json').read_text())
        cls.source = np.array(Image.open(SOURCE / 'venue_native_v7.png').convert('RGBA'))

    def test_part_metadata_is_in_every_export_preset(self):
        import configparser
        cfg = configparser.ConfigParser(interpolation=None)
        cfg.read(ROOT / 'export_presets.cfg', encoding='utf-8')
        for section in cfg.sections():
            if section.startswith('preset.') and not section.endswith('.options'):
                included = cfg[section]['include_filter'].strip('"').split(',')
                self.assertIn('assets/flats/castle/opera_house_four_floors/physical/parts.json', included)

    def test_rest_has_one_owner_and_exact_original_pixels(self):
        tiles = [np.array(Image.open(ART / f'venue_{i}.png').convert('RGBA')) for i in range(2)]
        rest = np.concatenate(tiles, axis=1)
        owners = (rest[:, :, 3] > 0).astype('uint8')
        for body, bounds in self.manifest['body_bounds'].items():
            x0, y0, x1, y1 = bounds
            layer = np.array(Image.open(ART / 'physical' / f'{body}_0.png').convert('RGBA'))
            opaque = layer[:, :, 3] > 0
            owners[y0:y1, x0:x1] += opaque
            rest[y0:y1, x0:x1][opaque] = layer[opaque]
        self.assertTrue(np.all(owners == 1), 'missing or doubly painted original pixels')
        np.testing.assert_array_equal(rest, self.source)

    def test_moving_pieces_keep_source_rgb_and_scale(self):
        ownership = np.zeros(self.source.shape[:2], dtype='uint8')
        for name, spec in self.manifest['parts'].items():
            x0, y0, x1, y1 = spec['native_bounds']
            part = np.array(Image.open(ART / 'physical' / f'{name}.png').convert('RGBA'))
            np.testing.assert_array_equal(part[:, :, :3], self.source[y0:y1, x0:x1, :3])
            ownership[y0:y1, x0:x1] += (part[:, :, 3] > 0)
            self.assertAlmostEqual(spec['source_rect'][2], (x1-x0)*1280/1672)
            self.assertAlmostEqual(spec['source_rect'][3], (y1-y0)*720/941)
        self.assertLessEqual(ownership.max(), 1, 'two physical pieces share source pixels')

    def test_petals_are_parts_of_the_held_flower(self):
        flower = np.array(Image.open(ART / 'physical/flower.png').convert('RGBA'))
        counts = np.zeros(flower.shape[:2], dtype='uint16')
        for name in ['flower_core'] + [f'flower_petal_{i}' for i in range(6)]:
            piece = np.array(Image.open(ART / 'physical' / f'{name}.png').convert('RGBA'))
            np.testing.assert_array_equal(piece[:, :, :3], flower[:, :, :3])
            counts += piece[:, :, 3]
        np.testing.assert_array_equal(counts, flower[:, :, 3])

    def test_removal_changes_only_the_actual_piece_footprint(self):
        for name, spec in self.manifest['parts'].items():
            body = spec['body']
            x0, y0, x1, y1 = self.manifest['body_bounds'][body]
            original = np.array(Image.open(ART / 'physical' / f'{body}_0.png').convert('RGBA'))
            removed = np.array(Image.open(ART / 'physical' / f'{body}_{spec["bit"]}.png').convert('RGBA'))
            mask = np.zeros(original.shape[:2], dtype=bool)
            px0, py0, px1, py1 = spec['native_bounds']
            part = np.array(Image.open(ART / 'physical' / f'{name}.png').convert('RGBA'))
            mask[py0-y0:py1-y0, px0-x0:px1-x0] = part[:, :, 3] > 0
            np.testing.assert_array_equal(removed[~mask], original[~mask])
            changed = np.any(removed[:, :, :3] != original[:, :, :3], axis=2)
            self.assertGreater(changed[mask].mean(), .9, 'picked object remains painted at source')


if __name__ == '__main__':
    unittest.main()

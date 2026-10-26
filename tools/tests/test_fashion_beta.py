import unittest
import numpy as np
from tools.audit_fashion_beta import check_layer


class BetaLayerControls(unittest.TestCase):
    def fixture(self):
        source = np.zeros((8, 8, 4), dtype=np.uint8)
        source[1:7, 1:7] = [40, 30, 180, 255]
        layer = np.zeros_like(source)
        layer[2:6, 2:6] = [180, 50, 190, 255]
        return source, layer, {"path":"control", "slot":"body", "fit":[[2,2,6,6]]}, {"cell":[8,8]}

    def test_valid_registered_layer(self):
        self.assertEqual(check_layer(*self.fixture()), 1)

    def test_real_outside_slot_corruption_is_rejected(self):
        args = self.fixture()
        args[1][0, 0] = [255, 255, 255, 255]
        with self.assertRaisesRegex(AssertionError, "outside slot"):
            check_layer(*args)

    def test_hand_source_contour_and_skin_changes_are_rejected(self):
        for corruption in ("hand", "contour", "skin"):
            source, layer, row, spec = self.fixture()
            if corruption == "hand": spec["protected_boxes"] = [[3,3,4,4]]
            if corruption == "contour": source[3, 3, 3] = 128
            if corruption == "skin": source[3, 3] = [230, 170, 80, 255]
            with self.assertRaises(AssertionError):
                check_layer(source, layer, row, spec)

    def test_empty_authored_cell_is_rejected(self):
        source, layer, row, spec = self.fixture()
        layer[:] = 0
        with self.assertRaisesRegex(AssertionError, "empty fitted cell"):
            check_layer(source, layer, row, spec)

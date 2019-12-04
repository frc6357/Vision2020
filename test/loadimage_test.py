#!/usr/local/bin/python3

# Runs two tests to ensure cv2.imread inside loadimage() has a valid filename to work with
# and checks that invald filenames are handled correctly

import unittest
from src.loadimage import loadimage
import sys

class TestLoadImage(unittest.TestCase):
    def test_load(self):
        test_file = "../CargoSideStraightDark36in.jpg"
        image = loadimage(test_file)
        self.assertIsNotNone(image, msg="File %s not found"%test_file)
        h, w, d = image.shape
        self.assertEqual(h, 240)
        self.assertEqual(w, 320)
        self.assertEqual(d, 3)

class TestBadImage(unittest.TestCase):
    def test_load(self):
        test_file = "../not a real file.jpg"
        image = loadimage(test_file)
        self.assertIsNone(image, msg="File %s found unexpectedly oh no"%test_file)


if __name__ == '__main__':
    unittest.main()

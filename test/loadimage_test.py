import unittest
from src.loadimage import loadimage
import os

class TestLoadImage(unittest.TestCase):
    def test_load(self):
        test_file = "../CargoSideStraightDark36in.jpg"
        h, w, d = loadimage(test_file).shape
        self.assertEqual(h, 240)
        self.assertEqual(w, 320)
        self.assertEqual(d, 3)



if __name__ == '__main__':
    unittest.main()

import unittest

from a9x_webstatistics.module1 import Number


class TestSimple(unittest.TestCase):

    def test_add(self):
        self.assertEqual((Number(7) + Number(6)).value, 13)


if __name__ == '__main__':
    unittest.main()

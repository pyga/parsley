from calc import Calc
import unittest

class CalcTest(unittest.TestCase):

    def test_calc(self):
        self.assertEqual(Calc("2 * (3 + 4)").expr(), 14)

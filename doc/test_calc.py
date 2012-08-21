from calc import Calc
import unittest

class CalcTest(unittest.TestCase):

    def test_calc(self):
        #self.assertEqual(Calc("2 * (3 + 4 * 5)").expr(), 46)
        #self.assertEqual(Calc("2 *( 3 + 40 /   5)").expr(), 22)
        import ometa.runtime
        ometa.runtime._go = True
        self.assertEqual(Calc("2 + +(* 3 + 40 /   5)").expr(), 22)

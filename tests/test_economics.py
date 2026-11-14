import unittest
from pilot.economics import calculate
class EconomicsTests(unittest.TestCase):
    def test_instructional_answers(self):
        self.assertEqual(calculate()['released_hours_month'],300)
        self.assertEqual(calculate()['year_one_net'],21600)
        self.assertAlmostEqual(calculate()['roi'],.4)
        self.assertAlmostEqual(calculate(.25)['roi'],-.3)
        self.assertAlmostEqual(calculate(.75)['roi'],1.1)
        self.assertAlmostEqual(calculate(realization=.4)['roi'],-.2)
        self.assertAlmostEqual(calculate()['simple_payback_months'],18000/3300)
    def test_no_positive_payback_without_operating_surplus(self):
        self.assertIsNone(calculate(coverage=0)['simple_payback_months'])

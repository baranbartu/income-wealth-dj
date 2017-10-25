from django.test import TestCase

from incomewealth.app.helpers import (calc_year_based_inequality_factors,
                                      calc_year_based_saving_capacities)


class UtilTest(TestCase):

    def setUp(self):
        self.mock_data_inequality = [
            {'year': 2010, 'foo_bottom50': 0.1, 'foo_top10': 0.2}
        ]

        self.mock_data_saving = [
            {'year': 2010, 'income_top10': 0.1},
            {'year': 2011, 'income_top10': 0.2},
            {'year': 2012, 'income_top10': 0.3},
        ]

    def test_inequality_factors(self):
        factor_mapping = None
        for d in calc_year_based_inequality_factors(
                self.mock_data_inequality, 'foo'):
            factor_mapping = d
            break

        self.assertTrue(factor_mapping is not None)
        self.assertEqual(factor_mapping['factor'], (0.1 / 50) / (0.2 / 10))

    def test_saving_capacities(self):
        saving_capacity_mapping = None
        for d in calc_year_based_saving_capacities(
                self.mock_data_saving, 'top', 10):
            saving_capacity_mapping = d
            break

        self.assertTrue(saving_capacity_mapping is not None)
        should_be = ((0.2 / 10) - (0.1 / 10)) / (0.1 / 10)
        self.assertEqual(saving_capacity_mapping['savingcapacity'], should_be)

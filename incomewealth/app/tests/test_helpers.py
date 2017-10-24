from django.test import TestCase

from incomewealth.app.helpers import calc_year_based_inequality_factors


class UtilTest(TestCase):

    def setUp(self):
        self.mock_data = [{'year': 2010, 'foo': 0.1, 'bar': 0.2}]

    def test_inequality_factors(self):
        factor_mapping = None
        for d in calc_year_based_inequality_factors(self.mock_data,
                                                    ('foo', 'bar')):
            factor_mapping = d
            break

        self.assertTrue(factor_mapping is not None)
        self.assertEqual(factor_mapping['factor'], 0.5)

import csv

from django.conf import settings
from django.test import TestCase

from incomewealth import utils
from incomewealth.app.models import IncomeWealth


class UtilTest(TestCase):

    def setUp(self):
        correct_csv_file_path = (
            settings.INIT_CSV_DUMP_FILE_REL_PATH)
        wrong_csv_file_path = settings.WRONG_CSV_FILE_REL_PATH

        self.correct_file = open(correct_csv_file_path)
        self.wrong_file = open(wrong_csv_file_path)

        IncomeWealth.objects.all().delete()

    def test_read_csv_success(self):
        seq = utils.read_csv(self.correct_file)
        data = list(seq)
        # assert at least one row exists
        self.assertTrue(len(data) >= 1)
        # assert each row has same column size
        self.assertTrue(
            next(iter(set([len(d) for d in data]))) == len(data[0]))

    def test_read_csv_error(self):
        data = None
        try:
            data = list(utils.read_csv(self.wrong_file))
        except Exception, e:
            self.assertTrue(isinstance(e, csv.Error))
        self.assertTrue(data is None)

    def test_update_or_create_income_and_wealth(self):
        data = list(utils.read_csv(self.correct_file))
        self.assertTrue(len(data) > 0)
        utils.update_or_create_income_and_wealth(data)
        obj_count_on_db = IncomeWealth.objects.count()
        # should be len(data) - 1, because first raw contains column names:
        self.assertTrue(obj_count_on_db == len(data) - 1)

    def tearDown(self):
        self.correct_file.close()
        self.wrong_file.close()

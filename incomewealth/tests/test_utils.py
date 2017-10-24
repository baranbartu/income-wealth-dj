import csv
import random

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

        # truncate all the records from test db
        IncomeWealth.objects.all().delete()

        # make sample list of dictionaries
        self.list_of_objects = [
            {'year': 1990, 'income': 0.32, 'wealth': 0.44},
            {'year': 1991, 'income': 0.27, 'wealth': 0.49},
        ]

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
        # should be len(data) - 1, because first raw contains column names
        self.assertTrue(obj_count_on_db == len(data) - 1)

    def test_flattenize_list_of_objects(self):
        flattened = utils.flattenize_list_of_objects(self.list_of_objects)
        random_obj = random.choice(self.list_of_objects)
        self.assertTrue(len(flattened) == len(random_obj))

    def tearDown(self):
        self.correct_file.close()
        self.wrong_file.close()

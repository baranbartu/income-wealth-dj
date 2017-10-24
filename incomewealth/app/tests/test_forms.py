from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from incomewealth.app.forms import CsvFileForm


class FormTest(TestCase):

    def setUp(self):
        correct_csv_file_path = (
            settings.INIT_CSV_DUMP_FILE_REL_PATH)
        wrong_csv_file_path = settings.WRONG_CSV_FILE_REL_PATH

        self.correct_file = open(correct_csv_file_path)
        self.wrong_file = open(wrong_csv_file_path)

    def test_correct_csv_validation(self):
        form = CsvFileForm({}, {'csv_file': SimpleUploadedFile(
            self.correct_file.name,
            self.correct_file.read(),
            content_type='text/csv')})
        self.assertTrue(form.is_valid())

    def test_wrong_csv_validation(self):
        form = CsvFileForm({}, {'csv_file': SimpleUploadedFile(
            self.wrong_file.name,
            self.wrong_file.read(),
            content_type='text/csv')})
        self.assertTrue(not form.is_valid())

    def tearDown(self):
        self.correct_file.close()
        self.wrong_file.close()

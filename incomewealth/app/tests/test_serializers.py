from django.test import TestCase
from django.core.exceptions import ValidationError

from incomewealth.app.serializers import serialize_get_request


class FormTest(TestCase):

    def setUp(self):
        self.correct_request = {'init': 2010, 'end': 2012}
        self.wrong_request1 = {'init': 'mahmut', 'end': 2012}
        self.wrong_request2 = {'end': 2012}

    def test_serialize_get_request(self):
        query = serialize_get_request(self.correct_request)
        self.assertEqual(query.init, self.correct_request['init'])

        self.assertRaises(ValidationError, lambda: serialize_get_request(
            self.wrong_request1))

        self.assertRaises(ValidationError, lambda: serialize_get_request(
            self.wrong_request2))

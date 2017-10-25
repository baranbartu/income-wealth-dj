from django.test import TestCase
from django.core.exceptions import ValidationError

from incomewealth.app.serializers import (serialize_get_request,
                                          serialize_saving_capacity_request)


class SerializerTest(TestCase):

    def setUp(self):
        self.correct_request = {'init': 2010, 'end': 2012}
        self.wrong_request1 = {'init': 'mahmut', 'end': 2012}
        self.wrong_request2 = {'end': 2012}

        # terrible way to mock wsgi request using Exception!
        self.mock_correct_wsgi_request = Exception()
        setattr(
            self.mock_correct_wsgi_request, 'content_type', 'application/json')
        setattr(self.mock_correct_wsgi_request,
                'body', '{"group": 10, "init":2010, "end": 2012}')

        self.mock_wrong_wsgi_request = Exception()
        setattr(
            self.mock_wrong_wsgi_request, 'content_type', 'application/xml')
        setattr(self.mock_wrong_wsgi_request, 'body', 'foobar')

    def test_serialize_get_request(self):
        query = serialize_get_request(self.correct_request)

        self.assertEqual(query.init, self.correct_request['init'])
        self.assertRaises(ValidationError, lambda: serialize_get_request(
            self.wrong_request1))
        self.assertRaises(ValidationError, lambda: serialize_get_request(
            self.wrong_request2))

    def test_serialize_saving_capacity_request(self):
        query = serialize_saving_capacity_request(
            self.mock_correct_wsgi_request)

        self.assertEqual(query.group, 'top')
        self.assertRaises(
            ValidationError, lambda: serialize_saving_capacity_request(
                self.mock_wrong_wsgi_request))

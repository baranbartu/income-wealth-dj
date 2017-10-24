import logging
import itertools
import csv

from django.conf import settings

from incomewealth.app.models import IncomeWealth


logger = logging.getLogger(__name__)


def read_csv(f):
    """
    f: is an in memory file, assuming csv
    kept memory utilised using sequence/generator like xrange, yield etc.
    return sequence of list including each rows and each columns
    """

    # detect delimeter/dialect automatically
    dialect = csv.Sniffer().sniff(f.read(2014))
    # back to the top again
    f.seek(0)

    # detect column count on each row
    reader1, reader2 = itertools.tee(csv.reader(f, dialect))
    column_count = len(next(reader1))
    del reader1

    for row in reader2:
        # index 0 contains column names
        column = [row[_] for _ in xrange(column_count)]
        yield column


def update_or_create_income_and_wealth(data):
    """
    data: should be sequence of lists including income/wealth data
    """
    for index, row in enumerate(data):
        # index one contains column names
        if index == 0:
            continue

        year = int(row[0])
        obj, created = IncomeWealth.objects.update_or_create(
            year=year,
            defaults={
                'income_top10': float(row[1]),
                'wealth_top10': float(row[2]),
                'income_bottom50': float(row[3]),
                'wealth_bottom50': float(row[4])
            })

        logger.info('{}, year: {}'.format(
            'INSERTED' if created else 'UPDATED', year))


def flattenize_list_of_objects(list_of_objects):
    """
    it is for common purpose to make list of objects to flattened dict
    example;
    [{'a':123, 'b': 234}, {'a':001, 'b': 002}]
    >>
    {'a': [123, 001], 'b': [234, 002]}
    """
    return dict(
        zip(list_of_objects[0], zip(*[d.values() for d in list_of_objects])))


def common_structured_view(f):
    """
    use for api endpoints to make wrapper like {'data': <inner json result>}
    """
    def inner(*args, **kwargs):
        inner_result = f(*args, **kwargs)
        if not isinstance(inner_result, tuple):
            actual_data, status = inner_result, 200
        else:
            actual_data, status = inner_result[0], inner_result[1]

        # convert data using default api mapping
        field_mapping = settings.DEFAULT_API_FIELD_MAPPING
        for field, should_be in field_mapping.items():
            if field in actual_data:
                actual_data[should_be] = actual_data.pop(field)

        result = {'data': actual_data}, status
        return result

    return inner

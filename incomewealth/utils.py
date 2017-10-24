import logging
import itertools
import csv

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
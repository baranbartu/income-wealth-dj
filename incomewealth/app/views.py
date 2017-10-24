# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods

from jsonview.decorators import json_view

from incomewealth.utils import (read_csv,
                                update_or_create_income_and_wealth,
                                flattenize_list_of_objects,
                                common_structured_view)
from incomewealth.app.serializers import serialize_get_request
from incomewealth.app.models import IncomeWealth
from incomewealth.app.forms import CsvFileForm
from incomewealth.app.helpers import calc_year_based_inequality_factors


@json_view
@common_structured_view
@require_http_methods(['POST'])
def upload_income_and_wealth_csv(request):
    # necessary validation was made in Form implementation
    form = CsvFileForm(request.POST, request.FILES)
    if not form.is_valid():
        return {'error': form.errors.get('csv_file')[0]}, 410

    f = request.FILES['csv_file']
    # get list of list - it is like row-columns
    data = read_csv(f)
    # update or insert to database
    update_or_create_income_and_wealth(data)

    # 201 should be returned according to REST spec.
    return {'status': True}, 201


def top10_bottom50_common_part(request, column1, column2):
    """
    both column1 and column2 should be different and one of the
    2 of combinations from the
    income_top10, wealth_bottom50, income_bottom50, wealth_top10
    """
    try:
        query = serialize_get_request(request.GET)
    except ValidationError, e:
        # raise BadRequest in case of validation error
        return {'error': unicode(e.message)}, 410

    desired_columns = ('year', column1, column2)
    # get regarding values from db as dict
    list_of_objects = IncomeWealth.objects.filter(
        year__gte=query.init, year__lte=query.end).values(*desired_columns)

    # parse into related format
    return flattenize_list_of_objects(list_of_objects)


@json_view
@common_structured_view
@require_http_methods(['GET'])
def top10(request):
    return top10_bottom50_common_part(request, 'income_top10', 'wealth_top10')


@json_view
@common_structured_view
@require_http_methods(['GET'])
def bottom50(request):
    return top10_bottom50_common_part(
        request, 'income_bottom50', 'wealth_bottom50')


def inequality_factors_common_part(request, column1, column2):
    """
    column1 and column2 should be given respectively to calc. correct factor
    """
    try:
        query = serialize_get_request(request.GET)
    except ValidationError, e:
        # raise BadRequest in case of validation error
        return {'error': unicode(e.message)}, 410

    default_columns = ('year', )
    factor_sequence = (column1, column2)
    desired_columns = default_columns + factor_sequence

    # get regarding values from db as dict
    list_of_objects = IncomeWealth.objects.filter(
        year__gte=query.init, year__lte=query.end).values(*desired_columns)

    inequality_factors = calc_year_based_inequality_factors(
        list_of_objects, factor_sequence)

    return flattenize_list_of_objects(list(inequality_factors))


@json_view
@common_structured_view
@require_http_methods(['GET'])
def wealth_inequality(request):
    return inequality_factors_common_part(
        request, 'wealth_bottom50', 'wealth_top10')


@json_view
@common_structured_view
@require_http_methods(['GET'])
def income_inequality(request):
    return inequality_factors_common_part(
        request, 'income_bottom50', 'income_top10')

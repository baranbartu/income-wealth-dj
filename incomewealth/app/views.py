# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods

from jsonview.decorators import json_view

from incomewealth.utils import (read_csv,
                                update_or_create_income_and_wealth,
                                flattenize_list_of_objects,
                                common_structured_view)
from incomewealth.app.serializers import (serialize_get_request,
                                          serialize_saving_capacity_request,
                                          serialize_predict_request)
from incomewealth.app.models import IncomeWealth
from incomewealth.app.forms import CsvFileForm
from incomewealth.app.helpers import (
    calc_year_based_inequality_factors, calc_year_based_saving_capacities)
from incomewealth.app import prediction


@json_view
@common_structured_view
@require_http_methods(['POST'])
def upload_income_and_wealth_csv(request):
    """
    example: /api/v1/upload-income-and-wealth-csv/
    and use "csv_file" field while uploading the file
    """
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
    values = IncomeWealth.objects.filter(
        year__gte=query.init, year__lte=query.end).values(*desired_columns)

    # parse into related format
    return flattenize_list_of_objects(values)


@json_view
@common_structured_view
@require_http_methods(['GET'])
def top10(request):
    """
    example: /api/v1/top10/?init=1972&end=1978
    """
    return top10_bottom50_common_part(request, 'income_top10', 'wealth_top10')


@json_view
@common_structured_view
@require_http_methods(['GET'])
def bottom50(request):
    """
    example: /api/v1/bottom50/?init=1972&end=1978
    """
    return top10_bottom50_common_part(
        request, 'income_bottom50', 'wealth_bottom50')


def inequality_factors_common_part(request, _type):
    """
    request: wsgi request
    _type: wealth or income
    """
    try:
        query = serialize_get_request(request.GET)
    except ValidationError, e:
        # raise BadRequest in case of validation error
        return {'error': unicode(e.message)}, 410

    # define desired columns using inequality type
    desired_columns = ('year', '{}_bottom50'.format(_type),
                       '{}_top10'.format(_type))

    # get regarding values from db as dict
    values = IncomeWealth.objects.filter(
        year__gte=query.init, year__lte=query.end).values(*desired_columns)

    inequality_factors = calc_year_based_inequality_factors(values, _type)

    return flattenize_list_of_objects(list(inequality_factors))


@json_view
@common_structured_view
@require_http_methods(['GET'])
def wealth_inequality(request):
    """
    example: /api/v1/wealthinequality/?init=1972&end=1978
    """
    return inequality_factors_common_part(request, 'wealth')


@json_view
@common_structured_view
@require_http_methods(['GET'])
def income_inequality(request):
    """
    example: /api/v1/incomeinequality/?init=1972&end=1978
    """
    return inequality_factors_common_part(request, 'income')


# POST end points
@json_view
@common_structured_view
@require_http_methods(['POST'])
def saving_capacity(request):
    """
    example: POST /api/v1/savingcapacity/ with below kind of data
    data: {"group": 10, "init":2010, "end": 2012}
    """
    try:
        query = serialize_saving_capacity_request(request)
    except ValidationError, e:
        # raise BadRequest in case of validation error
        return {'error': unicode(e.message)}, 410

    # get regarding values from db as dict
    values = IncomeWealth.objects.filter(
        year__gte=query.init, year__lte=query.end).values(
            *('year', query.group_column))

    saving_capacities = calc_year_based_saving_capacities(
        values, query.group, query.group_people_ratio)

    flattened_values = flattenize_list_of_objects(list(saving_capacities))
    flattened_values.update({'Group': query.group_people_ratio})
    return flattened_values


def predict_common_parts(request, _type):
    """
    request: wsgi request
    _type: wealth or income
    """
    try:
        query = serialize_predict_request(request)
    except ValidationError, e:
        # raise BadRequest in case of validation error
        return {'error': unicode(e.message)}, 410

    # it will make like 'income_bottom50'
    column = '{}_{}{}'.format(_type, query.group_verbose, query.group)
    # cache key may be changed with time when new income/wealth data added
    predictor_cache_key = '{}_{}'.format(
        column, settings.MAX_YEAR_TO_TRAIN_DATA)
    # check if exists in the cache
    predictor = prediction.get_predictor(predictor_cache_key)
    if not predictor:
        # get matrix
        matrix = IncomeWealth.objects.filter(
            year__lte=settings.MAX_YEAR_TO_TRAIN_DATA).values_list(
                *('year', column))
        # make predictor using regarding data
        predictor = prediction.make_linear_predictor(
            predictor_cache_key, matrix)

    predicted_data = []
    for _ in range(query.years):
        # each year should come after MAX_YEAR_TO_TRAIN_DATA
        # range starts from 0, thus we need to add 1 on each iteration
        year = settings.MAX_YEAR_TO_TRAIN_DATA + _ + 1
        predicted_value = predictor(year)
        predicted_data.append(predicted_value)

    return {'Group': query.group, 'prediction': predicted_data}


@json_view
@common_structured_view
@require_http_methods(['POST'])
def predict_wealth(request):
    """
    example: POST /api/v1/predictwealth/ with below kind of data
    data: {"group": <10|50>, "years": 5}
    """
    return predict_common_parts(request, 'wealth')


@json_view
@common_structured_view
@require_http_methods(['POST'])
def predict_income(request):
    """
    example: POST /api/v1/predictwealth/ with below kind of data
    data: {"group": <10|50>, "years": 5}
    """
    return predict_common_parts(request, 'income')

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods

from jsonview.decorators import json_view

from incomewealth.utils import read_csv, update_or_create_income_and_wealth
from incomewealth.app.serializers import serialize_get_request
from incomewealth.app.models import IncomeWealth
from incomewealth.app.forms import CsvFileForm


@json_view
@require_http_methods(['POST'])
def upload_income_and_wealth_csv(request):
    # necessary validation was made in Form implementation
    form = CsvFileForm(request.POST, request.FILES)
    if not form.is_valid():
        return {'error': form.errors.get('csv_file')[0]}, 410

    f = request.FILES['csv_file']
    data = read_csv(f)
    update_or_create_income_and_wealth(data)
    return {'status': True}


@json_view
@require_http_methods(['GET'])
def top10(request):
    try:
        query = serialize_get_request(request.GET)
    except ValidationError, e:
        # raise BadRequest in case of validation error
        return {'error': unicode(e.message)}, 410

    # get regarding values from db as dict
    objects = IncomeWealth.objects.filter(
        year__gte=query.init, year__lte=query.end).values(
            'year', 'income_top10', 'wealth_top10')

    # parse into related format
    return dict(zip(objects[0], zip(*[d.values() for d in objects])))


@json_view
@require_http_methods(['GET'])
def bottom50(request):
    try:
        query = serialize_get_request(request.GET)
    except ValidationError, e:
        # raise BadRequest in case of validation error
        return {'error': unicode(e.message)}, 410

    # get regarding values from db as dict
    objects = IncomeWealth.objects.filter(
        year__gte=query.init, year__lte=query.end).values(
            'year', 'income_bottom50', 'wealth_bottom50')

    # parse into related format
    return dict(zip(objects[0], zip(*[d.values() for d in objects])))

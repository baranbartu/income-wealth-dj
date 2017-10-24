# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError

from jsonview.decorators import json_view

from incomewealth.app.serializers import serialize_top10_request
from incomewealth.app.models import IncomeWealth


@json_view
def top10(request):
    try:
        query = serialize_top10_request(request.GET)
    except ValidationError, e:
        # raise BadRequest in case of validation error
        return {'error': unicode(e.message)}, 410

    # get regarding values from db as dict
    objects = IncomeWealth.objects.filter(
        year__gte=query.init, year__lte=query.end).values(
            'year', 'income_top10', 'wealth_top10')

    # parse into related format
    # TODO
    return list(objects)

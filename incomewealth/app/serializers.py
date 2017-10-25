import json

from collections import namedtuple

from django.core.exceptions import ValidationError

QueryGet = namedtuple('QueryGet', ('init', 'end'))
QuerySavingCapacity = namedtuple('QuerySavingCapacity',
                                 ('group_column', 'init',
                                  'end', 'group_people_ratio',
                                  'group'))


def serialize_get_request(data):
    if not all(_ in data for _ in ['init', 'end']):
        raise ValidationError('"init" and "end" should be provided!')

    try:
        init = int(data.get('init'))
        end = int(data.get('end'))
    except ValueError, e:
        raise ValidationError(e.message)

    return QueryGet(init=init, end=end)


def serialize_saving_capacity_request(request):
    body = request.body
    content_type = request.content_type

    if content_type != 'application/json':
        raise ValidationError('Content-Type should be application/json only!')

    try:
        data = json.loads(body)
    except (ValueError, TypeError, NameError):
        raise ValidationError('Should be provided a proper json data!')

    if not all(_ in data for _ in ['group', 'init', 'end']):
        raise ValidationError('"group", "init" and "end" should be provided!')

    group_key = data['group']
    (group_column,
     group_people_ratio,
     group) = ('income_bottom50', 50, 'bottom') if (
         group_key) == 50 else (
             'income_top10', 10, 'top') if group_key == 10 else (
                 None, None, None)
    if not group_column:
        raise ValidationError('Should be provided proper group: 10||50')

    return QuerySavingCapacity(
        group_column=group_column, init=int(data['init']),
        end=int(data['end']), group_people_ratio=group_people_ratio,
        group=group)

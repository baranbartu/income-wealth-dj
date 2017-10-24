from collections import namedtuple

from django.core.exceptions import ValidationError

QueryTop10 = namedtuple('QueryTop10', ('init', 'end'))


def serialize_get_request(data):
    if not all(_ in data for _ in ['init', 'end']):
        raise ValidationError('"init" and "end" should be provided!')

    try:
        init = int(data.get('init'))
        end = int(data.get('end'))
    except ValueError, e:
        raise ValidationError(e.message)

    return QueryTop10(init=init, end=end)

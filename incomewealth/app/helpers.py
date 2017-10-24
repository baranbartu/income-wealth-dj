def calc_year_based_inequality_factors(list_obj_objects, factor_sequence):
    """
    list_obj_objects: is a list which consists objs like {'year': 2010,
    'bottom50': 0.3456, 'top10': 0.6834}
    return a sequence which each obj consists factor according to factor
    sequence and regarding year
    """
    first_param = factor_sequence[0]
    second_param = factor_sequence[1]

    for obj in list_obj_objects:
        factor = obj[first_param] / obj[second_param]
        yield {'year': obj['year'], 'factor': factor}

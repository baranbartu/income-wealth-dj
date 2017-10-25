def calc_year_based_inequality_factors(values, _type):
    """
    values: is a list which consists objs like {'year': 2010,
    'bottom50': 0.3456, 'top10': 0.6834}
    return a sequence which each obj consists factor according to
    _type and regarding year
    """
    bottom50_column, bottom50_people_ratio = '{}_bottom50'.format(_type), 50.0
    top10_column, top10_people_ratio = '{}_top10'.format(_type), 10.0

    for obj in values:
        bottom50_val = obj[bottom50_column]
        top10_val = obj[top10_column]

        # find avg values for one person in specific groups using income or
        # wealth distrubution and people count(ratio) in groups
        avg_ratio_in_bottom50 = bottom50_val / bottom50_people_ratio
        avg_ratio_in_top10 = top10_val / top10_people_ratio

        # factor (assumed) should be ratio between above ratios
        factor = avg_ratio_in_bottom50 / avg_ratio_in_top10
        yield {'year': obj['year'], 'factor': factor}


def calc_year_based_saving_capacities(values, group, group_people_ratio):
    """
    saving capacity can be calculated using income and consumption, not wealth
    but we have no info about consumption, thus we can assume consumption is
    the same for each year
    """
    column = 'income_{}{}'.format(group, group_people_ratio)
    for index, obj in enumerate(values):
        if index < len(values) - 1:
            next_obj = values[index + 1]
            # between below years calculation
            years = (obj['year'], next_obj['year'])

            # find year specific income distribution for the one person who
            # belong the regarding group
            current_per_people_ratio = obj[column] / group_people_ratio
            next_per_people_ratio = next_obj[column] / group_people_ratio

            diff = next_per_people_ratio - current_per_people_ratio
            saving_capacity = diff / current_per_people_ratio
            yield {'year': years, 'savingcapacity': saving_capacity}

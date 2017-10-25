# in memory to prevent training time on each call
predictors = {}


def make_linear_predictor(cache_key, matrix):
    """
    matrix: example [(2000, 0.3672), (2001, 0.3543), ...]
    cache_key: will be used to cache calculated func

    we have 2x2 matrix like [(year, distrubution), ..], thus we can use linear
    regression to be able predict next years
    so , we need a function like f(x) = ax + b , where x-year, f(x)-distr.
    and need to find a and b to make ax + b according to given matrix
    """

    # basic avg function
    avg = lambda L: 1.0 * sum(L) / len(L) # noqa
    # zip(*matrix) >> [(2000, 2001), (0.3672, 0.3543), ...]
    # we need to get x_avg >> avg year, y_avg >> avg distribution
    x_avg, y_avg = map(avg, zip(*matrix))

    a_num = 0
    a_denom = 0
    for x, y in matrix:
        a_num += (y - y_avg) * x
        a_denom += (x - x_avg) * x

    a = float(a_num) / a_denom
    b = y_avg - a * x_avg
    predictor = lambda x: a * x + b # noqa
    # cache it!
    predictors[cache_key] = predictor
    return predictor


def get_predictor(cache_key):
    return predictors.get(cache_key)

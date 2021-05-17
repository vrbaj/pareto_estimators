import scipy
from functools import wraps
from timeit import default_timer as time


def measure_time(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        duration = end - start
        print('Elapsed time: {}'.format(duration))
        return result, duration
    return wrapper


@measure_time
def dummy_estimator(data_series):
    return min(data_series)


pareto_data = [1, 2, 3]
params, measured_time = dummy_estimator(pareto_data)
print(params)
print(measured_time)

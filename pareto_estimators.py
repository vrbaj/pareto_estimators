from scipy.stats import pareto
from functools import wraps
from timeit import default_timer as time
import numpy as np


def measure_time(f):
    """
    decorating function to measure time of function f execution
    :param f: function whose time is measured
    :return: the results of function f and total time of its execution
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        duration = end - start
        print('Elapsed time: {} seconds'.format(duration) + ' for function ' + f.__name__)
        results_dict[f.__name__] = [result, duration]
        return result, duration
    return wrapper


@measure_time
def dummy_estimator(data_series):
    """
    dummy function to illustrate how to work with @measure_time decorator
    :param data_series: samples from pareto distribution that are used to estimate its parameters
    :return: it should return the shape and scale parameters, now it returns dummy tuple
    """
    return min(data_series), max(data_series)


def get_pareto_data(shape, scale, number_of_data):
    """
    function to generate data from Pareto distribution specified by shape (alpha) and scale (gamma) parameters
    :param shape: alpha parameter of pareto distribution
    :param scale: gamma parameter of pareto distribution
    :param number_of_data: number of data samples to generate
    :return: numpy.ndarray with samples from pareto distribution specified by :param shape and :param scale.
    """
    data = pareto.rvs(shape, scale=scale, size=number_of_data)
    return data


@measure_time
def umvue_estimator(data_series):
    """
    function that implements uniformly minimum variance unbiased estimators for Pareto distribution
    (ESTIMATION OF THE SHAPE AND SCALE PARAMETERS OF THE PARETO DISTRIBUTION USING EXTREME RANKED SET SAMPLING)
    :param data_series: samples from pareto distribution that are used to estimate its parameters
    :return: tuple (alpha, gamma) that contains estimated parameters of Pareto distribution
    """
    n = len(data_series)
    x1 = min(data_series)
    data_series = data_series / x1
    triple_dot_alpha = n * (np.sum(np.log(data_series)) ** - 1)
    alpha = (1 - 2 * (n ** -1)) * triple_dot_alpha
    gamma = (1 - ((n - 1) ** - 1) * triple_dot_alpha ** -1) * x1
    return alpha, gamma


@measure_time
def maximum_likelihood_estimator(data_series):
    """
    function that implements the maximum likelihood estimator as closed solution
    (ESTIMATION OF THE SHAPE AND SCALE PARAMETERS OF THE PARETO DISTRIBUTION USING EXTREME RANKED SET SAMPLING)
    :param data_series: samples from pareto distribution that are used to estimate its parameters
    :return: tuple (alpha, gamma) that contains estimated parameters of Pareto distribution
    """
    n = len(data_series)
    gamma = min(data_series)
    data_series = data_series / gamma
    alpha = n * (np.sum(np.log(data_series)) ** - 1)
    return alpha, gamma


@measure_time
def maximum_likelihood_estimator_scipy(data_series):
    """
    wrapper for scipy default ML estimator
    :param data_series: samples from pareto distribution that are used to estimate its parameters
    :return: tuple (alpha, gamma) that contains estimated parameters of Pareto distribution
    """
    params = [0, 0, 0]
    params = pareto.fit(data_series)
    return params[0], params[2]


results_dict = {}
pareto_shape = 2
pareto_scale = 5
pareto_data = get_pareto_data(pareto_shape, pareto_scale, 100)
dummy_estimator(pareto_data)
umvue_estimator(pareto_data)
maximum_likelihood_estimator(pareto_data)
maximum_likelihood_estimator_scipy(pareto_data)

print(results_dict)

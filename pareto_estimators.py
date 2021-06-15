from scipy.stats import pareto
from scipy.stats import hmean
from functools import wraps
from timeit import default_timer as time
import numpy as np
import pickle


def measure_time(f):
    """
    decorating function to measure time of function f execution
    :param f: function whose time is measured
    :return: the results of function f and total time of its execution
    """

    # noinspection PyShadowingNames
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        duration = end - start
        # print('Elapsed time: {} seconds'.format(duration) + ' for function ' + f.__name__)
        if f.__name__ not in results_dict.keys():
            results_dict[f.__name__] = [[result, duration]]
        else:
            results_dict[f.__name__].append([result, duration])
        return result, duration

    return wrapper


@measure_time
def dummy_estimator(data_series):
    """
    dummy function to illustrate how to work with @measure_time decorator
    :param data_series: samples from pareto distribution that are used to estimate its parameters
    :return: it should return the shape and location parameters, now it returns dummy tuple
    """
    return min(data_series), max(data_series)


def get_pareto_data(shape, location, number_of_data):
    """
    function to generate data from Pareto distribution specified by shape (alpha) and location (gamma) parameters
    :param shape: alpha parameter of pareto distribution
    :param location: gamma parameter of pareto distribution
    :param number_of_data: number of data samples to generate
    :return: numpy.ndarray with samples from pareto distribution specified by :param shape and :param location.
    """
    data = pareto.rvs(shape, scale=location, size=number_of_data)
    return data


@measure_time
def umvue_estimator(data_series):
    """
    function that implements uniformly minimum variance unbiased estimators for Pareto distribution
    (ESTIMATION OF THE SHAPE AND location PARAMETERS OF THE PARETO DISTRIBUTION USING EXTREME RANKED SET SAMPLING)
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
def ml_estimator(data_series):
    """
    function that implements the maximum likelihood estimator as closed solution
    (ESTIMATION OF THE SHAPE AND location PARAMETERS OF THE PARETO DISTRIBUTION USING EXTREME RANKED SET SAMPLING)
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
    params = pareto.fit(data_series)
    return params[0], params[2]


@measure_time
def mom_estimator(data_series):
    """
    function that implements the Method of Moments estimator
    (Parameter estimation of Pareto distribution: some modified moment estimators)
    :param data_series: samples from pareto distribution that are used to estimate its parameters
    :return: tuple (alpha, gamma) that contains estimated parameters of Pareto distribution
    """
    t = np.mean(data_series)
    s2 = np.var(data_series)
    s = np.sqrt(s2)
    alpha = 1 + np.sqrt(1 + (t ** 2) / s2)
    gamma = np.sqrt(s2 + t ** 2) / (s + np.sqrt(s2 + t ** 2)) * t
    return alpha, gamma


@measure_time
def mm1_estimator(data_series):
    """
    function that implements the first modification of Method of Moments estimator
    (Parameter estimation of Pareto distribution: some modified moment estimators)
    :param data_series: samples from pareto distribution that are used to estimate its parameters
    :return: tuple (alpha, gamma) that contains estimated parameters of Pareto distribution
    """
    s2 = np.var(data_series)
    s = np.sqrt(s2)
    t2 = np.mean(data_series) ** 2
    alpha = 1 + np.sqrt(1 + t2 / s2)
    gamma = np.sqrt((s2 + t2) * (np.sqrt(s2 + t2) - s) / (s + np.sqrt(s2 + t2)))
    return alpha, gamma


@measure_time
def mm2_estimator(data_series):
    """
    function that implements the second modification of Method of Moments estimator
    (Parameter estimation of Pareto distribution: some modified moment estimators)
    :param data_series: samples from pareto distribution that are used to estimate its parameters
    :return: tuple (alpha, gamma) that contains estimated parameters of Pareto distribution
    """
    hm = hmean(data_series)
    t = np.mean(data_series)

    alpha = np.sqrt(1 + hm / t)
    gamma = np.sqrt(t + hm) * hm / (np.sqrt(t) + np.sqrt(t + hm))

    return alpha, gamma


@measure_time
def mm3_estimator(data_series):
    """
    function that implements the third modification of Method of Moments estimator
    (Parameter estimation of Pareto distribution: some modified moment estimators)
    :param data_series: samples from pareto distribution that are used to estimate its parameters
    :return: tuple (alpha, gamma) that contains estimated parameters of Pareto distribution
    """
    t1 = min(data_series)
    n = len(data_series)
    t = np.mean(data_series)

    alpha = (t1 - n * t) / (n * (t1 - t))
    gamma = t1 - t1 / (n * alpha)

    return alpha, gamma


@measure_time
def mm4_estimator(data_series):
    """
    function that implements the fourth modification of Method of Moments estimator
    (Parameter estimation of Pareto distribution: some modified moment estimators)
    :param data_series: samples from pareto distribution that are used to estimate its parameters
    :return: tuple (alpha, gamma) that contains estimated parameters of Pareto distribution
    """
    t1 = min(data_series)
    n = len(data_series)
    t = np.mean(data_series)
    alpha = ((n - 1) * t) / (n * (t - t1))
    gamma = t1 * (n / (n + 1)) ** (1 / alpha)
    return alpha, gamma


results_dict = {}
pareto_shape = 5
pareto_location = 3
experiments_number = 10000
data_quantity = 1000
function_names = ["umvue_estimator", "ml_estimator", "mom_estimator", "mm1_estimator", "mm2_estimator", "mm3_estimator",
                  "mm4_estimator"]

for experiment in range(experiments_number):
    for function_name in function_names:
        pareto_data = get_pareto_data(pareto_shape, pareto_location, data_quantity)
        eval(function_name + "(pareto_data)")
    if experiment % 100 == 99:
        print("Evaluated {:.2%} experiments".format((experiment + 1) / experiments_number))

avg_results = {}
for k in results_dict.keys():
    print(k)
    if "scipy" not in k:
        total_time = []
        for result in results_dict[k]:
            total_time.append(result[1])
        avg_results[k.replace("_estimator", "")] = [np.average(total_time), np.std(total_time), np.max(total_time)]

print(avg_results)
with open("experiment_{}.pickle".format(data_quantity), "wb") as handle:
    pickle.dump(avg_results, handle, protocol=pickle.HIGHEST_PROTOCOL)

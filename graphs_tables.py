from matplotlib import pyplot as plt
import pickle
import collections


def graph_plotter(results_dictionary, file_name):
    """
    function to create and save a graph for an article with average computational times for each method
    that are  in results_dictionary
    :param file_name: name of file with eps extension where the plot is saved (i.e. computational_times.eps)
    :param results_dictionary: dictionary where the key is the method name and value is a list
    [average computational time, std dev, maximum computational time]
    :return: None
    """
    computational_times = [value[0] for key, value in results_dictionary.items()]
    plt.bar(results_dictionary.keys(), computational_times)
    plt.xlabel("Estimation method")
    plt.ylabel("Computational time [$s$]")
    plt.tight_layout(True)
    plt.savefig(file_name, format="eps", dpi=600)


def table(sample_sizes, file_name):
    """
    function to create tex table with average computational times and maximum computational times for each method and
    for various sample sizes. Data are loaded from pickle files that contains dictionary (key is the method name, value
    is [average computational time, std dev, maximum computational time]
    :param file_name: name of file where is the tex table saved
    :param sample_sizes: number that specified pickled file with according sample size.. (i.e. 50 means that
    "experiment_50.pickle" is going to be load
    :return: None
    """
    results = {}
    for size in sample_sizes:
        with open("experiment_{}.pickle".format(size), "rb") as handle:
            results[str(size)] = pickle.load(handle)
        handle.close()
    result_by_method = dict.fromkeys(results[str(size)].keys(), [])

    counter = 0
    print(results)

    with open(file_name, "w") as f:
        f.writelines(r"\begin{table}[]" + "\n")
        f.writelines(r"\centering" + "\n")
        s = '|{}|'.format('|'.join('c' for _ in range(len(sample_sizes) * 2 + 1)))
        f.writelines(r"\begin{tabular}{" + s + "}" + "\n")
        f.writelines(r"\hline" + "\n")
        s = "{}".format("& \multicolumn{2}{c|}{$n = ".join(str(n) + "$}" for n in sample_sizes))
        f.writelines(r"\multirow{2}{*}{method} & \multicolumn{2}{c|}{$n =  " + s
                     + r"\\ \cline{2 -" + str(len(sample_sizes) * 2 + 1) + "}" + "\n")
        s = "{}".format(" & ".join("$CT_{avg}$ & $CT_{max}$" for _ in range(len(sample_sizes))))
        f.writelines(r" & " + s + r"\\ \hline" + "\n")
        for method in result_by_method:
            s = method
            for sample_number, dicts in results.items():
                s = s + r" & ${:.2f}$ & ${:.2f}$ ".format(1000000 * dicts[method][0],
                                                              1000000 * dicts[method][2]).replace("e-0", "\cdot 10^{-")
                print(s)
            s = s + r" \\ \hline" + "\n"
            f.write(s)
        f.writelines(r"\end{tabular}" + "\n")
        f.writelines(r"\end{table}" + "\n")
    f.close()
    print(result_by_method)

def table_maker(results_dictionary, file_name):
    """
    function to create tex table with average computational times for each method that is in results_dictionary
    :param results_dictionary: dictionary where the key is the method name and value is a list
    [average computational time, std dev]
    :param file_name: name of plain text with with latex table
    :return: None
    """
    with open(file_name, "w") as f:
        f.writelines(r"\begin{table}[]" + "\n")
        f.writelines(r"\centering" + "\n")
        f.writelines(r"\begin{tabular}{|c|c|c|}" + "\n")
        f.writelines(r"\hline" + "\n")
        f.writelines(r"Method & $\overline{CT}$ & $\sigma_{CT}$" + "$CT_{max}$" + "\n")
        f.writelines(r"\hline" + "\n")
        for key in results_dictionary.keys():
            f.writelines(key + (r" & {:.2e} &  {:.2e} & {:.2e}\\ \hline".format(1000 * results_dictionary[key][0],
                                                                                 1000 *results_dictionary[key][1],
                                                                                 1000 * results_dictionary[key][2])) + "\n")
        f.writelines(r"\end{tabular}" + "\n")
        f.writelines(r"\end{table}" + "\n")

    f.close()


def graph_plotter_ext(sample_sizes, file_name):
    """
    function to create graph with average computational times times for each method and
    for various sample sizes. Data are loaded from pickle files that contains dictionary (key is the method name,
    value is [average computational time, std dev, maximum computational time]
    :param file_name: name of file where is the tex table saved
    :param sample_sizes: number that specified pickled file with according sample size.. (i.e. 50 means that
    "experiment_50.pickle" is going to be load
    :return: None
    """
    results = {}
    x_labels = []
    for size in sample_sizes:
        x_labels.append(int(size))
        with open("experiment_{}.pickle".format(size), "rb") as handle:
            results[str(size)] = pickle.load(handle)
        handle.close()
    result_by_method = dict.fromkeys(results[str(size)].keys(), [])
    for method in result_by_method:
        s = method
        for sample_number, dicts in results.items():
            s = s + r" & ${:.2f}$ & ${:.2f}$ ".format(1000000 * dicts[method][0],
                                                      1000000 * dicts[method][2]).replace("e-0", "\cdot 10^{-")
            print(s)

def table_error_comparison(params,sample_sizes, file_name):
    """
    function to create tex table with MSE errors comparison for each method and
    for various sample sizes. Data are loaded from pickle files that contains dictionary (key is the method name, value
    is [mse_alpha, mse_gamma]
    :param file_name: name of file where is the tex table saved
    :param sample_sizes: number that specified pickled file with according sample size.. (i.e. 50 means that
    :param params: array with parameter values
    :return: None
    """
    results = {
        "size": [],
        "params": [],
        "umvue": [],
        "ml": [],
        "mom": [],
        "mm1": [],
        "mm2": [],
        "mm3": [],
        "mm4": []
    }

    for size in sample_sizes:
        for parset in params:
            with open("errors_params_{}_{}_samplesize_{}.pickle".format(parset[0], parset[1], size), "rb") as handle:
                dict = pickle.load(handle)
                for key,val in dict.items():
                    results[key].append(val)
            handle.close()
            results["size"].append(size)
            results["params"].append(parset)


    with open(file_name, "w") as f:
        # Header
        f.writelines(r"\begin{table}"+"\n")
        f.writelines(r"\centering"+"\n")
        f.writelines(r"\begin{tabular}{| c | c  c | c | c c |}"+"\n")
        f.writelines(r"\hline"+"\n")
        f.writelines(r"\multirow{2}{*}{n} & \multicolumn{2}{| c |}{True Values} & \multirow{2}{*}{Method} &  \multicolumn{2}{| c |}{MSE} \\"+"\n")
        f.writelines(r"& $\alpha$ & $\gamma$ & & $\alpha$ & $\gamma$ \\"+"\n")
        f.writelines(r"\hline"+"\n")

        counter = 0
        for i in range(len(results["size"])):
            f.writelines(r"\multirow{7}{*}{"+ str(results["size"][i]) +r"} & ")
            f.writelines(r"\multirow{7}{*}{" + str(results["params"][i][0]) +r"} & ")
            f.writelines(r"\multirow{7}{*}{" + str(results["params"][i][1]) +r"} & ")
            # s_repeated = "{} & {} & {}".format(results["size"][i], results["params"][i][0], results["params"][i][1])
            for key in list(results.keys())[2:]:
                counter += 1
                if key == "umvue":
                    s = r"{} & {:.2e} & {:.2e} \\".format(key, results[key][i][0], results[key][i][1]) + "\n"
                else:
                    s = r"& & & {} & {:.2e} & {:.2e} \\".format(key, results[key][i][0], results[key][i][1]) + "\n"
                f.writelines(s)
            f.write(r"\hline"+"\n")
        f.writelines(r"\end{tabular}" + "\n")
        f.writelines(r"\end{table}" + "\n")

    f.close()

def table_error_comparison_split(params,sample_sizes, file_name):
    """
    function to create tex tables (divided by sample size) with MSE errors comparison for each method and
    for various sample sizes. Data are loaded from pickle files that contains dictionary (key is the method name, value
    is [mse_alpha, mse_gamma]
    :param file_name: name of file where is the tex table saved
    :param sample_sizes: number that specified pickled file with according sample size.. (i.e. 50 means that
    :param params: array with parameter values
    :return: None
    """
    results = {
        "size": [],
        "params": [],
        "umvue": [],
        "ml": [],
        "mom": [],
        "mm1": [],
        "mm2": [],
        "mm3": [],
        "mm4": []
    }

    with open(file_name, "w") as f:
        pass
    f.close()

    for size in sample_sizes:
        for parset in params:
            with open("errors_params_{}_{}_samplesize_{}.pickle".format(parset[0], parset[1], size), "rb") as handle:
                dict = pickle.load(handle)
                for key,val in dict.items():
                    results[key] = val
            handle.close()
            results["size"] = size
            results["params"] = parset


        with open(file_name, "a") as f:
            # Header
            f.writelines(r"\begin{table}"+"\n")
            f.writelines(r"\centering"+"\n")
            f.writelines(r"\begin{tabular}{| c | c  c | c | c c |}"+"\n")
            f.writelines(r"\hline"+"\n")
            f.writelines(r"\multirow{2}{*}{n} & \multicolumn{2}{| c |}{True Values} & \multirow{2}{*}{Method} &  \multicolumn{2}{| c |}{MSE} \\"+"\n")
            f.writelines(r"& $\alpha$ & $\gamma$ & & $\alpha$ & $\gamma$ \\"+"\n")
            f.writelines(r"\hline"+"\n")

            counter = 0

            f.writelines(r"\multirow{7}{*}{"+ str(results["size"]) +r"} & ")
            f.writelines(r"\multirow{7}{*}{" + str(results["params"][0]) +r"} & ")
            f.writelines(r"\multirow{7}{*}{" + str(results["params"][1]) +r"} & ")
            # s_repeated = "{} & {} & {}".format(results["size"][i], results["params"][i][0], results["params"][i][1])
            for key in list(results.keys())[2:]:
                counter += 1
                if key == "umvue":
                    s = r"{} & {:.2e} & {:.2e} \\".format(key, results[key][0], results[key][1]) + "\n"
                else:
                    s = r"& & & {} & {:.2e} & {:.2e} \\".format(key, results[key][0], results[key][1]) + "\n"
                f.writelines(s)
            f.write(r"\hline"+"\n")
            f.writelines(r"\end{tabular}" + "\n")
            f.writelines(r"\end{table}" + "\n")

        f.close()


sample_sizes = [100]
params = [2,1]
sample_sizes = [50,100]
params = [[2,1],[4,1],[5,3]]

# table(sample_sizes, "example.tex")
# graph_plotter_ext(sample_sizes, "graph.eps")
table_error_comparison(params,sample_sizes,"example_errors.tex")



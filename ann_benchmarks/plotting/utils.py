from __future__ import absolute_import

import os, itertools, json, numpy, pickle
from ann_benchmarks.plotting.metrics import all_metrics as metrics
import matplotlib.pyplot as plt

def create_pointset(algo, all_data, xn, yn):
    xm, ym = (metrics[xn], metrics[yn])
    data = all_data[algo]
    rev = ym["worst"] < 0
    data.sort(key=lambda t: t[-1][yn], reverse=rev) # sort by y coordinate

    axs, ays, als = [], [], []
    # Generate Pareto frontier
    xs, ys, ls = [], [], []
    last_x = xm["worst"]
    comparator = \
      (lambda xv, lx: xv > lx) if last_x < 0 else (lambda xv, lx: xv < lx)
    for algo, algo_name, results in data:
        xv, yv = (results[xn], results[yn])
        if not xv or not yv:
            continue
        axs.append(xv)
        ays.append(yv)
        als.append(algo_name)
        if comparator(xv, last_x):
            last_x = xv
            xs.append(xv)
            ys.append(yv)
            ls.append(algo_name)
    return xs, ys, ls, axs, ays, als

def compute_metrics(dataset, res):
    all_results = {}
    all_algos = set()
    for definition, run in res:
        algo = definition.algorithm
        algo_name = run.attrs['name']

        print('--')
        print(algo_name)
        results = {}
        for name, metric in metrics.items():
            v = metric["function"](dataset, run)
            results[name] = v
            if v:
                print('%s: %g' % (name, v))

        all_algos.add(algo)
        if not algo in all_results:
            all_results[algo] = []
        all_results[algo].append((algo, algo_name, results))
    return (all_results, all_algos)

def generate_n_colors(n):
    vs = numpy.linspace(0.4, 1.0, 7)
    colors = [(.9, .4, .4, 1.)]
    def euclidean(a, b):
        return sum((x-y)**2 for x, y in zip(a, b))
    while len(colors) < n:
        new_color = max(itertools.product(vs, vs, vs), key=lambda a: min(euclidean(a, b) for b in colors))
        colors.append(new_color + (1.,))
    return colors

def create_linestyles(unique_algorithms):
    colors = dict(zip(unique_algorithms, generate_n_colors(len(unique_algorithms))))
    linestyles = dict((algo, ['--', '-.', '-', ':'][i%4]) for i, algo in enumerate(unique_algorithms))
    markerstyles = dict((algo, ['+', '<', 'o', '*', 'x'][i%5]) for i, algo in enumerate(unique_algorithms))
    faded = dict((algo, (r, g, b, 0.3)) for algo, (r, g, b, a) in colors.items())
    return dict((algo, (colors[algo], faded[algo], linestyles[algo], markerstyles[algo])) for algo in unique_algorithms)

def get_up_down(metric):
    if metric["worst"] == float("inf"):
        return "down"
    return "up"

def get_left_right(metric):
    if metric["worst"] == float("inf"):
        return "left"
    return "right"

def get_plot_label(xm, ym):
    return "%(xlabel)s-%(ylabel)s tradeoff - %(updown)s and to the %(leftright)s is better" % {
            "xlabel" : xm["description"], "ylabel" : ym["description"], "updown" : get_up_down(ym), "leftright" : get_left_right(xm) }


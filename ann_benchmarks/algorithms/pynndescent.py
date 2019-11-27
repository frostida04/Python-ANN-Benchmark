from __future__ import absolute_import
import pynndescent
from ann_benchmarks.algorithms.base import BaseANN
import numpy as np


class PyNNDescent(BaseANN):

    def __init__(self, metric, index_param_dict, n_search_trees=1, n_jobs=1):
        if "n_neighbors" in index_param_dict:
            self._n_neighbors = int(index_param_dict["n_neighbors"])
        else:
            self._n_neighbors = 10

        if "pruning_degree_multiplier" in index_param_dict:
            self._pruning_degree_multiplier = float(
                index_param_dict["pruning_degree_multiplier"])
        else:
            self._pruning_degree_multiplier = 1.5

        if "diversify_epsilon" in index_param_dict:
            self._diversify_epsilon = float(index_param_dict["diversify_epsilon"])
        else:
            self._diversify_epsilon = 1.0

        if "leaf_size" in index_param_dict:
            self._leaf_size = int(index_param_dict["leaf_size"])
        else:
            leaf_size = 32

        self._n_search_trees = int(n_search_trees)
        self._n_jobs = int(n_jobs)

        self._n_search_trees = int(n_search_trees)
        self._pynnd_metric = {'angular': 'cosine',
                              'euclidean': 'euclidean',
                              'hamming': 'hamming',
                              'jaccard': 'jaccard'}[metric]

    def fit(self, X):
        self._index = pynndescent.NNDescent(X,
                                            n_neighbors=self._n_neighbors,
                                            metric=self._pynnd_metric,
                                            low_memory=True,
                                            leaf_size=self._leaf_size,
                                            pruning_degree_multiplier=self._pruning_degree_multiplier,
                                            diversify_epsilon=self._diversify_epsilon,
                                            n_search_trees=self._n_search_trees,
                                            n_jobs=self._n_jobs)
        self._index._init_search_graph()

    def set_query_arguments(self, epsilon=0.1):
        self._epsilon = float(epsilon)

    def query(self, v, n):
        ind, dist = self._index.query(
            v.reshape(1, -1).astype('float32'), k=n,
            epsilon=self._epsilon)
        return ind[0]

    def __str__(self):
        str_template = (
            'PyNNDescent(n_neighbors=%d, pruning_mult=%.1f, diversify_epsilon=%.2f, epsilon=%.3f, leaf_size=%03d)')
        return str_template % (
        self._n_neighbors, self._pruning_degree_multiplier, self._diversify_epsilon,
        self._epsilon, self._leaf_size)


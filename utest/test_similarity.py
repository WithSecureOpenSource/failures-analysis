import numpy as np
import itertools

from failure_analysis.failure_analysis import jaccard_similarity, cosine_sim_vectors, score_failures


def test_jaccard_similarity():
    list1 = ["one", "two"]
    list2 = ["one", "two"]
    list3 = ["three", "four"]
    assert jaccard_similarity(list1, list2) == 1
    assert jaccard_similarity(list1, list3) == 0


def test_cosine_sim_vectors():
    vector1 = np.array([1, 1, 1])
    vector2 = np.array([1, 1, 1])
    assert cosine_sim_vectors(vector1, vector2) >= 1


def test_score_failures():
    failures = list(itertools.permutations(["i am failure 1", "i am failure 2", "i am failure 3", "i am failure 4"], 2))
    sm_ratios, coss, jaccards, jaros, levens = score_failures(failures)
    sum_sm = np.sum(sm_ratios)
    sum_coss = np.sum(coss)
    sum_jaccard = np.sum(jaccards)
    sum_jaros = np.sum(jaros)
    sum_levens = np.sum(levens)
    assert sum_sm > 0
    assert sum_coss > 0
    assert sum_jaccard > 0
    assert sum_jaros > 0
    assert sum_levens > 0

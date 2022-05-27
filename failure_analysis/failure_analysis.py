import argparse
import glob as glob
import itertools
import os
import sys
from difflib import SequenceMatcher
from pathlib import Path

import jellyfish
import Levenshtein  # type: ignore
import numpy as np
import pandas as pd  # type: ignore
from lxml import etree  # type: ignore
from sklearn.feature_extraction.text import CountVectorizer  # type: ignore
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore


def parse_xml(path):
    failure = []
    testname = []
    filename = []
    classname = []

    path = [f for f in glob.glob(path + "*.xml")]

    for xml in path:
        tree = etree.parse(xml)
        root = tree.getroot()
        if int(root.find("testsuite").attrib["failures"]) > 0:
            for node in root.findall(".//failure"):
                parent = node.getparent()
                # failure.append(node.attrib['message'])
                failure.append(node.text)
                testname.append(parent.attrib["name"])
                filename.append(os.path.basename(xml).lower())
                classname.append(parent.attrib["classname"])

    return failure, testname, filename, classname


def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    return float(len(s1.intersection(s2)) / len(s1.union(s2)))


def cosine_sim_vectors(vec1, vec2):
    """Takes in 2 vectors and returns a cosine similiarity between two vectors."""
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]


def score_failures(failures):
    """takes in a list of tuples of failures and returns 5 lists of 5 different string similiarity algorithms.

    sm_ratios, list of similiarity scores between two items in a tuple
    coss, a list of cosine similiarity scores between two items in a tuple
    jaccards, a list of jaccard scores between two items in a tuple
    jaros, a list of jaro scores between two items in a tuple
    levens, a list of levenshtein ratio scores between two items in a tuple
    """
    sm_ratios = []
    coss = []
    jaccards = []
    jaros = []
    levens = []

    for failure in failures:
        str1 = failure[0]
        str2 = failure[1]

        sm = SequenceMatcher(a=str1, b=str2)
        sm_ratios.append(sm.ratio())

        vectorizer = CountVectorizer().fit_transform([str1, str2])
        vectors = vectorizer.toarray()
        cos = cosine_sim_vectors(vectors[0], vectors[1])
        coss.append(cos)

        jaccard = jaccard_similarity(str1, str2)
        jaccards.append(jaccard)

        jaro = jellyfish.jaro_distance(str1, str2)
        jaros.append(jaro)

        leven = Levenshtein.ratio(str1, str2)
        levens.append(leven)

    return sm_ratios, coss, jaccards, jaros, levens


def main(path: str):

    failure, testname, filename, classname = parse_xml(path)

    testnames = list(itertools.permutations(testname, 2))
    failures = list(itertools.permutations(failure, 2))
    filenames = list(itertools.permutations(filename, 2))
    classnames = list(itertools.permutations(classname, 2))

    sm_ratios, coss, jaccards, jaros, levens = score_failures(failures)

    items = [
        filenames,
        testnames,
        classnames,
        sm_ratios,
        coss,
        jaccards,
        jaros,
        levens,
        failures,
    ]

    dfs = []
    for item in items:
        temp_df = pd.DataFrame(item)
        dfs.append(temp_df)
    df = pd.concat(dfs, axis=1)

    df.columns = [
        "filename1",
        "filename2",
        "testname1",
        "testname2",
        "suitename1",
        "suitename2",
        "sm_ratio",
        "cos",
        "jaccard",
        "jaro",
        "leven",
        "failure1",
        "failure2",
    ]
    df = df[["failure1", "suitename2", "testname2", "filename2", "cos", "leven"]]
    for failure in np.unique(df["failure1"].values):
        print("============== FAILURE START =================")
        print(failure)
        print("============== FAILURE END =================")
        temp = df[df["failure1"] == failure]
        temp = temp.sort_values("cos", ascending=True)
        temp = pd.pivot_table(temp, index=["suitename2", "testname2", "filename2"])
        print(temp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process xunit and group similar failures.')
    parser.add_argument("path", type=str,  help="Path to folder where xunit files are stored")
    args = parser.parse_args()
    main(args.path)

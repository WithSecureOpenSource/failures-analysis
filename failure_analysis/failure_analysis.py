from lxml import etree
import glob as glob
import os
import sys
import pandas as pd
import numpy as np
import itertools

from difflib import SequenceMatcher
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import Levenshtein
import jellyfish


def parseXMLs(path):
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


# JaccardSimiliarity
# takes in 2 lists and returns jaccard score of the two lists
def jaccardSimilarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    return float(len(s1.intersection(s2)) / len(s1.union(s2)))


# cosineSimVectors
# takes in 2 vectors and returns a cosine similiarity between two vectors
def cosineSimVectors(vec1, vec2):
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]


# scoreFailures
# takes in a list of tuples of failures and returns 5 lists of 5 different string similiarity algorithms
# sm_ratios, list of similiarity scores between two items in a tuple
# coss, a list of cosine similiarity scores between two items in a tuple
# jaccards, a list of jaccard scores between two items in a tuple
# jaros, a list of jaro scores between two items in a tuple
# levens, a list of levenshtein ratio scores between two items in a tuple


def scoreFailures(failures):
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
        cos = cosineSimVectors(vectors[0], vectors[1])
        coss.append(cos)

        jaccard = jaccardSimilarity(str1, str2)
        jaccards.append(jaccard)

        jaro = jellyfish.jaro_distance(str1, str2)
        jaros.append(jaro)

        leven = Levenshtein.ratio(str1, str2)
        levens.append(leven)

    return sm_ratios, coss, jaccards, jaros, levens


def main():
    path = sys.argv[1]

    failure, testname, filename, classname = parseXMLs(path)

    testnames = list(itertools.permutations(testname, 2))
    failures = list(itertools.permutations(failure, 2))
    filenames = list(itertools.permutations(filename, 2))
    classnames = list(itertools.permutations(classname, 2))

    sm_ratios, coss, jaccards, jaros, levens = scoreFailures(failures)

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
    # df = df.sort_values('cos',ascending = False)
    # df = pd.pivot_table(df,index=["failure1","testname2","classname2","filename2"])
    for failure in np.unique(df["failure1"].values):
        print("============== FAILURE START =================")
        print(failure)
        print("============== FAILURE END =================")
        temp = df[df["failure1"] == failure]
        temp = temp.sort_values("cos", ascending=True)
        temp = pd.pivot_table(temp, index=["suitename2", "testname2", "filename2"])
        print(temp)
    # print(df)


if __name__ == "__main__":
    main()

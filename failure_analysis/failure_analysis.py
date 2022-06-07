import argparse
import itertools
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd  # type: ignore
from lxml import etree  # type: ignore
from sklearn.feature_extraction.text import CountVectorizer  # type: ignore
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore


def parse_xml(path: Path):
    failure = []
    testname = []
    filename = []
    classname = []
    for xml in path.glob("**/*.xml"):
        if not xml.is_file():
            continue
        tree = etree.parse(xml)
        root = tree.getroot()
        if int(root.find("testsuite").attrib["failures"]) > 0:
            for node in root.findall(".//failure"):
                if node.text:
                    failure.append(node.text)
                else:
                    failure.append(node.attrib["message"])
                parent = node.getparent()
                testname.append(parent.attrib["name"])
                classname.append(parent.attrib["classname"])
                filename.append(os.path.basename(xml).lower())

    return failure, testname, filename, classname


def cosine_sim_vectors(vec1, vec2):
    """Takes in 2 vectors and returns a cosine similiarity between two vectors."""
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]


def score_failures(failures):
    """takes in a list of tuples of failures and returns a lists of cosine similarity.

    coss, a list of cosine similiarity scores between two items in a tuple
    """
    coss = []
    for failure in failures:
        str1 = failure[0]
        str2 = failure[1]
        vectorizer = CountVectorizer().fit_transform([str1, str2])
        vectors = vectorizer.toarray()
        cos = cosine_sim_vectors(vectors[0], vectors[1])
        coss.append(cos)
    return coss


def run(path: str):
    xml_path = Path(path)
    if not xml_path.is_dir():
        raise IOError(f"{path} should be directory but it was not.")
    failure, testname, filename, classname = parse_xml(xml_path)

    if len(failure) == 0:
        print("NO FAILURES FOUND")
        sys.exit(0)

    testnames = list(itertools.permutations(testname, 2))
    failures = list(itertools.permutations(failure, 2))
    filenames = list(itertools.permutations(filename, 2))
    classnames = list(itertools.permutations(classname, 2))
    coss = score_failures(failures)

    items = [
        filenames,
        testnames,
        classnames,
        coss,
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
        "cos",
        "failure1",
        "failure2",
    ]
    df = df[["failure1", "suitename2", "testname2", "filename2", "cos"]]
    for failure in np.unique(df["failure1"].values):
        print("============== FAILURE START =================")
        print(failure)
        print("============== FAILURE END =================")
        temp = df[df["failure1"] == failure]
        temp = temp.sort_values("cos", ascending=True)
        temp = pd.pivot_table(temp, index=["suitename2", "testname2", "filename2"])
        print(temp)


def main():
    parser = argparse.ArgumentParser(description="Process xunit and group similar failures from xunit failures.")
    parser.add_argument("path", type=str, help="Path to folder where xunit files are stored")
    args = parser.parse_args()
    path = args.path
    if not Path(path).is_dir():
        raise ValueError(f"{path} is not directory.")
    run(path)


if __name__ == "__main__":
    main()

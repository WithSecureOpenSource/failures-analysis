# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import argparse
import itertools
import os
import sys
from copy import deepcopy
from os.path import dirname
from pathlib import Path

import numpy as np
import pandas as pd  # type: ignore
from drain3 import TemplateMiner  # type: ignore
from drain3.template_miner_config import TemplateMinerConfig  # type: ignore
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
    """Takes in 2 vectors and returns a cosine similarity between two vectors."""
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]


def score_failures(failures: list):
    """takes in a list of tuples of failures and returns a lists of cosine similarity.

    coss, a list of cosine similarity scores between two items in a tuple
    """
    coss = []
    count_vectorizer = CountVectorizer()
    for failure in failures:
        vectorizer = count_vectorizer.fit_transform(failure)
        vectors = vectorizer.toarray()
        cos = cosine_sim_vectors(vectors[0], vectors[1])
        coss.append(cos)
    return coss


def template_failures(failures: list, drain_config: str) -> list:
    config = TemplateMinerConfig()
    if drain_config:
        config.load(drain_config)
    else:
        config.load(dirname(__file__) + "/drain3.ini")
    template_miner = TemplateMiner(config=config)
    return [template_miner.add_log_message(failure).get("template_mined") for failure in failures]


def run(path: str, min_threshold: float, drain_ini: str, drain_off: bool):
    xml_path = Path(path)
    if not xml_path.is_dir():
        raise IOError(f"{path} should be directory but it was not.")
    failure, testname, filename, classname = parse_xml(xml_path)
    failure_display = deepcopy(failure)
    if not drain_off:
        failure = template_failures(failure, drain_ini)

    if len(failure) == 0:
        print("NO FAILURES FOUND")
        sys.exit(0)

    testnames = list(itertools.combinations(testname, 2))
    failures = list(itertools.combinations(failure, 2))
    failure_display = itertools.combinations(failure_display, 2)
    failure_display = [fd[0] for fd in failure_display]
    filenames = list(itertools.combinations(filename, 2))
    classnames = list(itertools.combinations(classname, 2))
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
    df["failure_display"] = failure_display
    df = df[df["cos"] >= min_threshold]
    df = df[["failure1", "suitename2", "testname2", "filename2", "cos", "failure_display"]]
    for failure in np.unique(df["failure1"].values):
        print("============== FAILURE START =================")
        try:
            print(df.loc[df["failure1"] == failure, "failure_display"].iloc[0])
        except UnicodeEncodeError:
            print(
                df.loc[df["failure1"] == failure, "failure_display"].iloc[0].encode("ascii", "ignore").decode("utf - 8")
            )
        print("============== FAILURE END =================")
        temp = df[df["failure1"] == failure]
        temp = temp.sort_values("cos", ascending=True)
        temp = pd.pivot_table(temp, values=["cos"], index=["suitename2", "testname2", "filename2"])
        pd.set_option("display.max_rows", temp.shape[0] + 1)
        print(temp)


def main():
    parser = argparse.ArgumentParser(description="Process xunit and group similar failures from xunit failures.")
    parser.add_argument(
        "--min",
        "-M",
        type=int,
        help=(
            "Minimum threshold when failures are considered to be same. Default to 80, when Cos similarity is 0.80 "
            "or more error are considered to be same."
        ),
        default=0.80,
    )
    parser.add_argument(
        "--drain",
        "-D",
        type=str,
        help=(
            "Path to drain.ini file, which is used to configure Drain3 templating. "
            "If not given default templating will be used, unless --drain-off argument is given."
        ),
        default="",
    )
    parser.add_argument(
        "--drain-off",
        help="Turns drain templating off and will use error text as is. By default drain is enabled.",
        action="store_false",
        default=False,
    )
    parser.add_argument("path", type=str, help="Path to folder where xunit files are stored")
    args = parser.parse_args()
    path = args.path
    min_threshold = args.min
    drain_ini = args.drain
    drain_off = args.drain_off
    if not Path(path).is_dir():
        raise ValueError(f"{path} is not directory.")
    run(path, min_threshold, drain_ini, drain_off)


if __name__ == "__main__":
    main()

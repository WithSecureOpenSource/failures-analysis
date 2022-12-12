# Failure analysis

[![Version](https://img.shields.io/pypi/v/failures-analysis.svg)](https://pypi.org/project/failures-analysis/)
[![Actions Status](https://github.com/F-Secure/failures-analysis/workflows/CICD/badge.svg)](https://github.com/F-Secure/failures-analysis/actions)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<center><img src="https://github.com/F-Secure/failures-analysis/raw/main/docs/images/Failures-analysis.png" width="120px" height="120px"/></center>

Tests failure analysis package provides fast and reliable way to find and group similar failures in your CI/CD
pipeline. When failure grouping and similarity scoring is done automatically by a machine, it will free
resources from development team member to fix the most important failures in their CI/CD pipeline. It is tedious
work for a human to download, open and read all the test failures and analyze which failures belong to the same group.
The failure-analysis package solves this problem by processing xunit xml files and failures found within by calculating the similarity score of failures using cosine similarity. 

Results of this approach are to be published in Springer Book Series: Advances in Intelligent Systems and Computing
later (link to be provided once published). 

# Installation instructions

Only Python 3.8 or newer is supported.

1. Update pip `pip install -U pip` to ensure latest version is used
2. Install from the commandline: `pip install failures-analysis`

# Usage
To be able to find similar failures, users need to download xunit result(s) in to folder. How and where the download of
the xunit files is done, is not part of this project, but example
[flaky-test CI](https://github.com/F-Secure/flaky-test-ci/blob/main/download_artifacts.py) has an example
how download from GitHub can be performed. Tool can be used from command line and it needs only one argument:
path to folder where xunit xml files are located, example: 
`failures-analysis path/to/xunit/files`

# Supported xunit formats
Package has been tested with Pytest and Robot Framework xunit output files. Other format might be supported,
but because we do not have visibility on those formats, those are not listed.

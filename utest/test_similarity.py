import shutil
import tempfile
from pathlib import Path

import numpy as np
import itertools

import pytest
from approvaltests import verify  # type: ignore

from failure_analysis.failure_analysis import cosine_sim_vectors, score_failures, run

UTEST_ROOT = Path(__file__).resolve().parent
XUNIT_FILES_DIR = UTEST_ROOT / "resources"
PASS_01_FILE_NAME = "pass_01_.xml"
FAIL_01_FILE_NAME = "failing_01_.xml"
FAIL_02_FILE_NAME = "failing_02_.xml"
PASS_01_FILE_PATH = XUNIT_FILES_DIR / PASS_01_FILE_NAME
FAIL_01_FILE_PATH = XUNIT_FILES_DIR / FAIL_01_FILE_NAME
FAIL_02_FILE_PATH = XUNIT_FILES_DIR / FAIL_02_FILE_NAME
MIN_THRESHOLD = 0.80


def test_cosine_sim_vectors():
    vector1 = np.array([1, 1, 1])
    vector2 = np.array([1, 1, 1])
    assert cosine_sim_vectors(vector1, vector2) >= 1


def test_score_failures():
    failures = list(itertools.permutations(["i am failure 1", "i am failure 2", "i am failure 3", "i am failure 4"], 2))
    coss = score_failures(failures)
    sum_coss = np.sum(coss)
    assert sum_coss > 0


def test_invalid_path():
    with pytest.raises(IOError):
        run("not/here", MIN_THRESHOLD)


def test_console_output(capsys):
    run(str(XUNIT_FILES_DIR), MIN_THRESHOLD)
    captured = capsys.readouterr()
    verify(captured.out)


def test_no_failures(capsys):
    with pytest.raises(SystemExit):
        with tempfile.TemporaryDirectory() as temp_folder:
            shutil.copy(PASS_01_FILE_PATH, Path(temp_folder) / PASS_01_FILE_NAME)
            run(temp_folder, MIN_THRESHOLD)
            captured = capsys.readouterr()
            assert captured.out == "NO FAILURES FOUND"

    with pytest.raises(SystemExit):
        with tempfile.TemporaryDirectory() as temp_folder:
            run(temp_folder, MIN_THRESHOLD)
            captured = capsys.readouterr()
            assert captured.out == "NO FAILURES FOUND"


def test_finding_files(capsys):
    with tempfile.TemporaryDirectory() as temp_folder:
        folder_match_filter_patters = Path(temp_folder) / "xmlxml"
        folder_match_filter_patters.mkdir(parents=True)
        shutil.copy(PASS_01_FILE_PATH, folder_match_filter_patters / PASS_01_FILE_NAME)
        shutil.copy(FAIL_01_FILE_PATH, folder_match_filter_patters / FAIL_01_FILE_NAME)
        shutil.copy(FAIL_02_FILE_PATH, folder_match_filter_patters / FAIL_02_FILE_NAME)
        run(temp_folder, MIN_THRESHOLD)
        captured = capsys.readouterr()
        verify(captured.out)

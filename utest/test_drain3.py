from pathlib import Path

from approvaltests import verify  # type: ignore

from failure_analysis.failure_analysis import template_failures

UTEST_ROOT = Path(__file__).resolve().parent
XUNIT_FILES_DIR = UTEST_ROOT / "resources"


def test_template_failures():
    failures = [
        "def test_02():\n>       assert 'connected to 192.168.0.1' == 'connected to 192.0.0.0'\nE       assert False\n\n\ntests\\test_me.py:6: AssertionError",
        "def test_02():\n>       assert 'connected to 192.168.0.2' == 'connected to 192.0.0.0'\nE       assert False\n\n\ntests\\test_me.py:6: AssertionError",
        "def test_02():\n>       assert 'connected to 192.168.0.3' == 'connected to 192.0.0.0'\nE       assert False\n\n\ntests\\test_me.py:6: AssertionError",
    ]
    verify(template_failures(failures, ""))


def test_custom_ini(tmp_path):
    failures = [
        "def test_02():\n>       assert 'connected to 192.168.0.1' == 'connected to 192.0.0.0'\nE       assert False\n\n\ntests\\test_me.py:6: AssertionError",
    ]
    drain3_ini = XUNIT_FILES_DIR / "drain3.ini"
    drain3_ini = drain3_ini.resolve()
    assert drain3_ini.is_file()
    verify(template_failures(failures, str(drain3_ini)))

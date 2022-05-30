import os
import shutil
import sys
from pathlib import Path

from invoke import task

IN_CI = os.getenv("GITHUB_WORKFLOW")
ROOT_DIR = Path(".").resolve()
UTEST_DIR = ROOT_DIR / "utest"


@task
def lint(ctx):
    print("=" * 20, "isort")
    ctx.run("isort failure_analysis")
    print("=" * 20, "black")

    black_cmd = ["black", "--config", "pyproject.toml", "utest", "failure_analysis", "tasks.py"]
    if IN_CI:
        black_cmd.insert(1, "--check")
        black_cmd.insert(2, "--diff")
    ctx.run(" ".join(black_cmd))
    print("=" * 20, "flake8")
    ctx.run("flake8 utest failure_analysis")
    print("=" * 20, "mypy")
    ctx.run("mypy --show-error-codes utest failure_analysis")
    print("=" * 20)


@task
def test(ctx):
    ctx.run("pytest --showlocals --tb=long utest")


def _log_error(function, path, excinfo):
    if Path(path).exists():
        print(f"On function: '{function}' and with path: '{path}'")
        print(f"Got error:\n{excinfo}")
        sys.exit(1)


@task
def clean(ctx):
    shutil.rmtree(ROOT_DIR / ".pytest_cache", onerror=_log_error)
    shutil.rmtree(UTEST_DIR / ".pytest_cache", onerror=_log_error)
    shutil.rmtree(ROOT_DIR / "dist", onerror=_log_error)


@task
def release(ctx):
    ctx.run("semantic-release publish -v DEBUG")

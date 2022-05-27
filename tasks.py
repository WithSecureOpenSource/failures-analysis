import os

from invoke import task

IN_CI = os.getenv("GITHUB_WORKFLOW")


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

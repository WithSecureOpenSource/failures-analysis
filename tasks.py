from invoke import task


@task
def lint(ctx):
    print("=" * 20, "isort")
    ctx.run("isort failure_analysis")
    print("=" * 20, "black")
    ctx.run("black --config pyproject.toml utest failure_analysis")
    print("=" * 20, "flake8")
    ctx.run("flake8 utest failure_analysis")
    print("=" * 20, "mypy")
    ctx.run("mypy --show-error-codes utest failure_analysis")
    print("=" * 20)


@task
def test(ctx):
    ctx.run("pytest --showlocals --tb=long utest")

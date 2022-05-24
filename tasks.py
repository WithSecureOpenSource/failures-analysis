from invoke import task


@task
def lint(ctx):
    ctx.run("mypy --show-error-codes utest failure_analysis")
    ctx.run("isort failure_analysis")
    ctx.run("black --config pyproject.toml utest failure_analysis")

from invoke import task

@task
def start(ctx):
    ctx.run("uvicorn app.main:app --reload")

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest app")

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html")

@task(coverage_report)
def coverage_view(ctx):
    ctx.run('firefox htmlcov/index.html')

@task
def test(ctx):
    ctx.run("pytest app")

@task
def flake(ctx):
    ctx.run("flake8 app")

@task
def black(ctx):
    ctx.run("black app")

@task
def mypy(ctx):
    ctx.run("mypy app")
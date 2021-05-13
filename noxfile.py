import nox

nox.options.sessions = "lint", "format"
locations = ["foodscope"]


@nox.session
def tests(session):
    args = session.posargs or locations
    session.install("-r", "requirements.txt")
    session.run("pytest", *args)


@nox.session
def lint(session):
    args = session.posargs or locations
    session.install("flake8")
    session.run("flake8", *args)


@nox.session
def format(session):
    black(session)
    isort(session)


def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


def isort(session):
    args = session.posargs or locations
    session.install("isort")
    session.run("isort", "--profile", "black", *args)

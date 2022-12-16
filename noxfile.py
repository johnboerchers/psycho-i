import nox


@nox.session(python="3.10")
def tests(session: nox.Session) -> None:
    """
    Run the unit and regular tests.
    """
    session.install(".[test]")
    session.run("pytest")


@nox.session(python="3.10")
def docs(session: nox.Session) -> None:
    """
    Build the docs. Pass "--serve" to serve.
    """

    session.install(".[docs]")
    session.chdir("docs")
    session.run("sphinx-build", "-M", "html", ".", "_build")


@nox.session(python="3.10")
def serve(session: nox.Session) -> None:
    docs(session)
    print("Launching docs at http://localhost:8000/ - use Ctrl-C to quit")
    session.run("python", "-m", "http.server", "8000", "-d", "_build/html")

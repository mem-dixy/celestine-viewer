""""""


import pathlib
from celestine import load
from celestine.data.directory import (
    APPLICATION,
    INTERFACE,
    LANGUAGE,
)
from celestine.package import Package
from celestine.typed import (
    LS,
    B,
    H,
    Hold,
)

from .magic import Magic


def begin_session(argument_list: LS, exit_on_error: B) -> H:
    """"""

    magic = Magic(argument_list, exit_on_error)

    with magic:
        magic.parse(LANGUAGE)
        magic.parse(INTERFACE)
        magic.parse(APPLICATION)

        session1 = load.method("Session", "session", "session")
        session2 = load.method(
            "Session", APPLICATION, magic.core.application.name
        )
        session3 = load.method("Information", "session", "session")

        magic.get_parser([session1, session2, session3], False)

    # Save values to session object.
    application = magic.core.application.name
    session = Hold()

    session.application = load.module(APPLICATION, session1.application)

    session.attribute = session2

    session.interface = load.module(INTERFACE, session1.interface)

    session.language = load.module(LANGUAGE, session1.language)

    session.package = Package(session)

    session.window = None

    # items = load.python(APPLICATION, application)
    # car = list(items)

    view = load.module(APPLICATION, application, "view")

    code = load.module(APPLICATION, application, "code")

    session.code = load.functions(code)
    one = load.decorators(view, "scene")
    two = load.decorators(view, "main")
    session.view = one | two

    main = load.decorator_name(view, "main")
    session.main = session1.main if session1.main else main
    return session


"""
importer notes.

language.py is all you need for 1 language.
language/__init__.py can be used instead.

Not recomended to use both. However, note that
language/__init__.py takes priority over language.py

Must have at least one of these.
Recomend using directory version so you can add more languages.
Error messages will assume this version.

if you have more then 1 language you must use language/__init__.py
"""

"""Configuration information will show your saved stuff."""

""""""

import importlib
import re

from celestine import (
    bank,
    load,
)
from celestine.literal import (
    APPLICATION,
    CELESTINE,
    FULL_STOP,
    INTERFACE,
    LANGUAGE,
    PACKAGE,
)
from celestine.typed import (
    LS,
    A,
    B,
    C,
    D,
    N,
    R,
    S,
)
from celestine.window.collection import Dictionary

from . import default
from .magic import Magic

this = load.module(PACKAGE)

type Decorator = D[S, C[..., A]]


def decorators(*path: S) -> D[S, Decorator]:
    """Load all decorated functions from all modules found in path."""
    result: D[S, Decorator] = {}

    pattern = re.compile(r"<function (\w+)\.")

    base = FULL_STOP.join(path)
    walked = load.walk_package(base)
    for _module in walked:
        items = vars(_module).items()

        for key, value in items:
            match = pattern.match(repr(value))

            if not match:
                continue

            name = match[1]

            if name not in result:
                result[name] = {}

            item = FULL_STOP.join((base, key))
            result[name][item] = value

    return result


def set_lang():
    """"""
    # monkeypatch in the language
    language = load.package(CELESTINE, LANGUAGE)
    for key, value in vars(bank.language).items():
        setattr(language, key, value)


def begin_session(argument_list: LS, exit_on_error: B, **star: R) -> A:
    """
    First load Language so human can read errors.

    Then load Interface so human see errors the way they want.
    """

    bank.configuration = load.instance(
        "session",
        "configuration",
        "Configuration",
    )

    # The order here matters.
    bank.language = load.module(LANGUAGE, default.language())
    set_lang()
    bank.interface = load.module(INTERFACE, default.interface())
    hold = default.application()
    bank.application = load.module(APPLICATION, default.application())
    setattr(bank.application, "name", hold)

    magic = Magic(argument_list, exit_on_error)

    with magic:
        magic.parse(LANGUAGE)
        set_lang()
        magic.parse(INTERFACE)
        magic.parse(APPLICATION)

        method = load.method("Configuration", "session", "session")
        magic.get_parser([method], True)
        path = method.configuration
        bank.configuration.load(path)

        magic.parse(LANGUAGE)
        set_lang()
        magic.parse(INTERFACE)
        magic.parse(APPLICATION)

        session = importlib.import_module("celestine.session.session")
        importlib.reload(session)

        session1 = load.method("Session", "session", "session")
        name = bank.application.name
        session2 = load.method("Session", APPLICATION, name)
        session3 = load.method("Information", "session", "session")

        magic.get_parser([session1, session2, session3], False)

    # Save values to session object.
    bank.application = load.module(APPLICATION, session1.application)
    bank.attribute = session2
    bank.directory = session1.directory
    bank.interface = load.module(INTERFACE, session1.interface)
    bank.window = bank.interface.Window(**star)

    set_lang()

    return bank.window, bank.application.name


def begin_main(argument_list: LS, exit_on_error: B, **star: R) -> N:
    """"""
    window, application = begin_session(
        argument_list,
        exit_on_error,
        **star,
    )

    decorator = decorators(CELESTINE, APPLICATION, application)
    call = decorator.get("call", {})
    draw = decorator.get("draw", {})
    main = decorator.get("main", {})
    draw |= main

    def find_main() -> S:
        """Finds @main or 'def main' or any @draw."""
        try:
            return next(iter(main))
        except StopIteration:
            pass

        for key in draw:
            if "main" in key:
                return key

        try:
            return next(iter(draw))
        except StopIteration:
            pass

        raise Warning("There is nothing to draw.")

    window.main = find_main()

    _code: Decorator = {}
    _view: Decorator = {}

    for name, function in call.items():
        _code[name] = function

    for name, function in draw.items():
        view = window.drop(name)
        function(view)
        _view[name] = view

    # TODO init this better?
    window.code = Dictionary(_code)
    window.view = Dictionary(_view)
    window.run()

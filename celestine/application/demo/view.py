""""""


from celestine.session.session import Session
from celestine.typed import N
from celestine.window.container import Container as View


def one(this: Session, view: View) -> N:
    """"""
    language = view.this.language
    with view.span("one_head") as line:
        line.label("one_title", language.DEMO_ONE_TITLE)
        line.call("one_action", "Feed Cow", "cow", say="I eat you.")
    with view.span("one_body") as line:
        line.view("one_past", language.DEMO_ONE_PAST, "main")
        line.view("one_next", language.DEMO_ONE_NEXT, "two")


def two(this: Session, view: View) -> N:
    """"""
    language = view.this.language
    with view.span("two_head") as line:
        line.label("two_title", language.DEMO_TWO_TITLE)
        line.call("two_action", "Wave Cow", "cow", say="Good Bye!")
    with view.span("two_body") as line:
        line.view("two_past", language.DEMO_TWO_PAST, "one")
        line.view("two_next", language.DEMO_TWO_NEXT, "main")


def main(this: Session, view: View) -> N:
    """"""
    language = view.this.language
    with view.span("main_head") as line:
        line.label("main_title", language.DEMO_MAIN_TITLE)
        line.call("main_action", "Greet Cow", "cow", say="Hello!")
    with view.span("main_body") as line:
        line.view("main_past", language.DEMO_MAIN_PAST, "one")
        line.view("main_next", language.DEMO_MAIN_NEXT, "two")

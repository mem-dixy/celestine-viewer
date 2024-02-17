""""""

from collections.abc import Collection

from celestine.typed import (
    GF,
    A,
    B,
    D,
    F,
    G,
    H,
    I,
    K,
    N,
    R,
    S,
    T,
)
from celestine.unicode import NONE


class Point:
    """"""

    one: F
    two: F

    @classmethod
    def clone(cls, self: K) -> K:
        """"""
        return cls(self.one, self.two)

    def copy(self) -> K:
        """"""
        return self.clone(self)

    @property
    def float(self) -> T[F, F]:
        return (self.one, self.two)

    @property
    def int(self) -> T[I, I]:
        return tuple(map(round, self.float))

    def __init__(self, one: F, two: F) -> N:
        self.one = float(one)
        self.two = float(two)

    def __iter__(self) -> GF:
        yield self.one
        yield self.two

    def __repr__(self) -> S:
        return f"Point({self.one}, {self.two})"

    def __str__(self) -> S:
        return f"({self.one}, {self.two})"

    def __sub__(self, other: K) -> K:
        one = self.one - other.one
        two = self.two - other.two
        return type(self)(one, two)

    def __truediv__(self, other: K) -> K:
        one = self.one / other.one
        two = self.two / other.two
        return type(self)(one, two)


class Line:
    """"""

    minimum: F
    maximum: F

    @classmethod
    def clone(cls, self: K) -> K:
        """"""
        return cls(self.minimum, self.maximum)

    def copy(self) -> K:
        """"""
        return self.clone(self)

    @property
    def length(self) -> F:
        return self.maximum - self.minimum

    @property
    def midpoint(self) -> F:
        return (self.minimum + self.maximum) / 2

    @property
    def float(self) -> T[F, F]:
        return (self.minimum, self.maximum)

    @property
    def int(self) -> T[I, I]:
        return tuple(map(round, self.float))

    def __add__(self, other: F) -> K:
        one = self.minimum + other
        two = self.maximum + other
        return type(self)(one, two)

    def __contains__(self, item: F) -> B:
        return self.minimum <= item <= self.maximum

    def __iadd__(self, other: F) -> K:
        self.minimum += other
        self.maximum += other
        return self

    def __imul__(self, other: F) -> K:
        self.minimum *= other
        self.maximum *= other
        return self

    def __init__(self, minimum: F, maximum: F) -> N:
        self.minimum = float(min(minimum, maximum))
        self.maximum = float(max(minimum, maximum))

    def __mul__(self, other: F) -> K:
        one = self.minimum * other
        two = self.maximum * other
        return type(self)(one, two)

    def __repr__(self) -> S:
        return f"Line({self.minimum}, {self.maximum})"

    def __str__(self) -> S:
        return f"[{self.minimum}, {self.maximum}]"


class Plane:
    """"""

    one: Line
    two: Line

    def center(self, other: K) -> N:
        self += other.centroid - self.centroid

    @property
    def centroid(self) -> Point:
        one = self.one.midpoint
        two = self.two.midpoint
        return Point(one, two)

    @classmethod
    def clone(cls, self: K) -> K:
        """"""
        one = self.one.copy()
        two = self.two.copy()
        return cls(one, two)

    def copy(self) -> K:
        """"""
        return self.clone(self)

    @property
    def float(self) -> T[F, F, F, F]:
        xmin = self.one.minimum
        ymin = self.two.minimum
        xmax = self.one.maximum
        ymax = self.two.maximum
        return (xmin, ymin, xmax, ymax)

    @property
    def int(self) -> T[I, I, I, I]:
        return tuple(map(round, self.float))

    @classmethod
    def make(cls, width: F, height: F) -> K:
        """"""
        one = Line(0, width)
        two = Line(0, height)
        return cls(one, two)

    @property
    def origin(self) -> Point:
        """"""
        return Point(self.one.minimum, self.two.minimum)

    def scale_to_max(self, other: K) -> K:
        self *= max(other.size / self.size)
        return self

    def scale_to_min(self, other: K) -> K:
        self *= min(other.size / self.size)
        return self

    @property
    def size(self) -> Point:
        return Point(self.one.length, self.two.length)

    def __add__(self, other: Point) -> K:
        one = self.one + other.one
        two = self.two + other.two
        return type(self)(one, two)

    def __contains__(self, item: Point) -> B:
        one = item.one in self.one
        two = item.two in self.two
        return one and two

    def __iadd__(self, other: Point) -> K:
        self.one += other.one
        self.two += other.two
        return self

    def __imul__(self, other: F) -> K:
        self.one *= other
        self.two *= other
        return self

    def __init__(self, one: Line, two: Line) -> N:
        self.one = one.copy()
        self.two = two.copy()

    def __mul__(self, other: F) -> K:
        one = self.one * other
        two = self.two * other
        return type(self)(one, two)

    def __repr__(self) -> S:
        one = repr(self.one)
        two = repr(self.two)
        return f"Plane({one}, {two})"

    def __str__(self) -> S:
        one = str(self.one)
        two = str(self.two)
        return f"({one}, {two})"


class Object:
    """"""

    @classmethod
    def clone(cls, self: K) -> K:
        """"""
        return cls()

    def copy(self) -> K:
        """"""
        return self.clone(self)

    def __init__(self, **star: R) -> N:
        """This does not pass the star parameter to the real object."""
        super().__init__()


class Abstract(Object):
    """"""

    keep: A  # The object that the window system interacts with.
    parent: K

    area: Plane
    canvas: A
    hidden: B
    hold: H
    name: S  # The key to use to find this in the window dictionary.

    def click(self, point: Point) -> B:
        """"""
        if self.hidden:
            return False

        if point not in self.area:
            return False

        if self.action:
            self.hold.queue(self.action, self.argument, self.star)

        return True

    def draw(self, **star: R) -> N:
        """"""
        if self.hidden:
            return

    def hide(self) -> N:
        """"""
        self.hidden = True

    def make(self, canvas: A, **star: R) -> B:
        """"""
        self.canvas = canvas
        return True

    def show(self) -> N:
        """"""
        self.hidden = False

    def spot(self, area: Plane) -> N:
        """"""
        self.area = area

    def __init__(self, hold: H, name: S, parent: K, **star: R) -> N:
        super().__init__(**star)
        self.parent = parent
        self.area = Plane.make(0, 0)
        self.canvas = None
        self.hidden = False
        self.hold = hold
        self.name = name
        self.keep = None

        self.navigate = star.pop("navigate", NONE)
        # The page to turn to when clicked.

        self.action = star.pop("action", NONE)
        # The action to perform when the user triggers the button.

        self.argument = star.pop("argument", NONE)
        # The data to send when the action is called.

        self.text = star.pop("text", NONE)
        # Text that describes the purpose of the button's action.

        self.star = star
        # Contains all remaining keyword arguments.


class Tree(Object, Collection):
    """"""

    children: D[S, K]

    def get(self, name: S) -> K:
        """"""
        return self.children[name]

    def set(self, item: K) -> K:
        """"""
        self.children[item.name] = item
        return item

    def __bool__(self) -> B:
        return True

    def __contains__(self, item: S) -> B:
        return item in self.children

    def __init__(self, **star: R) -> N:
        self.children = {}
        super().__init__(**star)

    def __iter__(self) -> G[T[S, K], N, N]:
        yield from self.children.items()

    def __len__(self) -> I:
        return len(self.children)

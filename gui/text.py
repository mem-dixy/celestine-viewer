#from mem_dixy.tag.alphabet import convert
#from mem_dixy.tag.alphabet import tag
#from mem_dixy.tag.alphabet import hashy
#from mem_dixy.tag.alphabet import space
from mem_dixy.tag.alphabet import *

from enum import Enum


class State(Enum):
    NONE = 1
    TAG = 2
    HASH = 3
    SPACE = 3
    SYMBOL = 4


#string = input("you ugly")
string = "-🌋 Volcano🏕️ Camping🏜️ Desert !!||?#$&& pie"


falcon = []
falcon.append("[")

for character in string:
    falcon.append(convert.get(character, str()))

falcon.append("]")
bird = str().join(falcon)

tigger = []
token = []

state_now = State.NONE
state_past = State.NONE


class Atoken:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


print(VERTICAL_LINE)
print(EXCLAMATION_MARK)
print(AMPERSAND)


print(AMPERSAND in sql_and)
print(EXCLAMATION_MARK)
print(AMPERSAND)


class AND(Atoken):
    def __init__(self, value):
        super().__init__(AMPERSAND)


class IS(Atoken):
    def __init__(self, value):
        super().__init__(PLUS_SIGN)


class NOT(Atoken):
    def __init__(self, value):
        super().__init__(HYPHEN_MINUS)


class OR(Atoken):
    def __init__(self, value):
        super().__init__(VERTICAL_LINE)


class Atag(Atoken):
    def __init__(self, value):
        super().__init__(value)


class Asymbol(Atoken):
    def __init__(self, value):
        super().__init__("&")


def add_token():
    global tigger
    global token
    value = str().join(tigger)
    cat = Atag(value)
    token.append(cat)
    tigger = []


for character in bird:

    if character in tag:
        state_now = State.TAG

    elif character in number:
        state_now = State.HASH

    elif character in space:
        state_now = State.SPACE

    elif character in logica_operator:
        state_now = State.SYMBOL

    else:
        state_now = State.NONE

    if state_past is not state_now:
        add_token()

    tigger.append(character)
    state_past = state_now

print(string)
print(bird)
print(tigger)
print(token)

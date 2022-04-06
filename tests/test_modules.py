from modules.symbolic import Constant
from modules.symbolic import DuoFunc
from modules.symbolic import Variable


def test_duo_tree():
    root = DuoFunc("**")
    root.add_left(Constant(2))
    root.add_right(Variable("x"))
    result = root.evaluate({"x": 7})
    assert result == 128

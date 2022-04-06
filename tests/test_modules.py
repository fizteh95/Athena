import math  # noqa: F401

import pytest

from modules.symbolic import Constant
from modules.symbolic import DuoFunc
from modules.symbolic import UnoFunc
from modules.symbolic import Variable


def test_duo_tree():
    root = DuoFunc("**")
    root.add_left(Constant(2))
    root.add_right(Variable("x"))
    result = root.evaluate({"x": 7})
    assert result == 128


def test_central_child():
    root = UnoFunc("math.sqrt")
    root.add_central(Variable("x"))
    result = root.evaluate({"x": 4})
    assert result == 2


def test_incorrect_tree_no_childs():
    root = DuoFunc("*")
    with pytest.raises(Exception):
        root.evaluate({"x": 4})


def test_incorrect_tree_double_central():
    root = DuoFunc("*")
    root.add_central(Variable("x"))
    with pytest.raises(Exception):
        root.add_central(Variable("x"))


def test_incorrect_tree_double_left():
    root = DuoFunc("*")
    root.add_left(Variable("x"))
    with pytest.raises(Exception):
        root.add_left(Variable("x"))


def test_incorrect_tree_double_right():
    root = DuoFunc("*")
    root.add_right(Variable("x"))
    with pytest.raises(Exception):
        root.add_right(Variable("x"))


def test_remove_left_correct():
    root = DuoFunc("*")
    root.add_left(Constant(2))
    root.remove_left()
    assert root.left_children is None


def test_remove_left_wrong():
    root = DuoFunc("*")
    with pytest.raises(Exception):
        root.remove_left()


def test_remove_right_correct():
    root = DuoFunc("*")
    root.add_right(Constant(2))
    root.remove_right()
    assert root.right_children is None


def test_remove_right_wrong():
    root = DuoFunc("*")
    with pytest.raises(Exception):
        root.remove_right()


def test_remove_central_correct():
    root = DuoFunc("*")
    root.add_central(Constant(2))
    root.remove_central()
    assert root.central_children is None


def test_remove_central_wrong():
    root = DuoFunc("*")
    with pytest.raises(Exception):
        root.remove_central()


def test_wrong_unofunc_compute():
    root = UnoFunc("*")
    with pytest.raises(Exception):
        root.compute({})


def test_wrong_duofunc_compute():
    root = DuoFunc("*")
    with pytest.raises(Exception):
        root.compute({})

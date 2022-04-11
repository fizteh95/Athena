import math  # noqa: F401

import pytest

from modules.symbolic import Constant
from modules.symbolic import DuoFunc
from modules.symbolic import UnoFunc
from modules.symbolic import Variable


def test_duo_tree() -> None:
    root = DuoFunc("**")
    root.add_left(Constant(2))
    root.add_right(Variable("x"))
    result = root.evaluate({"x": 7})
    assert result == 128


def test_central_child() -> None:
    root = UnoFunc("math.sqrt")
    root.add_central(Variable("x"))
    result = root.evaluate({"x": 4})
    assert result == 2


def test_incorrect_tree_no_childs() -> None:
    root = DuoFunc("*")
    with pytest.raises(Exception):
        root.evaluate({"x": 4})


def test_incorrect_tree_double_left() -> None:
    root = DuoFunc("*")
    root.add_left(Variable("x"))
    with pytest.raises(Exception):
        root.add_left(Variable("x"))


def test_incorrect_tree_double_right() -> None:
    root = DuoFunc("*")
    root.add_right(Variable("x"))
    with pytest.raises(Exception):
        root.add_right(Variable("x"))


def test_remove_left_correct() -> None:
    root = DuoFunc("*")
    root.add_left(Constant(2))
    root.remove_left()
    assert root.left_children is None


def test_remove_left_wrong() -> None:
    root = DuoFunc("*")
    with pytest.raises(Exception):
        root.remove_left()


def test_remove_right_correct() -> None:
    root = DuoFunc("*")
    root.add_right(Constant(2))
    root.remove_right()
    assert root.right_children is None


def test_remove_right_wrong() -> None:
    root = DuoFunc("*")
    with pytest.raises(Exception):
        root.remove_right()


def test_remove_central_correct() -> None:
    root = UnoFunc("*")
    root.add_central(Constant(2))
    root.remove_central()
    assert root.central_children is None


def test_remove_central_wrong() -> None:
    root = UnoFunc("*")
    with pytest.raises(Exception):
        root.remove_central()


def test_wrong_unofunc_compute() -> None:
    root = UnoFunc("*")
    with pytest.raises(Exception):
        root.evaluate({"x": 5})


def test_wrong_duofunc_compute() -> None:
    root = DuoFunc("*")
    with pytest.raises(Exception):
        root.evaluate({"x": 5})


def test_wrong_unofunc_right_children() -> None:
    root = UnoFunc("*")
    with pytest.raises(Exception):
        root.add_right(Constant(2))


def test_wrong_unofunc_left_children() -> None:
    root = UnoFunc("*")
    with pytest.raises(Exception):
        root.add_left(Constant(2))


def test_wrong_duofunc_central_children() -> None:
    root = DuoFunc("*")
    with pytest.raises(Exception):
        root.add_central(Constant(2))


def test_complex_tree() -> None:
    root = DuoFunc("*")
    left_branch = DuoFunc("+")
    left_branch.add_left(Constant(2))
    left_branch_right_branch = DuoFunc("**")
    left_branch_right_branch.add_left(Constant(3))
    left_branch_right_branch.add_right(Variable("x"))
    left_branch.add_right(left_branch_right_branch)
    root.add_left(left_branch)
    right_branch = UnoFunc("math.sqrt")
    right_branch.add_central(Variable("y"))
    root.add_right(right_branch)
    result = root.evaluate({"x": 3, "y": 4})
    assert result == 58

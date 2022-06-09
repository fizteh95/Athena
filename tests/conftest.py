import typing as t

import pytest

from modules import symbolic as sym


@pytest.fixture
def complex_tree() -> t.Any:
    root = sym.DuoFunc("*")
    left_branch = sym.DuoFunc("+")
    left_branch.add_left(sym.Constant(2))
    left_branch_right_branch = sym.DuoFunc("**")
    left_branch_right_branch.add_left(sym.Constant(3))
    left_branch_right_branch.add_right(sym.Variable("x"))
    left_branch.add_right(left_branch_right_branch)
    root.add_left(left_branch)
    right_branch = sym.UnoFunc("math.sqrt")
    right_branch.add_central(sym.Variable("y"))
    root.add_right(right_branch)
    return root

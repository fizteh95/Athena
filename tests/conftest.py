import typing as t

import pytest

from modules.symbolic import Constant
from modules.symbolic import DuoFunc
from modules.symbolic import UnoFunc
from modules.symbolic import Variable


@pytest.fixture
def complex_tree() -> t.Any:
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
    return root

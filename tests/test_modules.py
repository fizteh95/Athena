import math  # noqa: F401
import typing as t

import pytest

import modules.symbolic as sym
from modules import NN_stand
from modules.symbolic_genome import GenomeEvolution
from modules.symbolic_genome import Population


def test_duo_tree() -> None:
    root = sym.DuoFunc("**")
    root.add_left(sym.Constant(2))
    root.add_right(sym.Variable("x"))
    result = root.evaluate({"x": 7})
    assert result == 128


def test_central_child() -> None:
    root = sym.UnoFunc("math.sqrt")
    root.add_central(sym.Variable("x"))
    result = root.evaluate({"x": 4})
    assert result == 2


def test_incorrect_tree_no_childs() -> None:
    root = sym.DuoFunc("*")
    with pytest.raises(Exception):
        root.evaluate({"x": 4})


def test_incorrect_tree_double_left() -> None:
    root = sym.DuoFunc("*")
    root.add_left(sym.Variable("x"))
    with pytest.raises(Exception):
        root.add_left(sym.Variable("x"))


def test_incorrect_tree_double_right() -> None:
    root = sym.DuoFunc("*")
    root.add_right(sym.Variable("x"))
    with pytest.raises(Exception):
        root.add_right(sym.Variable("x"))


def test_remove_left_correct() -> None:
    root = sym.DuoFunc("*")
    root.add_left(sym.Constant(2))
    root.remove_left()
    assert root.left_child is None


def test_remove_left_wrong() -> None:
    root = sym.DuoFunc("*")
    with pytest.raises(Exception):
        root.remove_left()


def test_remove_right_correct() -> None:
    root = sym.DuoFunc("*")
    root.add_right(sym.Constant(2))
    root.remove_right()
    assert root.right_child is None


def test_remove_right_wrong() -> None:
    root = sym.DuoFunc("*")
    with pytest.raises(Exception):
        root.remove_right()


def test_remove_central_correct() -> None:
    root = sym.UnoFunc("*")
    root.add_central(sym.Constant(2))
    root.remove_central()
    assert root.central_child is None


def test_remove_central_wrong() -> None:
    root = sym.UnoFunc("*")
    with pytest.raises(Exception):
        root.remove_central()


def test_wrong_unofunc_compute() -> None:
    root = sym.UnoFunc("*")
    with pytest.raises(Exception):
        root.evaluate({"x": 5})


def test_wrong_duofunc_compute() -> None:
    root = sym.DuoFunc("*")
    with pytest.raises(Exception):
        root.evaluate({"x": 5})


def test_wrong_unofunc_right_children() -> None:
    root = sym.UnoFunc("*")
    with pytest.raises(Exception):
        root.add_right(sym.Constant(2))


def test_wrong_unofunc_left_children() -> None:
    root = sym.UnoFunc("*")
    with pytest.raises(Exception):
        root.add_left(sym.Constant(2))


def test_wrong_duofunc_central_children() -> None:
    root = sym.DuoFunc("*")
    with pytest.raises(Exception):
        root.add_central(sym.Constant(2))


def test_complex_tree(complex_tree: sym.Node) -> None:
    result = complex_tree.evaluate({"x": 3, "y": 4})
    assert result == 58


def test_crossingover() -> None:
    p = Population(
        ["x", "y"], [{"x": 2, "y": 3}, {"x": 3, "y": 1}, {"x": 5, "y": 6}], [1, 2, 3]
    )
    ge = GenomeEvolution(p.values, p.questions, p.answers)
    ge.crossingover(p.items)


def test_replace_child(complex_tree: sym.Node) -> None:
    result = complex_tree.evaluate({"x": 3, "y": 4})
    assert result == 58

    test_const_prev = complex_tree.left_child.right_child.left_child  # type: ignore
    test_const_new = sym.Constant(4)
    complex_tree.replace_child(test_const_prev, test_const_new)  # type: ignore

    result = complex_tree.evaluate({"x": 3, "y": 4})
    assert result == 132


def test_change_const_value(complex_tree: sym.Node) -> None:
    result = complex_tree.evaluate({"x": 3, "y": 4})
    assert result == 58

    left_left_const = complex_tree.left_child.left_child  # type: ignore
    complex_tree.change_const_value(left_left_const, 4)  # type: ignore

    result = complex_tree.evaluate({"x": 3, "y": 4})
    assert result == 62


def test_nodes_walkthrough(complex_tree: sym.Node) -> None:
    nodes = [
        sym.DuoFunc("*"),
        sym.DuoFunc("+"),
        sym.UnoFunc("math.sqrt"),
        sym.Constant(2),
        sym.DuoFunc("**"),
        sym.Variable("y"),
        sym.Constant(3),
        sym.Variable("x"),
    ]
    res = list(GenomeEvolution.nodes_walkthrough(complex_tree))

    def is_equal(a: t.Any, b: t.Any) -> bool:
        if a.__class__ == b.__class__:
            if isinstance(a, sym.Node) and isinstance(b, sym.Node):
                if a.func == b.func:
                    return True
            elif isinstance(a, sym.Constant) and isinstance(b, sym.Constant):
                if a.number == b.number:
                    return True
            elif isinstance(a, sym.Variable) and isinstance(b, sym.Variable):
                if a.name == b.name:
                    return True
        return False

    equality = [is_equal(x, y) for x, y in zip(nodes, res)]
    assert all(equality)


def test_stand() -> None:
    accuracy = NN_stand.main()
    assert accuracy < 0.1


def test_depth(complex_tree: sym.Node) -> None:
    res = complex_tree.depth()
    assert res == 4


def test_shrink(complex_tree: sym.Node) -> None:
    p = Population(
        ["x", "y"], [{"x": 2, "y": 3}, {"x": 3, "y": 1}, {"x": 5, "y": 6}], [1, 2, 3]
    )
    ge = GenomeEvolution(p.values, p.questions, p.answers)
    res = complex_tree.depth()
    print(complex_tree)
    assert res == 4
    new_tree = ge.tree_shrink(complex_tree, max_depth=2)
    new_res = new_tree.depth()
    print(new_tree)
    assert new_res == 2

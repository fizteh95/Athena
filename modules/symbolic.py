from __future__ import annotations

import math  # noqa
import typing as t
from abc import abstractmethod


class Node:
    def __init__(self) -> None:
        self.left_children = None  # type: t.Union[Node, None]
        self.right_children = None  # type: t.Union[Node, None]
        self.central_children = None  # type: t.Union[Node, None]

    def evaluate(self, variables: t.Dict[str, t.Union[int, float]]) -> int | float:
        if (
            self.left_children is not None
            and self.right_children is not None
            and self.central_children is None
        ):
            left_res = self.left_children.evaluate(variables)
            right_res = self.right_children.evaluate(variables)
            return self.compute(left_res, right_res)
        elif (
            self.central_children is not None
            and self.left_children is None
            and self.right_children is None
        ):
            central_res = self.central_children.evaluate(variables)
            return self.compute(central_res)
        else:
            raise

    @abstractmethod
    def compute(self, *args: t.Union[int, float]) -> t.Union[int, float]:
        raise NotImplementedError

    def add_left(self, node: t.Any) -> None:
        if self.left_children is None and self.central_children is None:
            self.left_children = node
        else:
            raise

    def add_right(self, node: t.Any) -> None:
        if self.right_children is None and self.central_children is None:
            self.right_children = node
        else:
            raise

    def add_central(self, node: t.Any) -> None:
        if (
            self.central_children is None
            and self.right_children is None
            and self.left_children is None
        ):
            self.central_children = node
        else:
            raise

    def remove_left(self) -> None:
        if self.left_children is not None:
            self.left_children = None
        else:
            raise

    def remove_right(self) -> None:
        if self.right_children is not None:
            self.right_children = None
        else:
            raise

    def remove_central(self) -> None:
        if self.central_children is not None:
            self.central_children = None
        else:
            raise


class Constant:
    def __init__(self, number: t.Union[int, float]):
        self.number = number

    def evaluate(self, _: t.Any) -> t.Union[int, float]:
        return self.number


class Variable:
    def __init__(self, name: str):
        self.name = name

    def evaluate(
        self, variables: t.Dict[str, t.Union[int, float]]
    ) -> t.Union[int, float]:
        return variables[self.name]


class UnoFunc(Node):
    def __init__(self, func: str):
        super().__init__()
        self.func = func

    def add_left(self, node: t.Any) -> None:
        raise

    def add_right(self, node: t.Any) -> None:
        raise

    def compute(self, *args: t.Union[int, float]) -> t.Any:
        if (
            len(args) != 1
            or self.central_children is None
            or self.right_children is not None
            or self.left_children is not None
        ):
            raise
        else:
            return eval(self.func + f"({args[0]})")  # self.func(*args)


class DuoFunc(Node):
    def __init__(self, func: str):
        super().__init__()
        self.func = func

    def add_central(self, node: t.Any) -> None:
        raise

    def compute(self, *args: t.Union[int, float]) -> t.Any:
        if (
            len(args) != 2
            or self.central_children is not None
            or self.right_children is None
            or self.left_children is None
        ):
            raise
        else:
            return eval(f"({args[0]})" + self.func + f"({args[1]})")  # self.func(*args)


def main() -> None:
    root = DuoFunc("**")
    root.add_left(Constant(2))
    root.add_right(Variable("x"))
    result = root.evaluate({"x": 7})
    print(result)


if __name__ == "__main__":
    main()

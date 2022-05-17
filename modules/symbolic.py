from __future__ import annotations

import math  # noqa
import typing as t
from abc import abstractmethod


class Node:
    def __init__(self) -> None:
        self.left_child = None  # type: t.Union[Node, None]
        self.right_child = None  # type: t.Union[Node, None]
        self.central_child = None  # type: t.Union[Node, None]

    def evaluate(self, variables: t.Dict[str, t.Union[int, float]]) -> int | float:
        if (
            self.left_child is not None
            and self.right_child is not None
            and self.central_child is None
        ):
            left_res = self.left_child.evaluate(variables)
            right_res = self.right_child.evaluate(variables)
            return self.compute(left_res, right_res)
        elif (
            self.central_child is not None
            and self.left_child is None
            and self.right_child is None
        ):
            central_res = self.central_child.evaluate(variables)
            return self.compute(central_res)
        else:
            raise

    @abstractmethod
    def compute(self, *args: t.Union[int, float]) -> t.Union[int, float]:
        raise NotImplementedError

    def add_left(self, node: t.Any) -> None:
        if self.left_child is None and self.central_child is None:
            self.left_child = node
        else:
            raise

    def add_right(self, node: t.Any) -> None:
        if self.right_child is None and self.central_child is None:
            self.right_child = node
        else:
            raise

    def add_central(self, node: t.Any) -> None:
        if (
            self.central_child is None
            and self.right_child is None
            and self.left_child is None
        ):
            self.central_child = node
        else:
            raise

    def remove_left(self) -> None:
        if self.left_child is not None:
            self.left_child = None
        else:
            raise

    def remove_right(self) -> None:
        if self.right_child is not None:
            self.right_child = None
        else:
            raise

    def remove_central(self) -> None:
        if self.central_child is not None:
            self.central_child = None
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

    def __repr__(self) -> str:
        return f"UnoFunc {self.func} with child {self.central_child}"

    def add_left(self, node: t.Any) -> None:
        raise

    def add_right(self, node: t.Any) -> None:
        raise

    def compute(self, *args: t.Union[int, float]) -> t.Any:
        if (
            len(args) != 1
            or self.central_child is None
            or self.right_child is not None
            or self.left_child is not None
        ):
            raise
        else:
            return eval(self.func + f"({args[0]})")  # self.func(*args)


class DuoFunc(Node):
    def __init__(self, func: str):
        super().__init__()
        self.func = func

    def __repr__(self) -> str:
        return f"DuoFunc {self.func} with children {self.left_child} and {self.right_child}"

    def add_central(self, node: t.Any) -> None:
        raise

    def compute(self, *args: t.Union[int, float]) -> t.Any:
        if (
            len(args) != 2
            or self.central_child is not None
            or self.right_child is None
            or self.left_child is None
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

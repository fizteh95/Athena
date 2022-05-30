from __future__ import annotations
import uuid

import math  # noqa
import typing as t
from abc import abstractmethod


class Node:
    def __init__(self) -> None:
        self.left_child = None  # type: t.Union[Node, None]
        self.right_child = None  # type: t.Union[Node, None]
        self.central_child = None  # type: t.Union[Node, None]
        self.id = uuid.uuid1()

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

    def get_children(self) -> t.List[t.Type[Node | Constant | Variable]]:
        res = []
        for x in [self.left_child, self.right_child, self.central_child]:
            if x is not None:
                res.append(x)
        return res

    def replace_child(self, child: t.Any, new_child: t.Any) -> None:
        if self.central_child is not None:
            if self.central_child.id == child.id:
                self.remove_central()
                self.add_central(new_child)
            else:
                self.central_child.replace_child(child, new_child)
        elif self.right_child is not None or self.left_child is not None:
            if self.right_child.id == child.id:
                self.remove_right()
                self.add_right(new_child)
            elif self.left_child.id == child.id:
                self.remove_left()
                self.add_left(new_child)
            else:
                self.right_child.replace_child(child, new_child)
                self.left_child.replace_child(child, new_child)

    def change_const_value(self, const, new_value):
        if self.central_child is not None:
            if self.central_child.id == const.id:
                self.central_child.number = new_value
            else:
                self.central_child.change_const_value(const, new_value)
        elif self.right_child is not None or self.left_child is not None:
            if self.right_child.id == const.id:
                self.right_child.number = new_value
            elif self.left_child.id == const.id:
                self.left_child.number = new_value
            else:
                self.right_child.change_const_value(const, new_value)
                self.left_child.change_const_value(const, new_value)


class Leaf:
    def get_children(self) -> t.List:
        return []

    def change_const_value(self, const, new_value):
        pass

    def replace_child(self, child: t.Any, new_child: t.Any) -> None:
        pass


class Constant(Leaf):
    def __init__(self, number: t.Union[int, float]):
        self.number = number
        self.id = uuid.uuid1()

    def evaluate(self, _: t.Any) -> t.Union[int, float]:
        return self.number

    def change_const_value(self, const, new_value):
        if const.id == self.id:
            self.number = new_value


class Variable(Leaf):
    def __init__(self, name: str):
        self.name = name
        self.id = uuid.uuid1()

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

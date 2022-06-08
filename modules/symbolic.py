from __future__ import annotations

import math  # noqa
import typing as t
import uuid
from abc import abstractmethod


class Node:
    def __init__(self) -> None:
        self.left_child = None  # type: t.Union[Node, Leaf, None]
        self.right_child = None  # type: t.Union[Node, Leaf, None]
        self.central_child = None  # type: t.Union[Node, Leaf, None]
        self.id = uuid.uuid1()
        self.current_depth: t.Union[None, int] = None

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

    def get_children(self) -> t.List[t.Union[Node, Leaf]]:
        res = []
        for x in [self.left_child, self.right_child, self.central_child]:
            if x is not None:
                res.append(x)
        return res

    def replace_child(self, child: t.Union[Node, Leaf], new_child: t.Any) -> None:
        if self.central_child is not None:
            if self.central_child.id == child.id:
                self.remove_central()
                self.add_central(new_child)
            else:
                self.central_child.replace_child(child, new_child)
        elif self.right_child is not None and self.left_child is not None:
            if self.right_child.id == child.id:
                self.remove_right()
                self.add_right(new_child)
            elif self.left_child.id == child.id:
                self.remove_left()
                self.add_left(new_child)
            else:
                self.right_child.replace_child(child, new_child)
                self.left_child.replace_child(child, new_child)

    def change_const_value(self, const: Constant, new_value: int | float) -> None:
        if self.central_child is not None:
            if (
                isinstance(self.central_child, Constant)
                and self.central_child.id == const.id
            ):
                self.central_child.number = new_value
            else:
                self.central_child.change_const_value(const, new_value)
        elif self.right_child is not None and self.left_child is not None:
            if self.right_child.id == const.id and isinstance(
                self.right_child, Constant
            ):
                self.right_child.number = new_value
            elif self.left_child.id == const.id and isinstance(
                self.left_child, Constant
            ):
                self.left_child.number = new_value
            else:
                self.right_child.change_const_value(const, new_value)
                self.left_child.change_const_value(const, new_value)

    def is_in(self, node: t.Union[Node, Leaf]) -> bool:
        if node.id == self.id:
            return True
        elif self.central_child is not None:
            return self.central_child.is_in(node)
        elif self.right_child is not None and self.left_child is not None:
            return self.right_child.is_in(node) or self.left_child.is_in(node)
        return False

    def change_func_type(self, node: Node, f_type: str) -> None:
        if node.id == self.id:
            self.func = f_type
        else:
            if self.central_child is not None:
                self.central_child.change_func_type(node, f_type)
            elif self.right_child is not None and self.left_child is not None:
                self.right_child.change_func_type(node, f_type)
                self.left_child.change_func_type(node, f_type)

    def depth(self, start_depth: int = 0) -> int:
        self.current_depth = start_depth + 1
        if self.central_child is not None:
            depth = self.central_child.depth(start_depth=self.current_depth)
        elif self.right_child is not None and self.left_child is not None:
            right_depth = self.right_child.depth(start_depth=self.current_depth)
            left_depth = self.left_child.depth(start_depth=self.current_depth)
            if right_depth >= left_depth:
                depth = right_depth
            else:
                depth = left_depth
        else:
            raise
        return depth


class Leaf:
    def __init__(self) -> None:
        self.id = uuid.uuid1()
        self.current_depth: t.Union[None, int] = None

    def evaluate(self, variables: t.Dict[str, t.Union[int, float]]) -> int | float:
        raise

    def get_children(self) -> t.List[t.Union[Node, Leaf]]:
        return []

    def change_const_value(self, const: Constant, new_value: int | float) -> None:
        pass

    def replace_child(self, child: t.Union[Node, Leaf], new_child: t.Any) -> None:
        pass

    def is_in(self, node: t.Union[Node, Leaf]) -> bool:
        if node.id == self.id:
            return True
        return False

    def change_func_type(self, node: Node, f_type: str) -> None:
        pass

    def depth(self, start_depth: int = 0) -> int:
        self.current_depth = start_depth + 1
        return self.current_depth


class Constant(Leaf):
    def __init__(self, number: t.Union[int, float]):
        super().__init__()
        self.number = number

    def evaluate(self, _: t.Any) -> t.Union[int, float]:
        return self.number

    def change_const_value(self, const: Constant, new_value: int | float) -> None:
        if const.id == self.id:
            self.number = new_value


class Variable(Leaf):
    def __init__(self, name: str):
        super().__init__()
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
        return f"UnoFunc {self.func} with child ({self.central_child})"

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
        return f"DuoFunc {self.func} with children ({self.left_child}) and ({self.right_child})"

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

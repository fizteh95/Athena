import typing as t

import numpy as np
import symbolic as sym


def test_funcs(
    f1: t.Callable[[t.Union[int, float]], float],
    f2: t.Callable[[t.Union[int, float]], float],
    debug: bool = False,
) -> float:
    def nonlin(x: t.Union[int, float], deriv: bool = False) -> float:
        if deriv:
            return f1(x)
        return f2(x)

    X: t.Any = np.array([[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]])
    y: t.Any = np.array([[0], [1], [1], [0]])

    np.random.seed(1)

    # случайно инициализируем веса, в среднем - 0
    syn0 = 2 * np.random.random((3, 4)) - 1
    syn1 = 2 * np.random.random((4, 1)) - 1
    l2_error = [[1], [1], [1], [1]]

    for j in range(5000):
        # проходим вперёд по слоям 0, 1 и 2
        l0 = X
        l1 = np.vectorize(nonlin)(np.dot(l0, syn0))
        l2 = np.vectorize(nonlin)(np.dot(l1, syn1))

        # как сильно мы ошиблись относительно нужной величины?
        l2_error = y - l2  # [[]]

        if (j % 100) == 0 and debug:
            print("Error:" + str(np.mean(np.abs(l2_error))))

        # в какую сторону нужно двигаться?
        # если мы были уверены в предсказании, то сильно менять его не надо
        l2_delta = l2_error * np.vectorize(nonlin)(l2, deriv=True)

        # как сильно значения l1 влияют на ошибки в l2?
        l1_error = l2_delta.dot(
            syn1.T
        )  # [[], [], [], []] каждый синапс который идет к i нейрону домножаем на дельту этого нейрона

        # в каком направлении нужно двигаться, чтобы прийти к l1?
        # если мы были уверены в предсказании, то сильно менять его не надо
        l1_delta = l1_error * np.vectorize(nonlin)(l1, deriv=True)

        syn1 += l1.T.dot(l2_delta)
        syn0 += l0.T.dot(l1_delta)

    return float(np.mean(np.abs(l2_error)))


def get_node_quality(root_node: sym.Node, debug: bool = False) -> float:
    """
    Use ONLY ONE VARIABLE - x !!!
    :param root_node:
    :param debug:
    :return:
    """
    x1 = lambda x: root_node.evaluate({"x": x})
    x2 = lambda x: 1 / (1 + np.exp(-x))
    return test_funcs(x1, x2, debug=debug)


def main() -> float:
    # x * (1 - x)
    rl_child = sym.Constant(1)
    rr_child = sym.Variable("x")
    r_child = sym.DuoFunc("-")
    r_child.add_left(rl_child)
    r_child.add_right(rr_child)
    l_child = sym.Variable("x")
    root = sym.DuoFunc("*")
    root.add_left(l_child)
    root.add_right(r_child)

    res = get_node_quality(root, debug=True)
    # print(res)
    return res


if __name__ == "__main__":
    main()

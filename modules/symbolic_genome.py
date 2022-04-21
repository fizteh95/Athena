import copy
import math
import random as r
import typing as t

import symbolic as sym

UNO_FUNCS = ["math.sin", "math.cos", "math.log2", "math.log10", "math.sqrt"]
DUO_FUNCS = ["+", "-", "*", "/", "**"]

INIT_NUMBER = 10  # количество объектов в первоначальной популяции
PROB_LEAF_CREATE = 0.7  # вероятность создания листового элемента (константа, переменная), 1-PROB_LEAF_CREATE - функция
PROB_VAR_CREATE = 0.5  # вероятность создания переменной, 1-PROB_VAR_CREATE - вероятность создания константы
PROB_DUO_CREATE = (
    0.7  # вероятность создания бинарной фукнции, 1-PROB_DUO_CREATE - создание унарной
)
NUM_OF_CROSSES = 100  # количество потомков в кроссинговере

MUT_PROB_OF_TYPE = 0.6  # вероятность мутации 1 типа, 1-MUT_PROB_OF_TYPE - 2 тип
MUT_CONST_TO_VAR = 0.1  # вероятность преобразования константы в переменную
MUT_CONST_CHANGE = 0.1  # вероятность изменения константы на случайную величину


class Population:
    def __init__(
        self,
        values: t.List[str],
        questions: t.List[t.Dict[str, t.Union[int, float]]],
        answers: t.List[t.Union[int, float]],
        items: t.Union[t.List[sym.Node], None] = None,
    ):
        self.values = values
        self.answers = answers
        self.questions = questions
        if items is None:
            self.items = self.create_random()
        else:
            self.items = items

    def create_leaf(self) -> t.Union[sym.Variable, sym.Constant]:
        if r.random() < PROB_VAR_CREATE:
            node = sym.Variable(r.choice(self.values))
        else:
            node = sym.Constant(r.uniform(-20, 20))
        return node

    def _create_leaf_or_func(
        self,
    ) -> t.Union[sym.Variable, sym.Constant, sym.UnoFunc, sym.DuoFunc]:
        if r.random() < PROB_LEAF_CREATE:
            updated_node = self.create_leaf()
        else:
            if r.random() < PROB_DUO_CREATE:
                node = sym.DuoFunc(r.choice(DUO_FUNCS))
            else:
                node = sym.UnoFunc(r.choice(UNO_FUNCS))
            updated_node = self.create_node(node)

        return updated_node

    def create_node(self, root: t.Union[sym.UnoFunc, sym.DuoFunc]) -> sym.Node:
        if isinstance(root, sym.UnoFunc):
            root.add_central(self._create_leaf_or_func())
            return root
        elif isinstance(root, sym.DuoFunc):
            for child in ("left", "right"):
                updated_node = self._create_leaf_or_func()
                if child == "left":
                    root.add_left(updated_node)
                else:
                    root.add_right(updated_node)

            return root

    def create_random(self) -> t.List[sym.Node]:
        result = []
        for _ in range(INIT_NUMBER):
            result.append(self._create_leaf_or_func())

        return result

    def get_score(self, item: sym.Node) -> t.Union[int, float]:
        results = []
        for q in self.questions:
            try:
                result = item.evaluate(q)
                if isinstance(result, complex):
                    result = -math.inf
            except (ZeroDivisionError, ValueError, TypeError, OverflowError):
                result = -math.inf
            results.append(result)
        sub = [x**2 - y**2 for x, y in zip(results, self.answers)]
        res = sum(sub)
        return res

    def sort_population(self) -> t.List[sym.Node]:
        sorted_items = sorted(self.items, key=lambda x: self.get_score(x), reverse=True)
        return sorted_items

    def get_best_items(self, n: int = 10) -> t.List[sym.Node]:
        sorted_population = self.sort_population()
        return sorted_population[:n]

    @property
    def best_score(self) -> t.Union[int, float]:
        sorted_population = self.sort_population()
        return self.get_score(sorted_population[0])


class GenomeEvolution:
    def __init__(
        self,
        values: t.List[str],
        questions: t.List[t.Dict[str, t.Union[int, float]]],
        answers: t.List[t.Union[int, float]],
    ):
        self.answers = answers
        self.values = values
        self.questions = questions
        self.population = Population(self.values, self.questions, self.answers)

    def crossingover(self, items: t.List[sym.Node]) -> t.List[sym.Node]:
        """
        Левое дерево базовое, отрезаем случайного потомка, справа берем случайного потомка и подключаем к левому
        :param items:
        :return:
        """
        new_items = []
        for _ in range(NUM_OF_CROSSES):
            parent_a = copy.deepcopy(r.choice(items))
            parent_b = copy.deepcopy(r.choice(items))
            new_item = parent_a
            a_is_childfree = isinstance(parent_a, (sym.Constant, sym.Variable))
            b_is_childfree = isinstance(parent_b, (sym.Constant, sym.Variable))
            a_has_two_children = hasattr(parent_a, "left_child")
            b_has_two_children = hasattr(parent_b, "left_child")
            # True — используем левого потомка, иначе правого.
            a_coin_flip = r.random() > 0.5
            b_coin_flip = r.random() > 0.5
            comb = (a_is_childfree, b_is_childfree, a_has_two_children, b_has_two_children, a_coin_flip, b_coin_flip)
            match comb:
                case (True, True, _, _, _, _):
                    continue  # слишком простые.
                case (True, False, _, True, _, True):
                    # a простой, b имеет двух детей, a становится левым ребёнком.
                    parent_b.left_child = parent_a
                    new_item = parent_b
                case (True, False, _, True, _, False):
                    # a простой, b имеет двух детей, a становится правым ребёнком.
                    parent_b.right_child = parent_a
                    new_item = parent_b
                case (True, False, _, False, _, _):
                    # a простой, b имеет одного ребёнка, a становится ребёнком.
                    parent_b.central_child = parent_a
                    new_item = parent_b
                case (False, True, True, _, True, _):
                    # b простой, a имеет двух детей, b становится левым ребёнком.
                    parent_a.left_child = parent_b
                    new_item = parent_a
                case (False, True, True, _, False, _):
                    # b простой, a имеет двух детей, b становится правым ребёнком.
                    parent_a.right_child = parent_b
                    new_item = parent_a
                case (False, True, _, False, _, _):
                    # b простой, a имеет одного ребёнка, b становится ребёнком.
                    parent_a.central_child = parent_b
                    new_item = parent_a
                case (False, False, True, False, True, _):
                    # a имеет двух детей, b одного, ребёнок b становится левым ребёнком a.
                    parent_a.left_child = parent_b.central_child
                    new_item = parent_a
                case (False, False, True, False, False, _):
                    # a имеет двух детей, b одного, ребёнок b становится правым ребёнком a.
                    parent_a.right_child = parent_b.central_child
                    new_item = parent_a
                case (False, False, False, False, _, _):
                    # a и b имеют по одному ребёнку, ребёнок b становится ребёнком a.
                    parent_a.central_child = parent_b.central_child
                    new_item = parent_a
                case (False, False, True, True, True, True):
                    # у a и b по два ребёнка, левый ребёнок b становится левым ребёнком a.
                    parent_a.left_child = parent_b.left_child
                    new_item = parent_a
                case (False, False, True, True, True, False):
                    # у a и b по два ребёнка, правый ребёнок b становится левым ребёнком a.
                    parent_a.left_child = parent_b.right_child
                    new_item = parent_a
                case (False, False, True, True, False, True):
                    # у a и b по два ребёнка, левый ребёнок b становится правым ребёнком a.
                    parent_a.right_child = parent_b.left_child
                    new_item = parent_a
                case (False, False, True, True, False, False):
                    # у a и b по два ребёнка, правый ребёнок b становится правым ребёнком a.
                    parent_a.right_child = parent_b.right_child
                    new_item = parent_a

            new_item = self.tree_shrink(new_item)
            new_items.append(new_item)
        return new_items

    def mutation(self, items: t.List[sym.Node], rate: float = 0.2) -> t.List[sym.Node]:
        """
        Изменения 1-го типа
        Для констант - преобразование в переменную, изменение на случ. величину
        Для переменных - преобразование в константу, в функцию с добавлением нод, в другую переменную
        Для функций - включение в новую функцию как одного из потомков, вместо операции остается центральный потомок
        либо один из двух потомков, операнды меняются местами, заменяем тип функции, заменяется класс функции

        Изменения 2-го типа
        Замена рандомного потомка на случайное дерево
        Удаление UnoFunc как промежуточного узла
        Назначение корнем дерева новой функции, при необходимости доращиваем потомков

        :param items:
        :param rate:
        :return:
        """
        new_items = []
        for item in items:
            rate += rate
            new_item = copy.deepcopy(item)
            if r.random() < MUT_PROB_OF_TYPE:
                ...
            else:
                ...
            new_item = self.tree_shrink(new_item)
            new_items.append(new_item)
        return new_items

    @staticmethod
    def tree_shrink(item: sym.Node) -> sym.Node:
        """
        Оптимизация дерева, схлопывание функций только с константами, ограничение глубины деревьев
        :param item:
        :return:
        """
        return item

    def evolve(self) -> None:
        count = 0
        best_score = self.population.best_score
        while best_score > 0.1:
            new_population = []
            best_items = self.population.get_best_items()
            new_population += best_items
            new_population += self.crossingover(best_items)
            new_population += self.mutation(new_population, rate=0.2)
            self.population = Population(
                self.values, self.questions, self.answers, items=new_population
            )
            best_score = self.population.best_score
            count += 1
            if count % 10 == 0:
                print(f"Best score: {best_score}, count: {count}")


if __name__ == "__main__":
    p = Population(
        ["x", "y"], [{"x": 2, "y": 3}, {"x": 3, "y": 1}, {"x": 5, "y": 6}], [1, 2, 3]
    )
    ge = GenomeEvolution(p.values, p.questions, p.answers)
    ge.crossingover(p.items)
    print("Done")

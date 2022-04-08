import copy
import math  # noqa
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
        values: t.List[t.Union[int, float]],
        questions: t.List[t.Dict],
        answers: t.List,
        items: t.List = None,
    ):
        self.values = values
        self.answers = answers
        self.questions = questions
        if items is None:
            self.items = self.create_random()
        else:
            self.items = items

    def create_leaf(self):
        if r.random() < PROB_VAR_CREATE:
            node = sym.Variable(r.choice(self.values))
        else:
            node = sym.Constant(r.uniform(-20, 20))
        return node

    def create_node(self, root):
        if isinstance(root, sym.UnoFunc):
            if r.random() < PROB_LEAF_CREATE:
                updated_node = self.create_leaf()
            else:
                if r.random() < PROB_DUO_CREATE:
                    node = sym.DuoFunc(r.choice(DUO_FUNCS))
                else:
                    node = sym.UnoFunc(r.choice(UNO_FUNCS))
                updated_node = self.create_node(node)
            root.add_central(updated_node)
            return root
        elif isinstance(root, sym.DuoFunc):
            # left
            if r.random() < PROB_LEAF_CREATE:
                updated_node = self.create_leaf()
            else:
                if r.random() < PROB_DUO_CREATE:
                    node = sym.DuoFunc(r.choice(DUO_FUNCS))
                else:
                    node = sym.UnoFunc(r.choice(UNO_FUNCS))
                updated_node = self.create_node(node)
            root.add_left(updated_node)
            # right
            if r.random() < PROB_LEAF_CREATE:
                updated_node = self.create_leaf()
            else:
                if r.random() < PROB_DUO_CREATE:
                    node = sym.DuoFunc(r.choice(DUO_FUNCS))
                else:
                    node = sym.UnoFunc(r.choice(UNO_FUNCS))
                updated_node = self.create_node(node)
            root.add_right(updated_node)
            return root

    def create_random(self):
        result = []
        for _ in range(INIT_NUMBER):
            if r.random() < PROB_LEAF_CREATE:
                root = self.create_leaf()
                result.append(root)
            else:
                if r.random() < PROB_DUO_CREATE:
                    root = sym.DuoFunc(r.choice(DUO_FUNCS))
                else:
                    root = sym.UnoFunc(r.choice(UNO_FUNCS))
                root = self.create_node(root)
                result.append(root)

        return result

    def get_score(self, item: sym.Node):
        results = []
        for q in self.questions:
            result = item.evaluate(q)
            results.append(result)
        sub = [x**2 - y**2 for x, y in zip(results, self.answers)]
        res = sum(sub)
        return res

    def sort_population(self):
        sorted_items = sorted(self.items, key=lambda x: self.get_score(x), reverse=True)
        return sorted_items

    def get_best_items(self, n=10):
        sorted_population = self.sort_population()
        return sorted_population[:n]

    @property
    def best_score(self):
        sorted_population = self.sort_population()
        return self.get_score(sorted_population[0])


class GenomeEvolution:
    def __init__(self, values: t.List, questions: t.List[t.Dict], answers: t.List):
        self.answers = answers
        self.values = values
        self.questions = questions
        self.population = Population(self.values, self.questions, self.answers)

    def crossingover(self, items):
        """
        Левое дерево базовое, отрезаем случайного потомка, справа берем случайного потомка и подключаем к левому
        :param items:
        :return:
        """
        new_items = []
        for _ in range(NUM_OF_CROSSES):
            parent_a = copy.deepcopy(r.choice(items))
            parent_b = copy.deepcopy(r.choice(items))
            ...
            new_item = None
            new_item = self.tree_shrink(new_item)
            new_items.append(new_item)
        return new_items

    def mutation(self, items, rate=0.2):
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
            new_item = copy.deepcopy(item)
            if r.random() < MUT_PROB_OF_TYPE:
                ...
            else:
                ...
            new_item = self.tree_shrink(new_item)
            new_items.append(new_item)
        return new_items

    def tree_shrink(self, item):
        """
        Оптимизация дерева, схлопывание функций только с константами, ограничение глубины деревьев
        :param item:
        :return:
        """
        return item

    def evolute(self):
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
    print(p.items[0])
    print(p.items[1])
    print("Done")

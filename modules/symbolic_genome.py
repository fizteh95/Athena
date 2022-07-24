import copy
import math
import random as r
import typing as t
import uuid

from sklearn.metrics import mean_absolute_error

from .symbolic import Constant
from .symbolic import DuoFunc
from .symbolic import Leaf
from .symbolic import Node
from .symbolic import UnoFunc
from .symbolic import Variable

UNO_FUNCS = ["math.sin", "math.cos", "math.log2", "math.log10", "math.sqrt"]
DUO_FUNCS = ["+", "-", "*", "/"]  # , "**"

INIT_NUMBER = 50  # количество объектов в первоначальной популяции
PROB_LEAF_CREATE = 0.6  # вероятность создания листового элемента (константа, переменная), 1-PROB_LEAF_CREATE - функция
PROB_VAR_CREATE = 0.5  # вероятность создания переменной, 1-PROB_VAR_CREATE - вероятность создания константы
PROB_DUO_CREATE = (
    0.8  # вероятность создания бинарной фукнции, 1-PROB_DUO_CREATE - создание унарной
)

NUM_OF_CROSSES = 50  # количество потомков в кроссинговере
CROSS_PROB_CHANGE_CHILD = (
    0.5  # вероятность замены одного из потомка на потомка из другого дерева
)
CROSS_PROB_NEW_TREE = (
    0.5  # вероятность создания нового дерева из двух родителей (ветви нового дерева)
)
CROSS_PROB_INPLACE_PARENT = (
    0.5  # вероятность внедрения одного из родителя как ветки другого
)

MUT_PROB_OF_TYPE = 1  # вероятность мутации 1 типа, 1-MUT_PROB_OF_TYPE - 2 тип
MUT_PROB_CONST_CHANGE = 0.7  # вероятность изменения значения константы (новое значение)
MUT_CONST_TO_VAR = 0.5  # вероятность преобразования константы в переменную

MUT_PROB_VAR_TO_CONST = 0.5  # вероятность превращения переменной в константу
MUT_PROB_VAR_CHANGE = 0.5  # вероятность преобразования переменной в другую переменную
MUT_PROB_VAR_TO_FUNC = 0.7  # вероятность преобразования переменной в функцию с сохранением переменной как потомка

MUT_PROB_FUNC_TO_CHILD = (
    0.7  # вероятность включения функции в новую функцию как одного из потомков
)
MUT_PROB_LEAVE_CHILD = 0.7  # вероятность того, что вместо оп-ии остается центральный потомок либо один из двух потомков
MUT_PROB_OPERANDS_CHANGE = 0.7  # вероятность того, что операнды поменяются местами
MUT_PROB_CHANGE_FUNC_TYPE = 0.7  # вероятность изменения типа функции
MUT_PROB_CHANGE_FUNC_CLASS = 0.7  # вероятность изменения класса функции


class Population:
    def __init__(
        self,
        values: t.List[str],
        questions: t.List[t.Dict[str, t.Union[int, float]]],
        answers: t.List[t.Union[int, float]],
        items: t.Union[t.List[t.Union[Node, Variable, Constant]], None] = None,
    ):
        self.values = values
        self.answers = answers
        self.questions = questions
        if items is None:
            self.items = self.create_random()
        else:
            self.items = items

    # TODO: перенести методы в класс деревьев
    @staticmethod
    def create_leaf(values: t.List[str]) -> t.Union[Variable, Constant]:
        if r.random() < PROB_VAR_CREATE:
            return Variable(r.choice(values))
        else:
            return Constant(r.uniform(-20, 20))

    @staticmethod
    def create_leaf_or_func(
        values: t.List[str],
        only_func: bool = False,
        need_type: t.Union[str, None] = None,
    ) -> t.Union[Variable, Constant, UnoFunc, DuoFunc, Node]:
        if r.random() < PROB_LEAF_CREATE and not only_func:
            return Population.create_leaf(values)
        else:
            if need_type is not None:
                if need_type == "uno":
                    return Population.create_node(UnoFunc(r.choice(UNO_FUNCS)), values)
                elif need_type == "duo":
                    return Population.create_node(DuoFunc(r.choice(DUO_FUNCS)), values)
            if r.random() < PROB_DUO_CREATE:
                return Population.create_node(DuoFunc(r.choice(DUO_FUNCS)), values)
            else:
                return Population.create_node(UnoFunc(r.choice(UNO_FUNCS)), values)

    @staticmethod
    def create_node(root: t.Union[UnoFunc, DuoFunc], values: t.List[str]) -> Node:
        if isinstance(root, UnoFunc):
            root.add_central(Population.create_leaf_or_func(values))
            return root
        elif isinstance(root, DuoFunc):
            for child in ("left", "right"):
                updated_node = Population.create_leaf_or_func(values)
                if child == "left":
                    root.add_left(updated_node)
                else:
                    root.add_right(updated_node)
            return root

    def create_random(self) -> t.List[t.Union[Constant, Variable, Node]]:
        result = []
        for _ in range(INIT_NUMBER):
            result.append(self.create_leaf_or_func(self.values))

        return result

    def get_score(self, item: t.Union[Constant, Variable, Node], debug=False) -> t.Union[int, float]:
        # print(debug)
        results = []
        for q in self.questions:
            try:
                result = item.evaluate(q)
                if isinstance(result, complex):
                    result = -math.inf
                    result = -999
            except (ZeroDivisionError, ValueError, TypeError, OverflowError):
                result = -math.inf
                result = -999
            results.append(result)
        if debug:
            print('ha')
            print(results)
            print(self.answers)
        # print('*********')
        res = mean_absolute_error(self.answers, results)
        # sub = [x - y for x, y in zip(results, self.answers)]
        # res = sum(sub)
        return res

    def sort_population(self) -> t.List[t.Union[Constant, Variable, Node]]:
        sorted_items = sorted(self.items, key=lambda x: self.get_score(x))  # , reverse=True
        return sorted_items

    def get_best_items(self, n: int = 10) -> t.List[t.Union[Constant, Variable, Node]]:
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

    @staticmethod
    def _get_depth(tree: t.Union[Constant, Variable, Node]) -> t.List[str]:
        """
        Возвращает список методов, который нужно применить, чтобы дойти до последнего бездетного ребёнка.
        :param tree: входное дерево.
        :return methods_list: список методов для eval.
        """
        methods_list = []
        if isinstance(tree, Node):
            if hasattr(tree, "left_child") and tree.left_child:
                if r.random() > 0.5:
                    methods_list.append("left_child")
                else:
                    methods_list.append("right_child")
            elif hasattr(tree, "central_child") and tree.central_child:
                methods_list.append("central_child")
        else:
            return methods_list

        child = eval(f"tree.{methods_list[-1]}")
        while True:
            if hasattr(child, "left_child") and child.left_child:
                if r.random() > 0.5:
                    methods_list.append("left_child")
                    child = eval(f"child.{methods_list[-1]}")
                    continue
                else:
                    methods_list.append("right_child")
                    child = eval(f"child.{methods_list[-1]}")
                    continue
            elif hasattr(child, "central_child") and child.central_child:
                methods_list.append("central_child")
                child = eval(f"child.{methods_list[-1]}")
                continue
            else:
                break

        return methods_list

    def crossingover(
        self, items: t.List[t.Union[Constant, Variable, Node]]
    ) -> t.List[t.Union[Constant, Variable, Node]]:
        """
        :param items:
        :return:
        """
        new_items = []
        for _ in range(NUM_OF_CROSSES):
            parent_a = copy.deepcopy(r.choice(items))
            parent_b = copy.deepcopy(r.choice(items))
            while parent_a.__repr__() == parent_b.__repr__():
                parent_b = copy.deepcopy(r.choice(items))
            # замена одного из потомков на потомка из другого дерева
            if (
                r.random() < CROSS_PROB_CHANGE_CHILD
                and parent_a.depth() > 1
                and parent_b.depth() > 1
            ):
                children_a = list(self.nodes_walkthrough(parent_a))[1:]
                child_to_replace = r.choice(children_a)
                children_b = list(self.nodes_walkthrough(parent_b))[1:]
                child_to_inplace = r.choice(children_b)
                parent_a.replace_child(child_to_replace, child_to_inplace)
                new_item = parent_a
            # внедрение одного из родителя как ветки другого
            elif r.random() < CROSS_PROB_INPLACE_PARENT and (
                parent_a.depth() > 1 or parent_b.depth() > 1
            ):
                parent_a, parent_b = (
                    (parent_a, parent_b)
                    if parent_a.depth() > 1
                    else (parent_b, parent_a)
                )
                children_a = list(self.nodes_walkthrough(parent_a))[1:]
                child_to_replace = r.choice(children_a)
                #
                try:
                    parent_a.replace_child(child_to_replace, parent_b)
                except:
                    return Population.create_leaf(self.values)
                new_item = parent_a
            # создание нового дерева из двух родителей (ветви нового дерева)
            elif r.random() < CROSS_PROB_NEW_TREE:
                new_item = DuoFunc(r.choice(DUO_FUNCS))
                new_item.add_left(parent_a)
                new_item.add_right(parent_b)
            else:  # если неудачно, то просто создаем рандомное дерево
                new_item = Population.create_leaf_or_func(self.values)
            new_item = self.tree_shrink(new_item)
            new_items.append(new_item)
        return new_items

    @staticmethod
    def nodes_walkthrough(
        root: Node | Leaf | Constant,
        filter_type: t.Union[None, t.Type[Node | Leaf | Constant]] = None,
    ) -> t.Generator[Node | Leaf | Constant, None, None]:
        """
        BFS for syntax tree
        :param root: root node
        :param filter_type: node type for filtering
        :return: yield nodes given types
        """
        visited: t.List[t.Union[Node, Leaf]]
        queue: t.List[t.Union[Node, Leaf]]
        visited = []
        queue = []
        visited.append(root)
        queue.append(root)
        if filter_type is None:
            yield root
        else:
            if isinstance(root, filter_type):
                yield root
        while queue:
            s = queue.pop(0)
            for neighbor in s.get_children():
                if neighbor not in visited:
                    visited.append(neighbor)
                    queue.append(neighbor)
                    if filter_type is None:
                        yield neighbor
                    else:
                        if isinstance(neighbor, filter_type):
                            yield neighbor

    def mutation(
        self,
        items: t.List[t.Union[Constant, Variable, Node]],
        rate: float = 0.2,
    ) -> t.List[t.Union[Constant, Variable, Node]]:
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
        (на самом деле, изменения 2-го типа аналогичны последовательным изменения 1-го типа, но скорее всего
        они будут приводить к более быстрым изменениям деревьев)

        nodes_walkthrough идет сверху вниз, и возможна ситуация когда мы уже удалили узел, но он возвращен генератором,
        поэтому проверяем есть ли обрабатываемый узел в новом дереве

        :param items:
        :param rate:
        :return:
        """
        new_items = []
        # old_items = copy.deepcopy(items)
        for item in items:
            rate += rate
            new_item = copy.deepcopy(item)
            if r.random() < MUT_PROB_OF_TYPE:
                const: Constant
                for const in self.nodes_walkthrough(new_item, filter_type=Constant):  # type: ignore
                    if not new_item.is_in(const):  # если уже нет этого узла в дереве
                        continue
                    # замена значения на другое
                    if r.random() < MUT_PROB_CONST_CHANGE:
                        new_item.change_const_value(const, r.uniform(-20, 20))
                    # преобразование в переменную
                    elif r.random() < MUT_CONST_TO_VAR:
                        var = Variable(r.choice(self.values))
                        if isinstance(new_item, Constant):
                            new_item = var
                        else:
                            new_item.replace_child(const, var)
                for var in self.nodes_walkthrough(new_item, filter_type=Variable):  # type: ignore
                    if not new_item.is_in(var):  # если уже нет этого узла в дереве
                        continue
                    # преобразование в константу
                    if r.random() < MUT_PROB_VAR_TO_CONST:
                        const = Constant(r.uniform(-20, 20))
                        if isinstance(new_item, Variable):
                            new_item = const
                        else:
                            new_item.replace_child(var, const)
                    # преобразование в другую переменную
                    elif r.random() < MUT_PROB_VAR_CHANGE:
                        new_var = Variable(r.choice(self.values))
                        if isinstance(new_item, Variable):
                            new_item = new_var
                        else:
                            new_item.replace_child(var, new_var)
                    # преобразование в функцию с сохранением этой переменной как одной из ветвей
                    elif r.random() < MUT_PROB_VAR_TO_FUNC:
                        new_func = Population.create_leaf_or_func(
                            self.values, only_func=True
                        )
                        if isinstance(new_func, UnoFunc):
                            child_to_remove = new_func.central_child
                        elif isinstance(new_func, DuoFunc):
                            child_to_remove = (
                                new_func.right_child
                                if r.random() < 0.5
                                else new_func.left_child
                            )
                        else:
                            raise
                        if not isinstance(
                            new_item, Variable
                        ):  # если не единственный узел в дереве
                            new_item.replace_child(var, new_func)
                        else:
                            new_item = new_func
                        new_item.replace_child(child_to_remove, var)  # type: ignore
                for func in self.nodes_walkthrough(new_item, filter_type=Node):
                    if not new_item.is_in(func):  # если уже нет этого узла в дереве
                        continue
                    # включение в новую функцию как одного из потомков
                    if r.random() < MUT_PROB_FUNC_TO_CHILD:
                        new_func = Population.create_leaf_or_func(
                            self.values, only_func=True
                        )
                        if isinstance(new_func, UnoFunc):
                            child_to_remove = new_func.central_child
                        elif isinstance(new_func, DuoFunc):
                            child_to_remove = (
                                new_func.right_child
                                if r.random() < 0.5
                                else new_func.left_child
                            )
                        else:
                            raise
                        if new_item.id != func.id:  # если не первый узел в дереве
                            new_item.replace_child(func, new_func)
                        else:
                            new_item = new_func
                        new_item.replace_child(child_to_remove, func)  # type: ignore
                    # вместо операции остается центральный потомок либо один из двух потомков
                    if r.random() < MUT_PROB_LEAVE_CHILD:
                        if isinstance(func, UnoFunc):
                            child_to_inplace = copy.deepcopy(
                                func.central_child
                            )  # не уверен, что нужен deepcopy
                        elif isinstance(func, DuoFunc):
                            child_to_inplace = copy.deepcopy(
                                func.right_child
                                if r.random() < 0.5
                                else func.left_child
                            )
                        else:
                            raise
                        if new_item.id != func.id:  # если не первый узел в дереве
                            new_item.replace_child(func, child_to_inplace)
                        else:
                            new_item = child_to_inplace  # type: ignore
                    # операнды меняются местами
                    if r.random() < MUT_PROB_OPERANDS_CHANGE and isinstance(
                        func, DuoFunc
                    ):
                        if func.right_child is None or func.left_child is None:
                            raise
                        copy_of_child = copy.deepcopy(func.right_child)
                        new_item.replace_child(func.right_child, func.left_child)
                        func.right_child.id = (
                            uuid.uuid1()
                        )  # обновляем айдишник чтобы не зацепить
                        new_item.replace_child(func.left_child, copy_of_child)
                    # заменяем тип функции
                    if r.random() < MUT_PROB_CHANGE_FUNC_TYPE:
                        if isinstance(func, DuoFunc):
                            new_item.change_func_type(func, r.choice(DUO_FUNCS))
                        elif isinstance(func, UnoFunc):
                            new_item.change_func_type(func, r.choice(UNO_FUNCS))
                    # заменяется класс функции
                    if r.random() < MUT_PROB_CHANGE_FUNC_CLASS:
                        if isinstance(func, DuoFunc):
                            child_to_save = copy.deepcopy(
                                func.right_child
                                if r.random() < 0.5
                                else func.left_child
                            )
                            new_func = Population.create_leaf_or_func(
                                self.values, only_func=True, need_type="uno"
                            )
                            if isinstance(new_func, UnoFunc):
                                child_to_replace = new_func.central_child
                            else:
                                raise
                        elif isinstance(func, UnoFunc):
                            child_to_save = copy.deepcopy(func.central_child)
                            new_func = Population.create_leaf_or_func(
                                self.values, only_func=True, need_type="duo"
                            )
                            child_to_replace = (
                                new_func.right_child  # type: ignore
                                if r.random() < 0.5
                                else new_func.left_child  # type: ignore
                            )
                        else:
                            raise
                        if new_item.id != func.id:
                            new_item.replace_child(func, new_func)
                        else:
                            new_item = new_func
                        new_item.replace_child(child_to_replace, child_to_save)  # type: ignore
            else:
                ...
            new_item = self.tree_shrink(new_item)
            new_items.append(new_item)
        return new_items

    def tree_shrink(
        self, item: t.Union[Constant, Variable, Node], max_depth: int = 5
    ) -> t.Union[Constant, Variable, Node]:
        """
        Оптимизация дерева, схлопывание функций только с константами, ограничение глубины деревьев
        :param item:
        :param max_depth:
        :return:
        """
        # TODO: пока что только ограничение глубины, потом сделать схлопывание
        new_item = copy.deepcopy(item)
        if max_depth < 2:
            raise
        #
        try:
            if new_item.depth() >= 10:
                return Population.create_leaf(self.values)
        except:
            return Population.create_leaf(self.values)

        if new_item.depth() <= max_depth:
            return new_item
        else:
            for node in self.nodes_walkthrough(new_item):
                if not new_item.is_in(node):  # если уже нет этого узла в дереве
                    continue
                if node.current_depth == max_depth and (
                    isinstance(node, DuoFunc) or isinstance(node, UnoFunc)
                ):
                    new_leaf = Population.create_leaf(self.values)
                    new_item.replace_child(node, new_leaf)
                # elif node.current_depth > max_depth:
                #     ...
        return new_item

    def evolve(self) -> None:
        count = 0
        best_score = self.population.best_score
        while best_score > 0.15:
            new_population = []
            best_items = self.population.get_best_items()
            new_population += best_items
            new_population += self.crossingover(best_items)
            new_population += self.mutation(new_population, rate=0.2)
            new_population += Population(self.values, self.questions, self.answers).items
            print(len(new_population))
            self.population = Population(
                self.values, self.questions, self.answers, items=new_population
            )
            best_score = self.population.best_score
            count += 1
            if count % 2 == 0:
                print(f"Best score: {best_score}, count: {count}")
        print('*********')
        print('*********')
        print(f"Best score: {best_score}, count: {count}")

        it = self.population.get_best_items(n=1)[0]
        print(F'best item: {it}')

        print(self.population.get_score(it, debug=True))


if __name__ == "__main__":
    # simple function: 1 + b * c
    questions, answers = [], []
    for i in range(10):
        for j in range(10):
            questions.append({"a": i/10, "b": j/10})
            answers.append(1 + i * j / 100)
    p = Population(["a", "b"], questions, answers)
    ge = GenomeEvolution(p.values, p.questions, p.answers)
    ge.evolve()
    print("Done")

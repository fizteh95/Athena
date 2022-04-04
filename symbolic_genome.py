import typing as t
import random as r

import symbolic as sym


UNO_FUNCS = ['sin', 'cos', 'lg', 'ln']
DUO_FUNCS = ['+', '-', '*', '/', '**']

INIT_NUMBER = 100
PROB_LEAF_CREATE = 0.7
# PROB_CONST_CREATE = 0.5
PROB_VAR_CREATE = 0.5
PROB_DUO_CREATE = 0.7
# PROB_UNO_CREATE = 0.1


class Population:
    def __init__(self, values: t.Dict, answers: t.List, items: t.List = None):
        if items is None:
            self.items = self.create_random()
        else:
            self.items = items
        self.values = values
        self.answers = answers

    def create_leaf(self):
        if r.random() < PROB_VAR_CREATE:
            node = sym.Variable(r.choice(list(self.values.keys())))
        else:
            node = sym.Constant(r.uniform(-100, 100))
        return node

    def create_node(self, root):
        if isinstance(root, sym.UnoFunc):
            if r.random < PROB_LEAF_CREATE:
                node = self.create_leaf()
                root.add_central(node)
                return root
            else:
                if r.random() < PROB_DUO_CREATE:
                    node = sym.DuoFunc(r.choice(DUO_FUNCS))
                else:
                    node = sym.UnoFunc(r.choice(UNO_FUNCS))
                updated_node = self.create_node(node)
                root.add_central(updated_node)
                return root
        elif isinstance(root, sym.DuoFunc):
            pass


    def create_random(self):
        result = []
        for _ in range(INIT_NUMBER):
            if r.random() < PROB_LEAF_CREATE:
                root = self.create_leaf()
                result.append(root)
            else:
                if r.random() < PROB_DUO_CREATE:
                    root = sym.UnoFunc(r.choice(DUO_FUNCS))
                    # left
                    if r.random() < PROB_LEAF_CREATE:
                        root.add_left(self.create_leaf())
                    else:
                        pass
                    # right
                    if r.random() < PROB_LEAF_CREATE:
                        root.add_right(self.create_leaf())
                    else:
                        pass
                    result.append(root)
                else:
                    root = sym.UnoFunc(r.choice(UNO_FUNCS))
                    if r.random() < PROB_LEAF_CREATE:
                        root.add_central(self.create_leaf())
                    else:
                        pass
                    result.append(root)

        return []

    def get_score(self, item):
        ...
        return 0

    def sort_population(self):
        ...
        return []

    def get_best_items(self, n=0.2):
        sorted_population = self.sort_population()
        return sorted_population[:int(len(sorted_population) * n)]

    @property
    def best_score(self):
        sorted_population = self.sort_population()
        return get_score(sorted_population[0])


class GenomeEvolution:
    def __init__(self, values: t.Dict, answers: t.List):
        self.answers = answers
        self.population = Population(values, answers)

    def crossingover(self, items):
        ...
        return []

    def mutation(self, items):
        ...
        return []

    def evolute(self):
        count = 0
        best_score = self.population.best_score
        while best_score < 0.95:
            new_population = []
            best_items = self.population.get_best_items()
            new_population += best_items
            new_population += self.crossingover(best_items)
            new_population += self.mutation(new_population, rate=0.2)
            self.population = Population(values, answers, items=new_population)
            best_score = self.population.best_score
            count += 1
            if count % 10 == 0:
                print(f'Best score: {best_score}, count: {count}')


if __name__ == "__main__":
    print('Done')
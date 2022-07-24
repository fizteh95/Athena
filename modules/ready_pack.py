import graphviz
from gplearn.genetic import SymbolicRegressor


# simple function: 1 + b * c
questions, answers = [], []
for i in range(10):
    for j in range(10):
        questions.append([i/10, j/10])
        answers.append(1 + i * j / 100)


est_gp = SymbolicRegressor(population_size=5000,
                           generations=20, stopping_criteria=0.01,
                           p_crossover=0.7, p_subtree_mutation=0.1,
                           p_hoist_mutation=0.05, p_point_mutation=0.1,
                           max_samples=0.9, verbose=1,
                           parsimony_coefficient=0.01, random_state=0)
est_gp.fit(questions, answers)

print(est_gp._program)

dot_data = est_gp._program.export_graphviz()
graph = graphviz.Source(dot_data)
graph.render(directory='doctest-output', view=True)

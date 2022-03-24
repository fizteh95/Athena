import random as r
import string
import typing as t


class Population:
    def __init__(self, members: t.List, example=None):
        self.members = members
        self.example = example

    def get_score(self, member):
        # TODO: make like lambda from init
        return sum(member[i] == self.example[i] for i in range(len(self.example))) / len(self.example)

    def best_score(self):
        best_score = 0
        for m in self.members:
            score = self.get_score(m)
            if score > best_score:
                best_score = score
        return best_score

    def get_best_members(self, number_of_members):
        sorted_members = sorted(self.members, key=lambda x: self.get_score(x), reverse=True)
        return sorted_members[:number_of_members]

    @property
    def best_member(self):
        return self.get_best_members(1)[0]


class GeneticAlgorithm:
    def __init__(self, phrase="To be or not to be..."):
        self.phrase = phrase
        self.letter_choice = string.ascii_uppercase + string.ascii_lowercase + ' ' + ',' + '.'

    def make_population(self, init_number=100):
        population = []
        for _ in range(init_number):
            new_string = ''.join(r.choice(self.letter_choice) for _ in range(len(self.phrase)))
            population.append(new_string)
        return Population(population, example=self.phrase)

    def crossingover(self, members):
        new_members = []
        for i in range(300):
            new_member = ''
            for j in range(len(self.phrase)):
                new_member += r.choice([x[j] for x in members])
            new_members.append(new_member)
        return new_members

    def mutation(self, members, percent):
        new_members = []
        for m in members:
            new_member = ''.join([x if r.random() > percent else r.choice(self.letter_choice) for x in m])
            new_members.append(new_member)
        return new_members

    def get_new_population(self, population: Population):
        new_members = []
        best_members = population.get_best_members(10)
        new_members += self.crossingover(best_members)
        new_members += self.mutation(new_members, 0.32)
        return Population(new_members, example=self.phrase)

    def evolute(self):
        count = 0
        population = self.make_population()
        while population.best_score() < 1:
            population = self.get_new_population(population)
            count += 1
            print(f'Population: {count}, best phrase: {population.best_member}')

        return population.best_member


if __name__ == "__main__":
    g = GeneticAlgorithm(phrase="To be or not to be...")
    phrase = g.evolute()
    print(f'Yohohoho, {phrase}')

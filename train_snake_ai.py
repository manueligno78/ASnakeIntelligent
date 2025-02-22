import numpy as np
import random
from snake_ai import NeuralNetwork
import pickle

class GeneticAlgorithm:
    def __init__(self, population_size=10, mutation_rate=0.1, hidden_size=10, activation_function="sigmoid", learning_rate=0.01):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        # Initialize population of neural networks
        self.population = [NeuralNetwork(hidden_size=hidden_size, activation_function=activation_function, learning_rate=learning_rate) for _ in range(population_size)]
        self.best_fitness = 0

    def evaluate_fitness(self, scores):
        return np.array(scores) / np.sum(scores)

    def select_parents(self, fitness_scores):
        return random.choices(self.population, weights=fitness_scores, k=2)

    def crossover(self, parent1, parent2):
        child = NeuralNetwork()
        genetic_code1 = parent1.get_genetic_code()
        genetic_code2 = parent2.get_genetic_code()
        child_genetic_code = {}
        for key in genetic_code1:
            child_genetic_code[key] = np.where(np.random.rand(*genetic_code1[key].shape) > 0.5, genetic_code1[key], genetic_code2[key])
        child.set_genetic_code(child_genetic_code)
        return child

    def mutate(self, neural_net):
        genetic_code = neural_net.get_genetic_code()
        for key in genetic_code:
            mutation_mask = np.random.rand(*genetic_code[key].shape) < self.mutation_rate
            genetic_code[key] += mutation_mask * np.random.randn(*genetic_code[key].shape)
        neural_net.set_genetic_code(genetic_code)

    def generate_next_generation(self, scores):
        fitness_scores = self.evaluate_fitness(scores)
        new_population = []
        for _ in range(self.population_size):
            parent1, parent2 = self.select_parents(fitness_scores)
            child = self.crossover(parent1, parent2)
            self.mutate(child)
            new_population.append(child)
        self.population = new_population
        self.best_fitness = max(scores)
        print(f"Best fitness in this generation: {self.best_fitness}")

    def save_population(self, filename="saved_model.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.population, f)
        print("Population saved successfully.")

    def load_population(self, filename="saved_model.pkl"):
        try:
            with open(filename, "rb") as f:
                self.population = pickle.load(f)
            print("Population loaded successfully.")
        except FileNotFoundError:
            print("No saved population found. Starting from scratch.")

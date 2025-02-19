import numpy as np
import random
from snake_ai import NeuralNetwork
import pickle

class GeneticAlgorithm:
    def __init__(self, population_size=10, mutation_rate=0.1):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = [NeuralNetwork() for _ in range(population_size)]
        self.best_fitness = 0

    def evaluate_fitness(self, scores):
        return np.array(scores) / np.sum(scores)  # Normalize fitness scores

    def select_parents(self, fitness_scores):
        return random.choices(self.population, weights=fitness_scores, k=2)

    def crossover(self, parent1, parent2):
        child = NeuralNetwork()
        
        child.weights_input_hidden = (parent1.weights_input_hidden + parent2.weights_input_hidden) / 2
        child.weights_hidden_output = (parent1.weights_hidden_output + parent2.weights_hidden_output) / 2
        
        return child

    def mutate(self, neural_net):
        if random.random() < self.mutation_rate:
            neural_net.weights_input_hidden += np.random.randn(*neural_net.weights_input_hidden.shape) * 0.1
            neural_net.weights_hidden_output += np.random.randn(*neural_net.weights_hidden_output.shape) * 0.1

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

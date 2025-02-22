import os
import json

POPULATION_SIZE = 100
GENERATIONS = 1500
HIDDEN_LAYER_SIZE = 10         # Changed from None to 10
ACTIVATION_FUNCTION = "sigmoid"
LEARNING_RATE = 0.01
MUTATION_RATE = 0.1
GRAPH_UPDATE_RATE = 0.0

WIDTH = 500
HEIGHT = 500
GRID_SIZE = 20

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

CONFIG_FILE = "config.json"

def load_config(filename=CONFIG_FILE):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            config = json.load(f)
        pop_size = config.get("POPULATION_SIZE", POPULATION_SIZE)
        gens = config.get("GENERATIONS", GENERATIONS)
        hidden_layer_size = config.get("HIDDEN_LAYER_SIZE", HIDDEN_LAYER_SIZE)
        activation_function = config.get("ACTIVATION_FUNCTION", ACTIVATION_FUNCTION)
        learning_rate = config.get("LEARNING_RATE", LEARNING_RATE)
        mutation_rate = config.get("MUTATION_RATE", MUTATION_RATE)
        graph_update_rate = config.get("GRAPH_UPDATE_RATE", GRAPH_UPDATE_RATE)
    else:
        pop_size, gens = POPULATION_SIZE, GENERATIONS
        hidden_layer_size = HIDDEN_LAYER_SIZE
        activation_function = ACTIVATION_FUNCTION
        learning_rate = LEARNING_RATE
        mutation_rate = MUTATION_RATE
        graph_update_rate = GRAPH_UPDATE_RATE
    return pop_size, gens, hidden_layer_size, activation_function, learning_rate, mutation_rate, graph_update_rate

def save_config(population_size, generations, hidden_layer_size, activation_function, learning_rate, mutation_rate, graph_update_rate, filename=CONFIG_FILE):
    config = {
        "POPULATION_SIZE": population_size,
        "GENERATIONS": generations,
        "HIDDEN_LAYER_SIZE": hidden_layer_size,
        "ACTIVATION_FUNCTION": activation_function,
        "LEARNING_RATE": learning_rate,
        "MUTATION_RATE": mutation_rate,
        "GRAPH_UPDATE_RATE": graph_update_rate
    }
    with open(filename, "w") as f:
        json.dump(config, f)
    print(f"Updated settings: Population Size = {population_size}, Generations = {generations}, Hidden Layer Size = {hidden_layer_size}, Activation Function = {activation_function}, Learning Rate = {learning_rate}, Mutation Rate = {mutation_rate}, Graph Update Rate = {graph_update_rate}")
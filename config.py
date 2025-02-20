import os
import json
from constants import POPULATION_SIZE, GENERATIONS

CONFIG_FILE = "config.json"

def load_config(filename="config.json"):
    """Load configuration from config.json; fallback to defaults if not present."""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            config = json.load(f)
        pop_size = config.get("POPULATION_SIZE", POPULATION_SIZE)
        gens = config.get("GENERATIONS", GENERATIONS)
        hidden_layer_size = config.get("HIDDEN_LAYER_SIZE", None)
        activation_function = config.get("ACTIVATION_FUNCTION", None)
        learning_rate = config.get("LEARNING_RATE", None)
        mutation_rate = config.get("MUTATION_RATE", None)
    else:
        pop_size, gens = POPULATION_SIZE, GENERATIONS
        hidden_layer_size = None
        activation_function = None
        learning_rate = None
        mutation_rate = None
    return pop_size, gens, hidden_layer_size, activation_function, learning_rate, mutation_rate

def save_config(population_size, generations, hidden_layer_size, activation_function, learning_rate, mutation_rate, filename="config.json"):
    """Save the provided settings to config.json."""
    config = {
        "POPULATION_SIZE": population_size,
        "GENERATIONS": generations,
        "HIDDEN_LAYER_SIZE": hidden_layer_size,
        "ACTIVATION_FUNCTION": activation_function,
        "LEARNING_RATE": learning_rate,
        "MUTATION_RATE": mutation_rate
    }
    with open(filename, "w") as f:
        json.dump(config, f)
    print(f"Updated settings: Population Size = {population_size}, Generations = {generations}, Hidden Layer Size = {hidden_layer_size}, Activation Function = {activation_function}, Learning Rate = {learning_rate}, Mutation Rate = {mutation_rate}")
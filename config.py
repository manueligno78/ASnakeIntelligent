import os
import json
from constants import POPULATION_SIZE, GENERATIONS

CONFIG_FILE = "config.json"

def load_config():
    """Load configuration from config.json; fallback to defaults if not present."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        pop_size = config.get("POPULATION_SIZE", POPULATION_SIZE)
        gens = config.get("GENERATIONS", GENERATIONS)
    else:
        pop_size, gens = POPULATION_SIZE, GENERATIONS
    return pop_size, gens

def save_config(pop_val, gen_val):
    """Save the provided settings to config.json."""
    config = {"POPULATION_SIZE": pop_val, "GENERATIONS": gen_val}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
    print(f"Updated settings: Population Size = {pop_val}, Generations = {gen_val}")
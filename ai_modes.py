import msvcrt
from snake_game import SnakeGame
from train_snake_ai import GeneticAlgorithm
from ui import TrainingUI, EvolutionGraph
from config import load_config

def ai_play_snake():
    pop_size, _ = load_config()
    ga = GeneticAlgorithm(population_size=pop_size)
    try:
        ga.load_population("saved_model.pkl")
    except FileNotFoundError:
        print("No saved model found. Please run AI Learn first.")
        return
    best_snake = SnakeGame(ga.population[0])
    best_snake.play_best_snake()

def ai_learn():
    pop_size, gens = load_config()
    ga = GeneticAlgorithm(population_size=pop_size)
    ui = TrainingUI()
    graph = EvolutionGraph()

    try:
        ga.load_population("saved_model.pkl")
    except FileNotFoundError:
        print("No saved model found, training from scratch.")

    for generation in range(gens):
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\x1b':
                print("Training stopped by user.")
                break

        print(f"Generation {generation + 1}")
        scores = []
        for neural_net in ga.population:
            game = SnakeGame(neural_net)
            fitness = game.run()
            scores.append(fitness)
            print(f"Fitness: {fitness}")
        best_score = max(scores)
        avg_score = sum(scores) / len(scores)
        ui.update_ui(generation + 1, best_score, avg_score, ga.mutation_rate)
        graph.update_graph(generation + 1, best_score, avg_score)
        ga.generate_next_generation(scores)

    print("Training complete!")
    save_input = input("Do you want to save the model? (y/n): ")
    if save_input.lower() == "y":
        ga.save_population("saved_model.pkl")
        print("Model saved.")
    else:
        print("Model not saved.")

    print("Displaying evolution progress.")
    graph.plot_progress()
    print("Now playing the best-trained snake.")
    best_snake = SnakeGame(ga.population[0])
    best_snake.play_best_snake()
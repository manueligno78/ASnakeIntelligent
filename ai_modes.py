__all__ = ["ai_play_snake", "ai_learn", "training_menu_view_unified"]

import msvcrt
import random
import pygame
from snake_game import SnakeGame
from train_snake_ai import GeneticAlgorithm
from ui import EvolutionGraph
from config import load_config

def training_menu_view_unified(screen, clock, font, title_font, graph):
    # Definiamo i pulsanti e l'area per la view di fine training
    watch_button = pygame.Rect(50, 520, 150, 40)
    save_button = pygame.Rect(325, 520, 150, 40)
    continue_button = pygame.Rect(600, 520, 150, 40)
    message = "Training complete!"
    choice = None
    while choice is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choice = {"watch": False, "save": False}
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if watch_button.collidepoint(event.pos):
                    choice = {"watch": True, "save": False}
                elif save_button.collidepoint(event.pos):
                    choice = {"watch": False, "save": True}
                elif continue_button.collidepoint(event.pos):
                    choice = {"watch": False, "save": False}
        screen.fill((30, 30, 30))
        # Titolo
        title_surface = title_font.render("Training Complete", True, (255, 255, 255))
        screen.blit(title_surface, (screen.get_width()//2 - title_surface.get_width()//2, 20))
        # Messaggio
        msg_surface = font.render(message, True, (255, 255, 255))
        screen.blit(msg_surface, (screen.get_width()//2 - msg_surface.get_width()//2, 60))
        # Disegna il grafico aggiornato
        graph_area = pygame.Rect(50, 100, 700, 300)
        if hasattr(graph, "draw_graph"):
            graph.draw_graph(screen, graph_area)
        else:
            pygame.draw.rect(screen, (200,200,200), graph_area, 2)
            sample_text = font.render("Graph area", True, (255,255,255))
            screen.blit(sample_text, (graph_area.x + 10, graph_area.y + 10))
        # Disegna i pulsanti
        pygame.draw.rect(screen, (0,255,0), watch_button)
        watch_text = font.render("Watch Snake", True, (0,0,0))
        screen.blit(watch_text, (watch_button.x + 10, watch_button.y + 10))
        pygame.draw.rect(screen, (0,0,255), save_button)
        save_text = font.render("Save Model", True, (255,255,255))
        screen.blit(save_text, (save_button.x + 10, save_button.y + 10))
        pygame.draw.rect(screen, (200,200,200), continue_button)
        cont_text = font.render("Continue", True, (0,0,0))
        screen.blit(cont_text, (continue_button.x + 20, continue_button.y + 10))
        pygame.display.flip()
        clock.tick(30)
    return choice

def ai_play_snake():
    # Unpack 7 values; ignore graph_update_rate with a dummy variable
    pop_size, _, hidden_layer_size, activation_function, learning_rate, mutation_rate, _ = load_config()
    ga = GeneticAlgorithm(population_size=pop_size,
                          hidden_size=hidden_layer_size,
                          activation_function=activation_function,
                          learning_rate=learning_rate,
                          mutation_rate=mutation_rate)
    try:
        ga.load_population("saved_model.pkl")
    except FileNotFoundError:
        print("No saved model found. Please run AI Learn first.")
        return
    print("Genetic code:", ga.population[0].encode_genetic_code())
    snake_games = [SnakeGame(nn) for nn in ga.population]
    play_snake_with_network_visualization(snake_games)

def ai_learn():
    # Unpack 7 values; use graph_update_rate in aggregation
    pop_size, gens, hidden_layer_size, activation_function, learning_rate, mutation_rate, graph_update_rate = load_config()
    ga = GeneticAlgorithm(population_size=pop_size,
                          hidden_size=hidden_layer_size,
                          activation_function=activation_function,
                          learning_rate=learning_rate,
                          mutation_rate=mutation_rate)
    graph = EvolutionGraph()

    try:
        ga.load_population("saved_model.pkl")
    except FileNotFoundError:
        print("No saved model found, training from scratch.")

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Training Progress")
    font = pygame.font.Font(None, 30)
    title_font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    graph_rect = pygame.Rect(50, 80, 700, 300)
    info_y = 400

    stop_training = False
    # Determine window length for aggregation if graph_update_rate > 0
    window_length = 1 if graph_update_rate <= 0 else max(1, int(gens * graph_update_rate))
    # Temporary lists for window aggregation
    window_best = []
    window_avg = []
    
    for generation in range(gens):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Training interrupted by user.")
                    stop_training = True
                    break
        if stop_training:
            break
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
        # Append for aggregation
        window_best.append(best_score)
        window_avg.append(avg_score)
        # Update graph only if in realtime mode or end of aggregation window reached
        if graph_update_rate <= 0 or (generation + 1) % window_length == 0:
            # If aggregating, take max of best and average of avg over the window
            agg_best = max(window_best) if window_best else best_score
            agg_avg = sum(window_avg) / len(window_avg) if window_avg else avg_score
            graph.update_graph(generation + 1, agg_best, agg_avg)
            window_best = []
            window_avg = []
        ga.generate_next_generation(scores)

        screen.fill((30, 30, 30))
        # Title with total generations
        title_surface = title_font.render(f"Training - Generation {generation+1}/{gens}", True, (255,255,255))
        screen.blit(title_surface, (50, 20))
        # Format best score to two decimals
        info_surface = font.render(f"Best: {best_score:.2f}   Avg: {avg_score:.2f}", True, (255,255,255))
        screen.blit(info_surface, (50, info_y))
        config_surface = font.render(
            f"Pop: {pop_size}   LR: {learning_rate}   Mut: {mutation_rate}   Hidden: {hidden_layer_size}   Act: {activation_function}",
            True, (255,255,255))
        screen.blit(config_surface, (50, info_y + 30))
        if hasattr(graph, "draw_graph"):
            graph.draw_graph(screen, graph_rect)
        else:
            pygame.draw.rect(screen, (200,200,200), graph_rect, 2)
        pygame.display.flip()
        clock.tick(5)
    
    choice = training_menu_view_unified(screen, clock, font, title_font, graph)
    if choice.get("watch"):
        best_snake = SnakeGame(ga.population[0])
        best_snake.play_best_snake()
    if choice.get("save"):
        ga.save_population("saved_model.pkl")
    pygame.quit()
    from menu import main_menu
    main_menu()

# New function: combines snake game play with live network visualization.
def play_snake_with_network_visualization(snake_games):
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("AI Play Mode - Snake & Neural Network")
    clock = pygame.time.Clock()
    game_area = pygame.Rect(20, 20, 600, 560)
    network_area = pygame.Rect(640, 20, 340, 560)
    
    current_index = 0
    current_game = snake_games[current_index]
    game_running = True
    
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = False
                elif event.key == pygame.K_SPACE:
                    # Cycle to the next snake in the generation
                    current_index = (current_index + 1) % len(snake_games)
                    current_game = snake_games[current_index]
                    current_game.reset()
        if not current_game.move():
            current_game.reset()
        
        inputs = current_game.get_environment_data()
        if hasattr(current_game.neural_net, "get_activations"):
            activations = current_game.neural_net.get_activations(inputs)
        else:
            activations = generate_random_activations(current_game.neural_net)
            
        screen.fill((30, 30, 30))
        current_game.draw(screen.subsurface(game_area))
        draw_network_structure(screen.subsurface(network_area), current_game.neural_net, activations)
        
        # Overlay genetic fingerprint on top of network area
        font_fp = pygame.font.Font(None, 24)
        fingerprint = current_game.neural_net.get_genetic_fingerprint() if hasattr(current_game.neural_net, "get_genetic_fingerprint") else "N/A"
        fp_text = font_fp.render(f"GC: {fingerprint}", True, (255, 255, 255))
        screen.blit(fp_text, (network_area.x + 10, network_area.y + 10))
        
        pygame.display.flip()
        clock.tick(10)
    pygame.quit()
    from menu import main_menu
    main_menu()

# Update generate_random_activations to use dynamic sizes.
def generate_random_activations(neural_net):
    import random
    input_size = getattr(neural_net, "input_size", 6)
    hidden_size = getattr(neural_net, "hidden_size", 10)
    output_size = getattr(neural_net, "output_size", 4)
    return [
        [random.random() for _ in range(input_size)],   # Input layer
        [random.random() for _ in range(hidden_size)],  # Hidden layer
        [random.random() for _ in range(output_size)]   # Output layer
    ]

# Update draw_network_structure to dynamically derive layer sizes.
def draw_network_structure(surface, neural_net, activations=None):
    # Determine layer sizes dynamically
    if activations:
        layers = [len(layer) for layer in activations]
    else:
        layers = [
            getattr(neural_net, "input_size", 6),
            getattr(neural_net, "hidden_size", 10),
            getattr(neural_net, "output_size", 4)
        ]
    width, height = surface.get_size()
    surface.fill((50, 50, 50))
    layer_gap = width // (len(layers) + 1)
    coords = []  # Store centers of neurons per layer
    
    # Draw neurons and annotate bias (for hidden and output layers)
    for i, num_neurons in enumerate(layers):
        x = (i + 1) * layer_gap
        neuron_gap = height // (num_neurons + 1)
        layer_coords = []
        for j in range(num_neurons):
            y = (j + 1) * neuron_gap
            if activations and i < len(activations) and j < len(activations[i]):
                act = activations[i][j]
            else:
                act = 0.5
            color_intensity = max(0, min(255, int(act * 255)))
            neuron_color = (color_intensity, 100, 255 - color_intensity)
            pygame.draw.circle(surface, neuron_color, (x, y), 15)
            pygame.draw.circle(surface, (255, 255, 255), (x, y), 15, 2)
            
            # Annotate bias for hidden (i==1) and output (i==2) layers
            if i == 1 and hasattr(neural_net, "bias_hidden"):
                bias = neural_net.bias_hidden[j]
            elif i == 2 and hasattr(neural_net, "bias_output"):
                bias = neural_net.bias_output[j]
            else:
                bias = None
            if bias is not None:
                # Map bias to an inner circle thickness (positive: green, negative: red)
                bias_thickness = max(1, min(6, int(abs(bias) * 3)))
                bias_color = (0, 255, 0) if bias >= 0 else (255, 0, 0)
                pygame.draw.circle(surface, bias_color, (x, y), 5, bias_thickness)
            layer_coords.append((x, y))
        coords.append(layer_coords)

    # Draw dynamic lines between layers with weight-based styling and highlight high activation paths
    for i in range(len(coords) - 1):
        if i == 0 and hasattr(neural_net, "weights_input_hidden"):
            weight_matrix = neural_net.weights_input_hidden
        elif i == 1 and hasattr(neural_net, "weights_hidden_output"):
            weight_matrix = neural_net.weights_hidden_output
        else:
            weight_matrix = None

        for j, (x1, y1) in enumerate(coords[i]):
            for k, (x2, y2) in enumerate(coords[i+1]):
                if activations and i < len(activations) and j < len(activations[i]) and i+1 < len(activations) and k < len(activations[i+1]):
                    avg_activation = (activations[i][j] + activations[i+1][k]) / 2
                else:
                    avg_activation = 0.5
                intensity = max(0, min(255, int(avg_activation * 255)))
                # Use yellow if average activation is high
                if avg_activation > 0.75:
                    base_color = (255, 255, 0)  # yellow
                elif weight_matrix is not None:
                    weight = weight_matrix[j, k]
                    base_color = (0, 255, 0) if weight >= 0 else (255, 0, 0)
                else:
                    base_color = (intensity, 100, 255 - intensity)

                if weight_matrix is not None:
                    weight = weight_matrix[j, k]
                    thickness = max(1, min(3, int(abs(weight) * 2)))
                else:
                    thickness = 2
                pygame.draw.line(surface, base_color, (x1, y1), (x2, y2), thickness)
import pygame
from engine.game import SnakeGame   # updated import
from ai.genetic_algorithm import GeneticAlgorithm
from config.config import load_config
# You can import additional utilities if needed

def ai_play_snake():
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
        font_fp = pygame.font.Font(None, 24)
        fingerprint = current_game.neural_net.get_genetic_fingerprint() if hasattr(current_game.neural_net, "get_genetic_fingerprint") else "N/A"
        fp_text = font_fp.render(f"GC: {fingerprint}", True, (255, 255, 255))
        screen.blit(fp_text, (network_area.x + 10, network_area.y + 10))
        pygame.display.flip()
        clock.tick(10)
    # Remove quitting here so that the display remains active for main_menu()
    # pygame.quit() <-- removed
    # Instead simply return control so that main_menu() can reinitialize the display as needed

def generate_random_activations(neural_net):
    import random
    input_size = getattr(neural_net, "input_size", 6)
    hidden_size = getattr(neural_net, "hidden_size", 10)
    output_size = getattr(neural_net, "output_size", 4)
    return [
        [random.random() for _ in range(input_size)],
        [random.random() for _ in range(hidden_size)],
        [random.random() for _ in range(output_size)]
    ]

def draw_network_structure(surface, neural_net, activations=None):
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
    coords = []
    # First, compute neuron positions without drawing
    for i, num_neurons in enumerate(layers):
        x = (i + 1) * layer_gap
        neuron_gap = height // (num_neurons + 1)
        layer_coords = []
        for j in range(num_neurons):
            y = (j + 1) * neuron_gap
            layer_coords.append((x, y))
        coords.append(layer_coords)
    # Draw connecting lines
    for i in range(len(coords) - 1):
        if i == 0 and hasattr(neural_net, "weights_input_hidden"):
            weight_matrix = neural_net.weights_input_hidden
        elif i == 1 and hasattr(neural_net, "weights_hidden_output"):
            weight_matrix = neural_net.weights_hidden_output
        else:
            weight_matrix = None
        for j, (x1, y1) in enumerate(coords[i]):
            for k, (x2, y2) in enumerate(coords[i + 1]):
                if activations and i < len(activations) and j < len(activations[i]) and i + 1 < len(activations) and k < len(activations[i + 1]):
                    avg_activation = (activations[i][j] + activations[i + 1][k]) / 2
                else:
                    avg_activation = 0.5
                intensity = max(0, min(255, int(avg_activation * 255)))
                if avg_activation > 0.75:
                    base_color = (255, 255, 0)
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
    # Draw neuron nodes on top
    for i, num_neurons in enumerate(layers):
        if activations and i < len(activations):
            layer_acts = activations[i]
        else:
            layer_acts = [0.5] * num_neurons
        for j, (x, y) in enumerate(coords[i]):
            act = layer_acts[j] if j < len(layer_acts) else 0.5
            color_intensity = max(0, min(255, int(act * 255)))
            neuron_color = (color_intensity, 100, 255 - color_intensity)
            pygame.draw.circle(surface, neuron_color, (x, y), 15)
            pygame.draw.circle(surface, (255, 255, 255), (x, y), 15, 2)
            if i == 1 and hasattr(neural_net, "bias_hidden"):
                bias = neural_net.bias_hidden[j]
            elif i == 2 and hasattr(neural_net, "bias_output"):
                bias = neural_net.bias_output[j]
            else:
                bias = None
            if bias is not None:
                bias_thickness = max(1, min(6, int(abs(bias) * 3)))
                bias_color = (0, 255, 0) if bias >= 0 else (255, 0, 0)
                pygame.draw.circle(surface, bias_color, (x, y), 5, bias_thickness)

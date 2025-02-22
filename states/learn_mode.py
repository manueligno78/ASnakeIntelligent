import pygame
import msvcrt
import time  # NEW: for timing generations
import pickle  # NEW: for saving best performer
from engine.game import SnakeGame   # updated import
from ai.genetic_algorithm import GeneticAlgorithm
from ui.evolution_graph import EvolutionGraph
from config.config import load_config

def training_menu_view_unified(screen, clock, font, title_font, graph):
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
        title_surface = title_font.render("Training Complete", True, (255, 255, 255))
        screen.blit(title_surface, (screen.get_width()//2 - title_surface.get_width()//2, 20))
        msg_surface = font.render(message, True, (255, 255, 255))
        screen.blit(msg_surface, (screen.get_width()//2 - msg_surface.get_width()//2, 60))
        graph_area = pygame.Rect(50, 100, 700, 300)
        if hasattr(graph, "draw_graph"):
            graph.draw_graph(screen, graph_area)
        else:
            pygame.draw.rect(screen, (200,200,200), graph_area, 2)
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

def ai_learn():
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
    window_length = 1 if graph_update_rate <= 0 else max(1, int(gens * graph_update_rate))
    window_best = []
    window_avg = []
    
    # NEW: Initialize variables for extra info.
    max_best = 0
    max_best_avg = 0
    best_net = None          # NEW: store best performing neural net
    total_gen_time = 0
    last_gen_time = 0

    for generation in range(gens):
        start_time = time.time()  # NEW: Generation start time.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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
            #print(f"Fitness: {fitness}")
        best_score = max(scores)
        avg_score = sum(scores) / len(scores)
        # Update max values; also store best_net when a new max is achieved.
        if best_score > max_best:
            max_best = best_score
            # Assume each game is run with a specific neural_net; here, pick the one that gave best_score.
            best_net = ga.population[scores.index(best_score)]
        if avg_score > max_best_avg:
            max_best_avg = avg_score
        
        last_gen_time = time.time() - start_time  # NEW: Compute generation time.
        total_gen_time += last_gen_time
        mean_time = total_gen_time / (generation + 1)  # NEW: Mean generation time.
        
        if graph_update_rate <= 0 or (generation + 1) % window_length == 0:
            agg_best = max(window_best) if window_best else best_score
            agg_avg = sum(window_avg) / len(window_avg) if window_avg else avg_score
            graph.update_graph(generation + 1, agg_best, agg_avg)
            window_best = []
            window_avg = []
        ga.generate_next_generation(scores)

        screen.fill((30, 30, 30))
        title_surface = title_font.render(f"Training - Generation {generation+1}/{gens}", True, (255,255,255))
        screen.blit(title_surface, (50, 20))
        info_surface = font.render(f"Best: {best_score:.2f}   Avg: {avg_score:.2f}", True, (255,255,255))
        screen.blit(info_surface, (50, info_y))
        config_surface = font.render(f"Pop: {pop_size}   LR: {learning_rate}   Mut: {mutation_rate}   Hidden: {hidden_layer_size}   Act: {activation_function}", True, (255,255,255))
        screen.blit(config_surface, (50, info_y + 30))
        # NEW: Render additional timing and max score info.
        timing_surface = font.render(f"Last Gen Time: {last_gen_time:.2f}s   Mean Time: {mean_time:.2f}s", True, (255,255,255))
        screen.blit(timing_surface, (50, info_y + 60))
        extra_surface = font.render(f"Max Best: {max_best:.2f}   Max Avg: {max_best_avg:.2f}", True, (255,255,255))
        screen.blit(extra_surface, (50, info_y + 90))
        # NEW: Use get_genetic_fingerprint to display the best performer's genetic fingerprint.
        if best_net is not None and hasattr(best_net, "get_genetic_fingerprint"):
            fingerprint = best_net.get_genetic_fingerprint()
            code_surface = font.render("Code: " + fingerprint, True, (255,255,255))
            screen.blit(code_surface, (50, info_y + 120))
            # NEW: Render genetic color snake representation for best performer.
            if hasattr(best_net, "get_genetic_color_array"):
                colors = best_net.get_genetic_color_array()
                start_x = 50
                snake_y = info_y + 150
                piece_width = 20
                piece_height = 10
                for i, color in enumerate(colors):
                    rect_piece = pygame.Rect(start_x + i * (piece_width + 2), snake_y, piece_width, piece_height)
                    pygame.draw.rect(screen, color, rect_piece)
        if hasattr(graph, "draw_graph"):
            graph.draw_graph(screen, graph_rect)
        else:
            pygame.draw.rect(screen, (200,200,200), graph_rect, 2)
        pygame.display.flip()
        clock.tick(5)
    
    choice = training_menu_view_unified(screen, clock, font, title_font, graph)
    if choice.get("watch"):
        from states.play_mode import ai_play_snake
        ai_play_snake()
    if choice.get("save"):
        ga.save_population("saved_model.pkl")
        # NEW: save the best performer as a pickle file if possible.
        if best_net is not None:
            with open("c:/Users/manue/Desktop/repositories/snake2/best_performer.pkl", "wb") as f:
                pickle.dump(best_net, f)
            print("Best performer saved to best_performer.pkl")
    return

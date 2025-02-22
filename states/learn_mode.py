import pygame
import msvcrt
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
    
    for generation in range(gens):
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
            print(f"Fitness: {fitness}")
        best_score = max(scores)
        avg_score = sum(scores) / len(scores)
        window_best.append(best_score)
        window_avg.append(avg_score)
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
        if hasattr(graph, "draw_graph"):
            graph.draw_graph(screen, graph_rect)
        else:
            pygame.draw.rect(screen, (200,200,200), graph_rect, 2)
        pygame.display.flip()
        clock.tick(5)
    
    choice = training_menu_view_unified(screen, clock, font, title_font, graph)
    if choice.get("watch"):
        # Instead of launching a new view, reconnect to the same AI Play mode view:
        from states.play_mode import ai_play_snake
        ai_play_snake()
    if choice.get("save"):
        ga.save_population("saved_model.pkl")
    # Do not call pygame.quit() here
    return  # Simply return to allow main_menu() to be re-called from the top-level.

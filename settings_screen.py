import pygame
from config import load_config, save_config

def settings():
    # Import locale per eliminare il problema della circular import
    from menu import main_menu

    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    font = pygame.font.Font(None, 24)  # Reduced font size
    title_font = pygame.font.Font(None, 36)  # Larger font for title
    config = load_config()
    population_size, generations, hidden_layer_size, activation_function, learning_rate, mutation_rate = config

    input_boxes = [
        {"label": "Population Size", "value": str(population_size), "rect": pygame.Rect(250, 50, 140, 32)},
        {"label": "Generations", "value": str(generations), "rect": pygame.Rect(250, 100, 140, 32)},
        {"label": "Hidden Layer Size", "value": str(hidden_layer_size), "rect": pygame.Rect(250, 150, 140, 32)},
        {"label": "Learning Rate", "value": str(learning_rate), "rect": pygame.Rect(250, 250, 140, 32)},
        {"label": "Mutation Rate", "value": str(mutation_rate), "rect": pygame.Rect(250, 300, 140, 32)}
    ]

    activation_functions = ["sigmoid", "relu"]
    activation_index = activation_functions.index(activation_function)
    activation_rect = pygame.Rect(250, 200, 140, 32)

    save_button = pygame.Rect(50, 400, 100, 40)
    back_button = pygame.Rect(200, 400, 100, 40)

    active_box = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for box in input_boxes:
                    if box["rect"].collidepoint(event.pos):
                        active_box = box
                        break
                if activation_rect.collidepoint(event.pos):
                    activation_index = (activation_index + 1) % len(activation_functions)
                if save_button.collidepoint(event.pos):
                    save_config(
                        int(input_boxes[0]["value"]),
                        int(input_boxes[1]["value"]),
                        int(input_boxes[2]["value"]),
                        activation_functions[activation_index],
                        float(input_boxes[3]["value"]),
                        float(input_boxes[4]["value"])
                    )
                    print("Settings saved.")
                    running = False  # Close settings screen and return to main menu
                    main_menu()      # Return to main menu
                if back_button.collidepoint(event.pos):
                    running = False  # Close settings screen without saving
                    main_menu()      # Return to main menu
            elif event.type == pygame.KEYDOWN:
                if active_box:
                    if event.key == pygame.K_RETURN:
                        active_box = None
                    elif event.key == pygame.K_BACKSPACE:
                        active_box["value"] = active_box["value"][:-1]
                    else:
                        active_box["value"] += event.unicode

        screen.fill((30, 30, 30))

        # Draw title
        title_surface = title_font.render("Settings", True, (255, 255, 255))
        screen.blit(title_surface, (screen.get_width() // 2 - title_surface.get_width() // 2, 10))

        for box in input_boxes:
            pygame.draw.rect(screen, (255, 255, 255), box["rect"], 2)
            text_surface = font.render(box["value"], True, (255, 255, 255))
            screen.blit(text_surface, (box["rect"].x + 5, box["rect"].y + 5))
            label_surface = font.render(box["label"], True, (255, 255, 255))
            screen.blit(label_surface, (box["rect"].x - 200, box["rect"].y + 5))  # Increased horizontal space

        # Draw activation function selection
        pygame.draw.rect(screen, (255, 255, 255), activation_rect, 2)
        activation_surface = font.render(activation_functions[activation_index], True, (255, 255, 255))
        screen.blit(activation_surface, (activation_rect.x + 5, activation_rect.y + 5))
        activation_label_surface = font.render("Activation Function", True, (255, 255, 255))
        screen.blit(activation_label_surface, (activation_rect.x - 200, activation_rect.y + 5))  # Increased horizontal space

        # Draw buttons
        pygame.draw.rect(screen, (0, 255, 0), save_button)
        save_text = font.render("Save", True, (0, 0, 0))
        screen.blit(save_text, (save_button.x + 20, save_button.y + 10))

        pygame.draw.rect(screen, (255, 0, 0), back_button)
        back_text = font.render("Back", True, (0, 0, 0))
        screen.blit(back_text, (back_button.x + 20, back_button.y + 10))

        pygame.display.flip()

    pygame.quit()
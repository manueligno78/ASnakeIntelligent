import pygame
from config import load_config, save_config
from constants import WIDTH, HEIGHT, BLACK, WHITE, GRAY

def settings():
    pop_size, gens = load_config()
    population_size = str(pop_size)
    generations = str(gens)
    active_field = None  # "population" or "generations"

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Settings")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    input_rect_pop = pygame.Rect(WIDTH//2 - 100, 150, 200, 40)
    input_rect_gen = pygame.Rect(WIDTH//2 - 100, 250, 200, 40)

    running = True
    while running:
        screen.fill(BLACK)
        title = font.render("Settings", True, WHITE)
        instructions = font.render("Click field, type number, ENTER to save, ESC to cancel", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        screen.blit(instructions, (WIDTH//2 - instructions.get_width()//2, 90))

        label_pop = font.render("Population Size:", True, WHITE)
        label_gen = font.render("Generations:", True, WHITE)
        screen.blit(label_pop, (input_rect_pop.x, input_rect_pop.y - 40))
        screen.blit(label_gen, (input_rect_gen.x, input_rect_gen.y - 40))

        pygame.draw.rect(screen, GRAY if active_field == "population" else WHITE, input_rect_pop, 2)
        pygame.draw.rect(screen, GRAY if active_field == "generations" else WHITE, input_rect_gen, 2)

        pop_text = font.render(population_size, True, WHITE)
        gen_text = font.render(generations, True, WHITE)
        screen.blit(pop_text, (input_rect_pop.x + 10, input_rect_pop.y + 5))
        screen.blit(gen_text, (input_rect_gen.x + 10, input_rect_gen.y + 5))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect_pop.collidepoint(event.pos):
                    active_field = "population"
                elif input_rect_gen.collidepoint(event.pos):
                    active_field = "generations"
                else:
                    active_field = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
                elif event.key == pygame.K_RETURN:
                    try:
                        pop_val = int(population_size) if population_size != "" else 0
                        gen_val = int(generations) if generations != "" else 0
                    except ValueError:
                        print("Invalid number format.")
                        continue
                    save_config(pop_val, gen_val)
                    running = False
                    break
                elif active_field:
                    if event.key == pygame.K_BACKSPACE:
                        if active_field == "population":
                            population_size = population_size[:-1]
                        elif active_field == "generations":
                            generations = generations[:-1]
                    elif event.unicode.isdigit():
                        if active_field == "population":
                            population_size += event.unicode
                        elif active_field == "generations":
                            generations += event.unicode

        clock.tick(30)

    pygame.quit()
    from menu import main_menu
    main_menu()
import pygame
from constants import WIDTH, HEIGHT, GRID_SIZE, WHITE, BLACK, GREEN, RED
from snake_game import SnakeGame

def manual_play():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Manual Snake")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)

    # Create a SnakeGame instance without AI (dummy neural network)
    game = SnakeGame(neural_net=None)
    game.reset()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()
        pressed_keys = []
        if keys[pygame.K_UP]:
            pressed_keys.append((0, -GRID_SIZE))
        if keys[pygame.K_DOWN]:
            pressed_keys.append((0, GRID_SIZE))
        if keys[pygame.K_LEFT]:
            pressed_keys.append((-GRID_SIZE, 0))
        if keys[pygame.K_RIGHT]:
            pressed_keys.append((GRID_SIZE, 0))
        
        if len(pressed_keys) == 1:
            new_direction = pressed_keys[0]
            if new_direction != (-game.direction[0], -game.direction[1]):
                game.direction = new_direction

        head = (game.snake[0][0] + game.direction[0],
                game.snake[0][1] + game.direction[1])
        if head in game.snake or head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            running = False
        else:
            game.snake.insert(0, head)
            if head == game.food:
                game.food = game.spawn_food()
                game.score += 1
                game.energy = 100
            else:
                game.snake.pop()

        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, (*game.food, GRID_SIZE, GRID_SIZE))
        for segment in game.snake:
            pygame.draw.rect(screen, GREEN, (*segment, GRID_SIZE, GRID_SIZE))

        score_text = font.render("Score: " + str(game.score), True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
    from menu import main_menu
    main_menu()
import pygame
import random

# Game settings
WIDTH, HEIGHT = 500, 500
GRID_SIZE = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("AI Snake Game")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.snake = [(WIDTH // (2 * GRID_SIZE) * GRID_SIZE, HEIGHT // (2 * GRID_SIZE) * GRID_SIZE)]
        self.direction = (GRID_SIZE, 0)
        self.food = self.spawn_food()
        self.score = 0

    def spawn_food(self):
        while True:
            food = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                    random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)
            if food not in self.snake:
                return food

    def move(self):
        head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
        
        # Check collisions
        if head in self.snake or head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            self.reset()
            return
        
        self.snake.insert(0, head)
        if head == self.food:
            self.food = self.spawn_food()
            self.score += 1
        else:
            self.snake.pop()
    
    def render(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, RED, (*self.food, GRID_SIZE, GRID_SIZE))
        for segment in self.snake:
            pygame.draw.rect(self.screen, GREEN, (*segment, GRID_SIZE, GRID_SIZE))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != (0, GRID_SIZE):
                        self.direction = (0, -GRID_SIZE)
                    elif event.key == pygame.K_DOWN and self.direction != (0, -GRID_SIZE):
                        self.direction = (0, GRID_SIZE)
                    elif event.key == pygame.K_LEFT and self.direction != (GRID_SIZE, 0):
                        self.direction = (-GRID_SIZE, 0)
                    elif event.key == pygame.K_RIGHT and self.direction != (-GRID_SIZE, 0):
                        self.direction = (GRID_SIZE, 0)
            
            self.move()
            self.render()
            self.clock.tick(10)

        pygame.quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()

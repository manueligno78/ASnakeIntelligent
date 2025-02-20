import pygame
import random
import numpy as np
from constants import WIDTH, HEIGHT, GRID_SIZE, WHITE, GREEN, RED, BLACK

class SnakeGame:
    def __init__(self, neural_net):
        self.neural_net = neural_net
        self.reset()

    def reset(self):
        self.snake = [(WIDTH // (2 * GRID_SIZE) * GRID_SIZE,
                       HEIGHT // (2 * GRID_SIZE) * GRID_SIZE)]
        self.direction = (GRID_SIZE, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.energy = 100
        self.steps = 0

    def spawn_food(self):
        while True:
            food = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                    random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)
            if food not in self.snake:
                return food

    def get_environment_data(self):
        head_x, head_y = self.snake[0]
        food_x, food_y = self.food
        obstacle_up = 1 if (head_y - GRID_SIZE < 0 or (head_x, head_y - GRID_SIZE) in self.snake) else 0
        obstacle_down = 1 if (head_y + GRID_SIZE >= HEIGHT or (head_x, head_y + GRID_SIZE) in self.snake) else 0
        obstacle_left = 1 if (head_x - GRID_SIZE < 0 or (head_x - GRID_SIZE, head_y) in self.snake) else 0
        obstacle_right = 1 if (head_x + GRID_SIZE >= WIDTH or (head_x + GRID_SIZE, head_y) in self.snake) else 0
        return np.array([(food_x - head_x) / WIDTH,
                         (food_y - head_y) / HEIGHT,
                         obstacle_up, obstacle_down, obstacle_left, obstacle_right])

    def move(self):
        inputs = self.get_environment_data()
        direction_index = self.neural_net.predict_direction(inputs)
        directions = [(0, -GRID_SIZE), (0, GRID_SIZE), (-GRID_SIZE, 0), (GRID_SIZE, 0)]
        if directions[direction_index] == (-self.direction[0], -self.direction[1]):
            direction_index = (direction_index + 2) % 4
        self.direction = directions[direction_index]

        head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
        if head in self.snake or head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return False

        self.snake.insert(0, head)
        if head == self.food:
            self.food = self.spawn_food()
            self.score += 1
            self.energy = 100
        else:
            self.snake.pop()
            self.energy -= 1

        self.steps += 1
        if self.energy <= 0:
            return False

        return True

    def run(self):
        while self.move():
            pass
        return self.score + (self.steps / 100)

    def play_best_snake(self):
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 15)
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            if not self.move():
                self.reset()

            screen.fill(BLACK)
            pygame.draw.rect(screen, RED, (*self.food, GRID_SIZE, GRID_SIZE))
            for segment in self.snake:
                pygame.draw.rect(screen, GREEN, (*segment, GRID_SIZE, GRID_SIZE))

            text = font.render("Press ESC to stop", True, WHITE)
            screen.blit(text, (10, 10))

            pygame.display.flip()
            clock.tick(10)
        pygame.quit()
        # Removed automatic call to main_menu()
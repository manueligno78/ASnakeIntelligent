# This module contains additional UI helper functions previously in ui.py.
# (Make sure it does not conflict with EvolutionGraph from evolution_graph.py)

def extra_ui_function():
    # ...existing code...
    pass

# Add any additional classes or functions needed for UI functionality.
import pygame
import matplotlib.pyplot as plt
import numpy as np

class TrainingUI:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(None, 30)
        self.width, self.height = 400, 300
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Training Stats")

    def update_ui(self, generation, best_score, avg_score, mutation_count):
        self.screen.fill((0, 0, 0))
        
        text_gen = self.font.render(f"Generation: {generation}", True, (255, 255, 255))
        text_best = self.font.render(f"Best Score: {best_score}", True, (255, 255, 255))
        text_avg = self.font.render(f"Avg Score: {avg_score:.2f}", True, (255, 255, 255))
        text_mut = self.font.render(f"Mutations: {mutation_count}", True, (255, 255, 255))
        
        self.screen.blit(text_gen, (20, 20))
        self.screen.blit(text_best, (20, 60))
        self.screen.blit(text_avg, (20, 100))
        self.screen.blit(text_mut, (20, 140))
        
        pygame.display.flip()

    def close(self):
        pygame.quit()

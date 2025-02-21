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

class EvolutionGraph:
    def __init__(self):
        self.generations = []
        self.best_scores = []
        self.avg_scores = []
    
    def update_graph(self, generation, best_score, avg_score):
        self.generations.append(generation)
        self.best_scores.append(best_score)
        self.avg_scores.append(avg_score)
    
    def draw_graph(self, surface, rect):
        pygame.draw.rect(surface, (255, 255, 255), rect, 2)
        if len(self.generations) < 2:
            font = pygame.font.Font(None, 24)
            msg = font.render("No data yet", True, (255,255,255))
            surface.blit(msg, (rect.x + 10, rect.y + 10))
            return

        min_score = 0  
        max_score = max(self.best_scores) if self.best_scores else 1
        score_range = max_score - min_score if max_score != min_score else 1
        count = len(self.generations)
        x_spacing = rect.width / (count - 1)

        # Draw horizontal ticks on y-axis
        num_ticks = 5
        tick_interval = score_range / num_ticks
        for i in range(num_ticks + 1):
            tick_value = min_score + i * tick_interval
            y = rect.y + rect.height - (tick_value / score_range * rect.height)
            pygame.draw.line(surface, (200,200,200), (rect.x - 5, y), (rect.x, y), 1)
            tick_label = pygame.font.Font(None, 20).render(f"{tick_value:.2f}", True, (255,255,255))
            surface.blit(tick_label, (rect.x - tick_label.get_width() - 10, y - tick_label.get_height()/2))

        points = []
        for i, score in enumerate(self.best_scores):
            x = rect.x + i * x_spacing
            y = rect.y + rect.height - ((score - min_score) / score_range * rect.height)
            points.append((x, y))
        pygame.draw.lines(surface, (0, 255, 0), False, points, 2)

        avg_points = []
        for i, score in enumerate(self.avg_scores):
            x = rect.x + i * x_spacing
            y = rect.y + rect.height - ((score - min_score) / score_range * rect.height)
            avg_points.append((x, y))
        pygame.draw.lines(surface, (255, 255, 0), False, avg_points, 2)
        
        # Draw labels for max and 0
        font_label = pygame.font.Font(None, 20)
        max_text = font_label.render(f"{max_score:.2f}", True, (255,255,255))
        zero_text = font_label.render("0", True, (255,255,255))
        surface.blit(max_text, (rect.x - max_text.get_width() - 5, rect.y - 5))
        surface.blit(zero_text, (rect.x - zero_text.get_width() - 5, rect.y + rect.height - zero_text.get_height()))

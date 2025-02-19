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
        # Enable interactive mode and create a figure
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.line_best, = self.ax.plot([], [], label="Best Score")
        self.line_avg, = self.ax.plot([], [], label="Average Score")
        self.ax.legend()
        self.ax.set_xlabel("Generation")
        self.ax.set_ylabel("Score")
        plt.show()

    def update_graph(self, gen, best, avg):
        self.generations.append(gen)
        self.best_scores.append(best)
        self.avg_scores.append(avg)
        self.line_best.set_data(self.generations, self.best_scores)
        self.line_avg.set_data(self.generations, self.avg_scores)
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.001)

    def plot_progress(self):
        # Optionally, if you wish to block at the end.
        plt.ioff()
        plt.show()

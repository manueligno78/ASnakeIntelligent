import pygame

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
        
        # Draw horizontal ticks
        num_ticks = 5
        tick_interval = score_range / num_ticks
        for i in range(num_ticks + 1):
            tick_value = min_score + i * tick_interval
            y = rect.y + rect.height - ((tick_value / score_range) * rect.height)
            pygame.draw.line(surface, (200,200,200), (rect.x - 5, y), (rect.x, y), 1)
            tick_label = pygame.font.Font(None, 20).render(f"{tick_value:.2f}", True, (255,255,255))
            surface.blit(tick_label, (rect.x - tick_label.get_width() - 10, y - tick_label.get_height()/2))
            
        # Plot best scores
        points = []
        for i, score in enumerate(self.best_scores):
            x = rect.x + i * x_spacing
            y = rect.y + rect.height - ((score - min_score) / score_range * rect.height)
            points.append((x, y))
        pygame.draw.lines(surface, (0, 255, 0), False, points, 2)

        # Plot average scores
        avg_points = []
        for i, score in enumerate(self.avg_scores):
            x = rect.x + i * x_spacing
            y = rect.y + rect.height - ((score - min_score) / score_range * rect.height)
            avg_points.append((x, y))
        pygame.draw.lines(surface, (255, 255, 0), False, avg_points, 2)

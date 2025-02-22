import pygame

def draw_input_box(screen, rect, text, font, color=(255,255,255)):
    pygame.draw.rect(screen, color, rect, 2)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (rect.x + 5, rect.y + 5))

def draw_label(screen, label, pos, font, color=(255,255,255)):
    label_surface = font.render(label, True, color)
    screen.blit(label_surface, pos)

import pygame
import sys
from states.play_mode import ai_play_snake
from states.learn_mode import ai_learn
from ui.settings_screen import settings
from states.manual_play import manual_play
from config.config import WIDTH, HEIGHT, WHITE, BLACK, GRAY
from utils.utils import draw_label

def exit_app():
    pygame.quit()
    sys.exit()

def get_display():
    surface = pygame.display.get_surface()
    if surface is None:
        surface = pygame.display.set_mode((WIDTH, HEIGHT))
    return surface

def main_menu():
    if not pygame.get_init():
        pygame.init()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    menu_items = [
        {"text": "Play Snake", "action": manual_play},
        {"text": "AI Play Snake", "action": ai_play_snake},
        {"text": "AI Learn", "action": ai_learn},
        {"text": "Settings", "action": settings},
        {"text": "Exit", "action": exit_app}
    ]

    running = True
    while running:
        screen = get_display()
        screen.fill(BLACK)
        
        title_text = font.render("Welcome to Snake AI", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 50))
        screen.blit(title_text, title_rect)

        menu_rects = []
        for index, item in enumerate(menu_items):
            mouse_pos = pygame.mouse.get_pos()
            dummy_rect = pygame.Rect(0, 150 + index * 50, WIDTH, 50)
            color = GRAY if dummy_rect.collidepoint(mouse_pos) else WHITE
            text_surface = font.render(item["text"], True, color)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, 150 + index * 50))
            screen.blit(text_surface, text_rect)
            menu_rects.append((text_rect, item["action"]))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit_app()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, action in menu_rects:
                    if rect.collidepoint(event.pos):
                        action()  # Call the state action.
                        pygame.time.wait(100)
                        pygame.event.clear()
                        break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        clock.tick(30)
    exit_app()

if __name__ == "__main__":
    main_menu()
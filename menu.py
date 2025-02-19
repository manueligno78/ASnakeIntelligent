import pygame
import sys
from play_modes import manual_play, ai_play_snake, ai_learn, settings
from constants import WIDTH, HEIGHT, WHITE, BLACK, GRAY

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Welcome to Snake AI")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    menu_items = [
        {"text": "Play Snake", "action": manual_play},
        {"text": "AI Play Snake", "action": ai_play_snake},
        {"text": "AI Learn", "action": ai_learn},
        {"text": "Settings", "action": settings},
    ]
    selected_index = None
    menu_rects = []
    running = True

    while running:
        screen.fill(BLACK)
        title_text = font.render("Welcome to Snake AI", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 50))
        screen.blit(title_text, title_rect)

        menu_rects.clear()
        for index, item in enumerate(menu_items):
            color = GRAY if selected_index == index else WHITE
            text_surface = font.render(item["text"], True, color)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, 150 + index * 50))
            screen.blit(text_surface, text_rect)
            menu_rects.append((text_rect, item["action"]))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                selected_index = None
                for i, (rect, _) in enumerate(menu_rects):
                    if rect.collidepoint(mouse_pos):
                        selected_index = i
                        break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and selected_index is not None:
                    action = menu_items[selected_index]["action"]
                    pygame.quit()  # close menu before calling action
                    action()
                    running = False
                    break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                break

        clock.tick(30)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()
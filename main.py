import pygame
from ui.menu import main_menu

if __name__ == "__main__":
    # Reinitialize pygame in case a submodule has closed the display.
    pygame.init()
    main_menu()

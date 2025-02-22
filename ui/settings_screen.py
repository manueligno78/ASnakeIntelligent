import pygame
from config.config import load_config, save_config
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from utils.utils import draw_input_box, draw_label

def open_model_menu():
    # Opens a dialog to choose to load a model file or wipe the existing model
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    choice = messagebox.askquestion("Model Options", "Load a model file? (Click 'Yes' to load, 'No' to wipe)")
    if choice == "yes":
        file_path = filedialog.askopenfilename(title="Select model file", filetypes=[("PKL files", "*.pkl")])
        if file_path:
            shutil.copy(file_path, "saved_model.pkl")
            print("Model loaded successfully.")
        else:
            print("No file selected.")
    else:
        if os.path.exists("saved_model.pkl"):
            os.remove("saved_model.pkl")
            print("Saved model wiped.")
        else:
            print("No saved model found to wipe.")
    root.destroy()

def settings():
    from ui.menu import main_menu

    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    font = pygame.font.Font(None, 24)
    title_font = pygame.font.Font(None, 36)
    config = load_config()
    population_size, generations, hidden_layer_size, activation_function, learning_rate, mutation_rate, graph_update_rate = config

    input_boxes = [
        {"label": "Population Size", "value": str(population_size), "rect": pygame.Rect(250, 50, 140, 32)},
        {"label": "Generations", "value": str(generations), "rect": pygame.Rect(250, 100, 140, 32)},
        {"label": "Hidden Layer Size", "value": str(hidden_layer_size), "rect": pygame.Rect(250, 150, 140, 32)},
        {"label": "Learning Rate", "value": str(learning_rate), "rect": pygame.Rect(250, 250, 140, 32)},
        {"label": "Mutation Rate", "value": str(mutation_rate), "rect": pygame.Rect(250, 300, 140, 32)},
        {"label": "Graph Update Rate", "value": str(graph_update_rate), "rect": pygame.Rect(250, 350, 140, 32)}
    ]
    
    activation_functions = ["sigmoid", "relu"]
    activation_index = activation_functions.index(activation_function)
    activation_rect = pygame.Rect(250, 200, 140, 32)

    # "Model" button is placed near the top for quick access.
    model_button = pygame.Rect(50, 400, 250, 40)
    # "Save" and "Back" buttons are grouped at the bottom.
    save_button = pygame.Rect(50, 460, 100, 40)
    back_button = pygame.Rect(200, 460, 100, 40)

    active_box = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for box in input_boxes:
                    if box["rect"].collidepoint(event.pos):
                        active_box = box
                        break
                if activation_rect.collidepoint(event.pos):
                    activation_index = (activation_index + 1) % len(activation_functions)
                if model_button.collidepoint(event.pos):
                    open_model_menu()
                if save_button.collidepoint(event.pos):
                    try:
                        pop_val = int(input_boxes[0]["value"]) if input_boxes[0]["value"].isdigit() else population_size
                        gens_val = int(input_boxes[1]["value"]) if input_boxes[1]["value"].isdigit() else generations
                        hidden_val = int(input_boxes[2]["value"]) if input_boxes[2]["value"].isdigit() else hidden_layer_size
                        lr_val = float(input_boxes[3]["value"]) if input_boxes[3]["value"].replace('.', '', 1).isdigit() else learning_rate
                        mut_val = float(input_boxes[4]["value"]) if input_boxes[4]["value"].replace('.', '', 1).isdigit() else mutation_rate
                        graph_val = float(input_boxes[5]["value"]) if input_boxes[5]["value"].replace('.', '', 1).isdigit() else graph_update_rate
                    except Exception as e:
                        print("Error converting input: ", e)
                        return
                    save_config(pop_val, gens_val, hidden_val, activation_functions[activation_index], lr_val, mut_val, graph_val)
                    print("Settings saved, exiting settings...")
                    running = False
                if back_button.collidepoint(event.pos):
                    print("Exiting settings (Back)")
                    running = False
            elif event.type == pygame.KEYDOWN:
                if active_box:
                    if event.key == pygame.K_RETURN:
                        active_box = None
                    elif event.key == pygame.K_BACKSPACE:
                        active_box["value"] = active_box["value"][:-1]
                    else:
                        active_box["value"] += event.unicode

        screen.fill((30, 30, 30))
        title_surface = title_font.render("Settings", True, (255, 255, 255))
        screen.blit(title_surface, (screen.get_width() // 2 - title_surface.get_width() // 2, 10))
        for box in input_boxes:
            draw_input_box(screen, box["rect"], box["value"], font)
            draw_label(screen, box["label"], (box["rect"].x - 200, box["rect"].y + 5), font)
        pygame.draw.rect(screen, (255, 255, 255), activation_rect, 2)
        activation_surface = font.render(activation_functions[activation_index], True, (255, 255, 255))
        screen.blit(activation_surface, (activation_rect.x + 5, activation_rect.y + 5))
        activation_label_surface = font.render("Activation Function", True, (255, 255, 255))
        screen.blit(activation_label_surface, (activation_rect.x - 200, activation_rect.y + 5))
        pygame.draw.rect(screen, (128, 128, 128), model_button)
        model_text = font.render("Model (Wipe/Load)", True, (0, 0, 0))
        screen.blit(model_text, (model_button.x + 10, model_button.y + 10))
        pygame.draw.rect(screen, (0, 255, 0), save_button)
        save_text = font.render("Save", True, (0, 0, 0))
        screen.blit(save_text, (save_button.x + 20, save_button.y + 10))
        pygame.draw.rect(screen, (255, 0, 0), back_button)
        back_text = font.render("Back", True, (0, 0, 0))
        screen.blit(back_text, (back_button.x + 20, back_button.y + 10))
        pygame.display.flip()
        pygame.time.wait(30)  # Short wait, if needed.
    pygame.event.clear()
    return
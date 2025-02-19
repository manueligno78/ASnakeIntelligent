# Snake AI

Snake AI is a project that implements a classic Snake game with additional features such as AI-controlled modes and a learning mode based on genetic algorithms. It is built using Python and Pygame.

## Features

- **Manual Play**: Play Snake manually using the arrow keys.
- **AI Play**: Watch the best-trained AI play the game.
- **AI Learn**: Train the AI using a genetic algorithm. Training progress is shown in real time.
- **Settings**: Configure parameters such as population size and the number of generations. Settings are persisted in a `config.json` file.

## Project Structure

- **constants.py**: Contains global settings and color definitions.
- **config.py**: Handles loading and saving configuration settings from/to `config.json`.
- **snake_game.py**: Implements the core Snake game logic.
- **manual_play.py**: Contains the function to play the game manually.
- **ai_modes.py**: Contains functions for AI Play and AI Learning modes.
- **settings_screen.py**: Implements the settings screen to adjust configuration values.
- **play_modes.py**: Aggregates different play mode functions for easy import.
- **menu.py**: Implements the main menu screen where you can select the game mode.
- **game.py**: Entry point of the application.
- **train_snake_ai.py**: (Assumed) Contains the implementation for the genetic algorithm and neural network training.
- **ui.py**: (Assumed) Contains the UI elements for displaying training progress and evolution graphs.
- **config.json**: Stores persistent configuration values (e.g., population size and generations).
- **README.md**: This file.

**Application Usage**
Main Menu: When you start the application, a main menu will appear with the following options:
Play Snake: Launches manual play.
AI Play Snake: Lets you watch the best AI-controlled game.
AI Learn: Starts the training process for the AI.
Settings: Opens the settings screen where you can adjust and save configuration parameters.
Manual Play: Use the arrow keys to control the snake. The game returns to the main menu when you quit.
AI Learning: Progress is displayed in real time through UI elements and an evolution graph. Press ESC during training to stop.
Settings: Click on a field (Population Size or Generations), edit the value, and press ENTER to save. Changes will persist in config.json.

**Contributing**
Feel free to fork the repository and submit pull requests.
For bug reports or feature requests, please open an issue on the repository.
License
This project is for educational purposes.

**Acknowledgements**
Built with Python and Pygame.
Inspired by classic Snake games and machine learning projects.

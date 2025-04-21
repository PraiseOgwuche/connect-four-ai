# Connect Four AI

An implementation of Connect Four with an AI opponent using minimax algorithm with alpha-beta pruning. Created as a final project for AI class.

## Features

- Terminal-based user interface
- Optional Pygame graphical interface
- AI opponent with three difficulty levels (Easy, Medium, Hard)
- Performance analysis of the AI's decision-making process
- Game statistics tracking

## Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/connect-four-ai.git
cd connect-four-ai

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Installing Pygame

If you want to use the graphical interface, you'll need to install Pygame:

```bash
pip install pygame
```

On macOS, you might need to install SDL dependencies first using Homebrew:

```bash
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
pip install pygame
```

## Running the Game

```bash
python main.py
```

This will prompt you to select either the terminal interface or the graphical interface (Pygame).

## How to Play

1. When you start the game, you'll be prompted to select a difficulty level:
   - **Easy**: The AI looks 2 moves ahead
   - **Medium**: The AI looks 4 moves ahead
   - **Hard**: The AI looks 6 moves ahead


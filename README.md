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

2. You play as 'X' and the AI plays as 'O'

3. During your turn, enter the column number (0-6) where you want to place your piece

4. After the AI's move, you'll see performance statistics about its decision-making process

5. The game continues until someone wins or the board is full (a draw)

6. At the end of the game, you can choose to play again

## Project Structure

- `src/game/board.py`: Connect Four game logic
- `src/ai/minimax.py`: AI implementation using minimax with alpha-beta pruning
- `src/ui/interface.py`: Terminal-based user interface
- `src/ui/pygame_interface.py`: Pygame-based graphical user interface
- `main.py`: Entry point to run the game
- `documentation.md`: Detailed documentation about the project

## Learning Outcomes Addressed

This project addresses the following course learning outcomes:

- **Search (#search)**: Implementation of the minimax algorithm with alpha-beta pruning to search the game tree
- **AI Logic (#ailogic)**: Logical evaluation of game states to determine the best move
- **AI Coding (#aicoding)**: Implementation of AI algorithms in Python

For more detailed information about the project, please refer to the `documentation.md` file.
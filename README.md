# Connect Four AI

As my final project for Introduction to Artificial Intelligence, I've created a Connect Four game that showcases two different AI approaches: Minimax with alpha-beta pruning and Monte Carlo Tree Search (MCTS) both comparatively and against a human opponent. I designed this project to demonstrate my understanding of search algorithms, game theory, and AI decision-making processes.
The project implements a classic Connect Four game where players take turns dropping colored discs into a vertical grid, aiming to connect four of their discs in a row while preventing their opponent from doing the same. What makes this implementation special is the ability to play against two different AI algorithms and analyze their performance in real-time.

![game play image](https://github.com/user-attachments/assets/c702a4d1-52e9-4671-931b-043f503734bb)

## Features

- Terminal-based user interface
- Optional Pygame graphical interface
- Two AI algorithms to choose from:
  - Minimax with Alpha-Beta Pruning
  - Monte Carlo Tree Search (MCTS)
- Three difficulty levels for each AI algorithm (Easy, Medium, Hard)
- Performance analysis of the AI's decision-making process
- Game statistics tracking
- AI comparison tools to evaluate algorithm performance

## Setup

```bash
# Clone the repository
git clone https://github.com/praiseogwuche/connect-four-ai.git
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

This will prompt you to select:
1. Interface type (terminal or graphical)
2. AI algorithm (Minimax or MCTS)
3. Difficulty level (Easy, Medium, Hard)

## How to Play

1. When you start the game, you'll be prompted to select a difficulty level:
   - **Easy**: Lower search depth/simulations
   - **Medium**: Medium search depth/simulations
   - **Hard**: Higher search depth/simulations

2. You play as 'X' and the AI plays as 'O'

3. During your turn, enter the column number (0-6) where you want to place your piece

4. After the AI's move, you'll see performance statistics about its decision-making process

5. The game continues until someone wins or the board is full (a draw)

6. At the end of the game, you can choose to play again

## AI Comparison

The project includes two scripts for comparing the AI algorithms:

```bash
# Compare algorithm performance on specific board positions
python compare_ai.py

# Simulate multiple games against a smart random player
python ai_vs_random.py
```

### Minimax vs. MCTS

- **Minimax with Alpha-Beta Pruning**: Uses a heuristic evaluation function and looks ahead a fixed number of moves. More deterministic and efficient at lower depths.

- **Monte Carlo Tree Search**: Uses random simulations to evaluate positions. Better at long-term exploration in complex trees, but slower and more resource-intensive due to its stochastic nature.

## Project Structure

- `src/game/board.py`: Connect Four game logic
- `src/ai/minimax.py`: AI implementation using minimax with alpha-beta pruning
- `src/ai/mcts.py`: AI implementation using Monte Carlo Tree Search
- `src/ui/interface.py`: Terminal-based user interface
- `src/ui/pygame_interface.py`: Pygame-based graphical user interface
- `main.py`: Entry point to run the game
- `compare_ai.py`: Script to compare AI algorithm performance 
- `ai_vs_random.py`: Script to simulate games against a smart random player


## Author

Praise Ogwuche  
Email: praiseogwuche@uni.minerva.edu  
GitHub: [github.com/PraiseOgwuche](https://github.com/PraiseOgwuche)

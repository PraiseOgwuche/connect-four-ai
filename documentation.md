# Connect Four AI - Project Documentation

## 1. Overview

This project implements a Connect Four game with an AI opponent that uses the minimax algorithm with alpha-beta pruning. The game allows human players to challenge the AI at three different difficulty levels, with performance metrics displayed to demonstrate the AI's decision-making process.

Connect Four is a two-player connection game where players take turns dropping colored discs into a vertically suspended grid. The objective is to be the first to form a horizontal, vertical, or diagonal line of four discs of your color.

## 2. Project Structure

The project follows a modular architecture with clear separation of concerns:

### 2.1 Core Components

- **Game Logic (`src/game/board.py`)**: Implements the Connect Four game rules and board state management
- **AI Implementation (`src/ai/minimax.py`)**: Contains the AI opponent using minimax with alpha-beta pruning
- **User Interface (`src/ui/interface.py`)**: Terminal-based interface for player interaction
- **Optional Graphical Interface (`src/ui/pygame_interface.py`)**: Pygame-based graphical interface (for local execution)
- **Main Application (`main.py`)**: Entry point with interface selection

### 2.2 Directory Structure

```
connect-four-ai/
├── README.md
├── requirements.txt
├── documentation.md
├── src/
│   ├── __init__.py
│   ├── game/
│   │   ├── __init__.py
│   │   └── board.py
│   ├── ai/
│   │   ├── __init__.py
│   │   └── minimax.py
│   └── ui/
│       ├── __init__.py
│       ├── interface.py
│       └── pygame_interface.py
└── main.py
```

## 3. Installation and Setup

### 3.1 Prerequisites
- Python 3.6 or higher
- Pygame (optional, for graphical interface)

### 3.2 Installation Steps

```bash
# Clone the repository
git clone https://github.com/yourusername/connect-four-ai.git
cd connect-four-ai

# Set up a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 4. Running the Game

### 4.1 Command Line Options

You can run the game using the following command:

```bash
python main.py
```

This will prompt you to select either the terminal interface or the graphical interface (Pygame). Alternatively, you can specify the interface directly:

```bash
python main.py terminal  # For terminal interface
python main.py pygame    # For graphical interface (when available)
```

### 4.2 Playing the Game

1. When you start the game, you'll be prompted to select a difficulty level:
   - **Easy**: The AI looks 2 moves ahead
   - **Medium**: The AI looks 4 moves ahead
   - **Hard**: The AI looks 6 moves ahead

2. You play as 'X' and the AI plays as 'O'

3. During your turn, enter the column number (0-6) where you want to place your piece

4. After the AI's move, you'll see performance statistics about its decision-making process

5. The game continues until someone wins or the board is full (a draw)

6. At the end of the game, you can choose to play again

## 5. AI Algorithm Explanation

### 5.1 Minimax Algorithm

The AI uses the minimax algorithm, which is a decision-making algorithm used in two-player turn-based games. It works by:

1. Building a game tree of possible future states up to a specified depth
2. Evaluating the leaf nodes of the tree using a heuristic function
3. Propagating these values back up the tree to determine the best move

For a two-player zero-sum game like Connect Four:
- The AI (maximizing player) chooses moves that maximize its score
- The human (minimizing player) is assumed to choose moves that minimize the AI's score

### 5.2 Alpha-Beta Pruning

Alpha-beta pruning is an optimization technique that reduces the number of nodes evaluated in the minimax algorithm. It works by:

1. Keeping track of two values: alpha (best value for maximizing player) and beta (best value for minimizing player)
2. Stopping the evaluation of a branch when it's proven that it cannot affect the final decision
3. Significantly reducing computation without affecting the final result

### 5.3 Board Evaluation Function

The AI evaluates board states using a heuristic function that considers:

1. Immediate wins or losses (highest priority)
2. Potential winning sequences:
   - Four consecutive positions with three AI pieces and one empty space
   - Four consecutive positions with two AI pieces and two empty spaces
   - Four consecutive positions with three human pieces and one empty space (threat)

The evaluation function looks at horizontal, vertical, and both diagonal directions when analyzing the board.

### 5.4 Difficulty Levels

The difficulty levels are implemented by varying the search depth:
- **Easy**: Search depth of 2 (AI looks 2 moves ahead)
- **Medium**: Search depth of 4 (AI looks 4 moves ahead)
- **Hard**: Search depth of 6 (AI looks 6 moves ahead)

As the search depth increases, the AI becomes stronger but requires more computation time.

## 6. Performance Analysis

The game includes performance analysis metrics for the AI's decision-making process:

- **Nodes Explored**: Total number of board states examined in the search tree
- **Pruning Count**: Number of branches eliminated by alpha-beta pruning
- **Evaluation Time**: Time taken (in seconds) to determine the best move
- **Nodes per Second**: Processing efficiency (nodes explored divided by evaluation time)

These metrics provide insights into the algorithm's efficiency and the impact of different difficulty levels.

## 7. Code Explanation

### 7.1 Game Board (`board.py`)

The `ConnectFourBoard` class implements the game board and rules:

- **Board Representation**: 2D array with 0 for empty cells, 1 for player pieces, and 2 for AI pieces
- **Move Validation**: Checks if a column has empty spaces for new pieces
- **Win Detection**: Checks for four in a row horizontally, vertically, and diagonally
- **Game State**: Tracks the current player and last move

### 7.2 AI Implementation (`minimax.py`)

The `MinimaxAI` class implements the AI opponent:

- **Minimax Algorithm**: Recursive function to explore possible future game states
- **Alpha-Beta Pruning**: Optimization to reduce the number of nodes explored
- **Board Evaluation**: Heuristic function to score board states
- **Performance Tracking**: Metrics to analyze the AI's decision-making process

### 7.3 Terminal Interface (`interface.py`)

The `TerminalInterface` class provides a text-based user interface:

- **Board Display**: Shows the current state of the game board
- **User Input**: Gets column selections from the human player
- **Difficulty Selection**: Allows the player to choose the AI difficulty level
- **Performance Display**: Shows AI performance metrics after each AI move

### 7.4 Pygame Interface (`pygame_interface.py`)

The `PygameInterface` class provides a graphical user interface using Pygame:

- **Visual Board**: Graphical representation of the game board
- **Mouse Input**: Allows the player to select columns by clicking
- **Visual Feedback**: Shows a preview of where the piece will drop
- **Animated Game Flow**: Visual representation of the game progression

## 8. Learning Outcomes Addressed

This project addresses the following course learning outcomes:

### 8.1 Search (#search)
- Implementation of the minimax algorithm with alpha-beta pruning
- Exploration of the game tree with different search depths
- Optimization of search through pruning techniques

### 8.2 AI Logic (#ailogic)
- Logical evaluation of game states using heuristics
- Decision-making based on future game states
- Strategic planning and threat response

### 8.3 AI Coding (#aicoding)
- Implementation of AI algorithms in Python
- Performance optimization and analysis
- Object-oriented design for AI components

## 9. Future Enhancements

Potential future enhancements for the project:

- **Transposition Table**: Cache previously evaluated positions to avoid redundant calculations
- **Opening Book**: Pre-computed optimal moves for the early game
- **Machine Learning Approach**: Replace the handcrafted evaluation function with a trained model
- **Multi-threading**: Parallelize the search for better performance on multi-core systems
- **Network Play**: Allow two human players to play against each other over a network

## 10. Conclusion

This Connect Four AI project demonstrates the application of classical AI search algorithms to create an intelligent game-playing agent. The implementation showcases how the minimax algorithm with alpha-beta pruning can be used to make optimal decisions in a two-player zero-sum game.

The different difficulty levels allow for an appropriate challenge regardless of the human player's skill level, while the performance metrics provide insights into the AI's decision-making process and the efficiency of the algorithm.
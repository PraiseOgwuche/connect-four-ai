# Connect Four AI

An implementation of Connect Four with an AI opponent using the minimax algorithm with alpha-beta pruning. Created as a final project for AI class.

## Project Overview

This project implements a Connect Four game with an AI opponent that uses the minimax algorithm with alpha-beta pruning to make decisions. The AI evaluates the game state and chooses the best move based on a look-ahead search of possible game states.

### Features

- Terminal-based user interface
- Optional Pygame graphical interface (when run locally)
- AI opponent with three difficulty levels (Easy, Medium, Hard)
- Performance analysis of the AI's decision-making process
- Game statistics tracking

## Learning Outcomes Addressed

This project addresses the following course learning outcomes:
- **Search (#search)**: Implementation of the minimax algorithm with alpha-beta pruning to search the game tree
- **AI Logic (#ailogic)**: Logical evaluation of game states to determine the best move
- **AI Coding (#aicoding)**: Implementation of AI algorithms in Python

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
from src.game.board import ConnectFourBoard
from src.ai.minimax import MinimaxAI
from src.ai.mcts import MCTS_AI
import sys
import os

def select_interface():
    """
    Let the user select the interface to use.
    
    Returns:
        str: Interface type ('terminal' or 'pygame')
    """
    print("\n==========================================")
    print("      Welcome to Connect Four AI!")
    print("==========================================")
    print("\nSelect interface:")
    print("1. Terminal Interface")
    print("2. Graphical Interface (Pygame)")
    
    while True:
        try:
            choice = int(input("Enter your choice (1-2): "))
            if choice == 1:
                return 'terminal'
            elif choice == 2:
                return 'pygame'
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def select_ai_algorithm():
    """
    Let the user select the AI algorithm to use.
    
    Returns:
        str: AI algorithm ('minimax' or 'mcts')
    """
    print("\nSelect AI algorithm:")
    print("1. Minimax with Alpha-Beta Pruning")
    print("2. Monte Carlo Tree Search (MCTS)")
    
    while True:
        try:
            choice = int(input("Enter your choice (1-2): "))
            if choice == 1:
                return 'minimax'
            elif choice == 2:
                return 'mcts'
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    # Check if interface type is provided as a command line argument
    if len(sys.argv) > 1 and sys.argv[1] in ['terminal', 'pygame']:
        interface_type = sys.argv[1]
    else:
        # Let the user select the interface
        interface_type = select_interface()
    
    # Let the user select the AI algorithm
    ai_algorithm = select_ai_algorithm()
    
    # Create a new game board
    board = ConnectFourBoard()
    
    # Create the AI player based on the selected algorithm
    if ai_algorithm == 'minimax':
        ai = MinimaxAI()
    else:  # mcts
        ai = MCTS_AI()
    
    # Create the user interface
    if interface_type == 'pygame':
        try:
            # Disable audio to avoid ALSA warnings
            os.environ['SDL_AUDIODRIVER'] = 'dummy'
            
            # Try to import and use Pygame
            from src.ui.pygame_interface import PygameInterface
            ui = PygameInterface(board, ai)
        except Exception as e:
            print(f"\nError initializing Pygame interface: {e}")
            print("Falling back to terminal interface.")
            from src.ui.interface import TerminalInterface
            ui = TerminalInterface(board, ai)
    else:
        from src.ui.interface import TerminalInterface
        ui = TerminalInterface(board, ai)
    
    # Start the game
    ui.play_game()

if __name__ == "__main__":
    main()
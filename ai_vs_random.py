import random
import time
from src.game.board import ConnectFourBoard
from src.ai.minimax import MinimaxAI
from src.ai.mcts import MCTS_AI

class SmartRandomPlayer:
    """
    A player that makes mostly random moves but has basic Connect Four understanding.
    """
    def __init__(self):
        self.name = "SmartRandom"
    
    def get_move(self, board):
        """
        Select a move with basic strategy:
        1. Win if possible
        2. Block opponent from winning if necessary
        3. Otherwise make a random move
        
        Args:
            board: Current game board
            
        Returns:
            int: Column index (0-based) for the move
        """
        valid_moves = board.get_valid_moves()
        if not valid_moves:
            return None
        
        # Check if we can win in this move
        for col in valid_moves:
            board_copy = self._copy_board(board)
            board_copy.make_move(col)
            if board_copy.get_winner() == board.current_player:
                return col
        
        # Check if opponent can win in their next move and block it
        opponent = 3 - board.current_player  # Switch player (1->2, 2->1)
        for col in valid_moves:
            board_copy = self._copy_board(board)
            # Simulate opponent making a move in this column
            board_copy.current_player = opponent
            board_copy.make_move(col)
            if board_copy.get_winner() == opponent:
                return col
        
        # Otherwise, make a random move
        return random.choice(valid_moves)
    
    def _copy_board(self, board):
        """Create a deep copy of the board."""
        from src.game.board import ConnectFourBoard
        
        new_board = ConnectFourBoard(board.rows, board.cols)
        for r in range(board.rows):
            for c in range(board.cols):
                new_board.board[r][c] = board.board[r][c]
        
        new_board.last_move = board.last_move
        new_board.current_player = board.current_player
        
        return new_board

def simulate_games(ai_player, num_games=100, verbose=True):
    """
    Simulate games between an AI player and a smart random player.
    
    Args:
        ai_player: The AI player to test
        num_games: Number of games to simulate
        verbose: Whether to print game progress
        
    Returns:
        dict: Results of the simulation
    """
    # Use SmartRandomPlayer instead of RandomPlayer
    random_player = SmartRandomPlayer()
    
    results = {
        'ai_wins': 0,
        'random_wins': 0,
        'draws': 0,
        'ai_first_wins': 0,
        'ai_second_wins': 0,
        'total_moves': 0,
        'total_time': 0
    }
    
    start_time = time.time()
    
    for game in range(num_games):
        # Create a new board
        board = ConnectFourBoard()
        
        # Randomly decide who goes first
        ai_first = random.choice([True, False])
        ai_player_num = 1 if ai_first else 2
        random_player_num = 2 if ai_first else 1
        
        # Keep track of the number of moves
        moves_count = 0
        
        # Play until the game is over
        while not board.is_game_over():
            if board.current_player == ai_player_num:
                move_start = time.time()
                move = ai_player.get_move(board)
                results['total_time'] += time.time() - move_start
            else:
                move = random_player.get_move(board)
            
            board.make_move(move)
            moves_count += 1
        
        results['total_moves'] += moves_count
        
        # Determine the winner
        winner = board.get_winner()
        
        if winner is None:
            results['draws'] += 1
            if verbose:
                print(f"Game {game+1}: Draw after {moves_count} moves")
        elif winner == ai_player_num:
            results['ai_wins'] += 1
            if ai_first:
                results['ai_first_wins'] += 1
            else:
                results['ai_second_wins'] += 1
            if verbose:
                print(f"Game {game+1}: AI wins after {moves_count} moves (AI {'first' if ai_first else 'second'})")
        else:
            results['random_wins'] += 1
            if verbose:
                print(f"Game {game+1}: Smart Random wins after {moves_count} moves (AI {'first' if ai_first else 'second'})")
    
    # Calculate percentages and averages
    results['ai_win_percentage'] = results['ai_wins'] / num_games * 100
    results['random_win_percentage'] = results['random_wins'] / num_games * 100
    results['draw_percentage'] = results['draws'] / num_games * 100
    results['avg_moves_per_game'] = results['total_moves'] / num_games
    results['avg_time_per_move'] = results['total_time'] / (results['total_moves'] / 2) if results['total_moves'] > 0 else 0
    results['total_simulation_time'] = time.time() - start_time
    
    return results

def print_results(ai_name, results):
    """
    Print simulation results in a readable format.
    """
    print("\n==========================================")
    print(f"      {ai_name} vs Smart Random Player")
    print("==========================================")
    print(f"Games played: {results['ai_wins'] + results['random_wins'] + results['draws']}")
    print(f"AI wins: {results['ai_wins']} ({results['ai_win_percentage']:.1f}%)")
    print(f"  - When AI goes first: {results['ai_first_wins']}")
    print(f"  - When AI goes second: {results['ai_second_wins']}")
    print(f"Smart Random player wins: {results['random_wins']} ({results['random_win_percentage']:.1f}%)")
    print(f"Draws: {results['draws']} ({results['draw_percentage']:.1f}%)")
    print(f"Average moves per game: {results['avg_moves_per_game']:.1f}")
    print(f"Average time per AI move: {results['avg_time_per_move']*1000:.1f} ms")
    print(f"Total simulation time: {results['total_simulation_time']:.1f} seconds")
    print("==========================================\n")

def main():
    print("\n==========================================")
    print("      AI vs Smart Random Player Simulation")
    print("==========================================")
    
    # Number of games to simulate
    num_games = 100
    
    # Test different difficulty levels
    difficulty_levels = ['easy', 'medium', 'hard']
    
    print("\nSimulating games with Minimax AI...")
    for difficulty in difficulty_levels:
        print(f"\nTesting Minimax ({difficulty}) against Smart Random Player...")
        minimax_ai = MinimaxAI(difficulty)
        minimax_results = simulate_games(minimax_ai, num_games, verbose=False)
        print_results(f"Minimax ({difficulty})", minimax_results)
    
    print("\nSimulating games with MCTS AI...")
    for difficulty in difficulty_levels:
        print(f"\nTesting MCTS ({difficulty}) against Smart Random Player...")
        mcts_ai = MCTS_AI(difficulty)
        mcts_results = simulate_games(mcts_ai, num_games, verbose=False)
        print_results(f"MCTS ({difficulty})", mcts_results)
    
    # Detailed comparison of medium difficulty
    print("\n==========================================")
    print("      Detailed Comparison (Medium Difficulty)")
    print("==========================================")
    
    minimax_medium = MinimaxAI('medium')
    mcts_medium = MCTS_AI('medium')
    
    print("\nSimulating 100 games with Minimax (medium)...")
    minimax_re
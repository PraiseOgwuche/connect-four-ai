import time
import random
from src.game.board import ConnectFourBoard
from src.ai.minimax import MinimaxAI
from src.ai.mcts import MCTS_AI

def compare_performance():
    """
    Compare performance of Minimax and MCTS AI.
    """
    print("\n==========================================")
    print("      AI Algorithm Comparison")
    print("==========================================")
    
    # Create AI instances with different difficulty levels
    minimax_easy = MinimaxAI('easy')
    minimax_medium = MinimaxAI('medium')
    minimax_hard = MinimaxAI('hard')
    
    mcts_easy = MCTS_AI('easy')
    mcts_medium = MCTS_AI('medium')
    mcts_hard = MCTS_AI('hard')
    
    # Test scenarios
    print("\nTesting on empty board...")
    test_scenario("Empty Board", ConnectFourBoard(), [
        minimax_easy, minimax_medium, minimax_hard,
        mcts_easy, mcts_medium, mcts_hard
    ])
    
    print("\nTesting on mid-game board...")
    mid_game_board = create_mid_game_board()
    test_scenario("Mid-Game Board", mid_game_board, [
        minimax_easy, minimax_medium, minimax_hard,
        mcts_easy, mcts_medium, mcts_hard
    ])
    
    print("\nTesting on near-winning board...")
    near_win_board = create_near_win_board()
    test_scenario("Near-Win Board", near_win_board, [
        minimax_easy, minimax_medium, minimax_hard,
        mcts_easy, mcts_medium, mcts_hard
    ])
    
    print("\n==========================================")
    print("      AI Strategy Comparison")
    print("==========================================")
    
    print("\nPlaying Minimax vs MCTS (10 games)...")
    result_10 = play_games(MinimaxAI('medium'), MCTS_AI('medium'), 10, verbose=True)
    print(f"Minimax wins: {result_10['minimax_wins']}")
    print(f"MCTS wins: {result_10['mcts_wins']}")
    print(f"Draws: {result_10['draws']}")
    
    print("\nPlaying Minimax vs MCTS (100 games)...")
    print("This will take some time, please wait...")
    result_100 = play_games(MinimaxAI('medium'), MCTS_AI('medium'), 100, verbose=False)
    print(f"Minimax wins: {result_100['minimax_wins']}")
    print(f"MCTS wins: {result_100['mcts_wins']}")
    print(f"Draws: {result_100['draws']}")
    print(f"Minimax win rate: {result_100['minimax_wins']}%")
    print(f"MCTS win rate: {result_100['mcts_wins']}%")
    print(f"Draw rate: {result_100['draws']}%")

def test_scenario(scenario_name, board, ai_list):
    """
    Test AI performance on a specific board scenario.
    """
    print(f"\n{scenario_name}:")
    print("-" * len(scenario_name) + "---")
    
    for ai in ai_list:
        # Make a copy of the board
        board_copy = ConnectFourBoard()
        for r in range(board.rows):
            for c in range(board.cols):
                board_copy.board[r][c] = board.board[r][c]
        board_copy.last_move = board.last_move
        board_copy.current_player = board.current_player
        
        # Measure time to make a move
        start_time = time.time()
        move = ai.get_move(board_copy)
        end_time = time.time()
        
        # Get performance stats
        if hasattr(ai, 'get_performance_stats'):
            stats = ai.get_performance_stats()
        else:
            stats = {}
        
        # Print results
        ai_type = "Minimax" if isinstance(ai, MinimaxAI) else "MCTS"
        print(f"{ai_type} ({ai.difficulty}): Move {move}, Time {end_time - start_time:.4f}s")
        
        if isinstance(ai, MinimaxAI):
            print(f"  Nodes explored: {stats.get('nodes_explored', 'N/A')}")
            print(f"  Pruning count: {stats.get('pruning_count', 'N/A')}")
            print(f"  Nodes per second: {int(stats.get('nodes_per_second', 0))}")
        else:  # MCTS
            print(f"  Simulations: {stats.get('simulations', 'N/A')}")
            print(f"  Nodes explored: {stats.get('nodes_explored', 'N/A')}")
            print(f"  Simulations per second: {int(stats.get('simulations_per_second', 0))}")

def create_mid_game_board():
    """
    Create a board with some pieces already placed (mid-game scenario).
    """
    board = ConnectFourBoard()
    
    # Make some moves to create a mid-game state
    moves = [3, 2, 4, 3, 2, 4, 3, 2]
    for move in moves:
        board.make_move(move)
    
    return board

def create_near_win_board():
    """
    Create a board where player 2 (AI) can win in one move.
    """
    board = ConnectFourBoard()
    
    # Set up a board where player 2 can win in one move
    board.board = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [1, 1, 1, 2, 2, 2, 0]
    ]
    
    board.last_move = (5, 5)
    board.current_player = 2  # AI's turn
    
    return board

def play_games(ai1, ai2, num_games, verbose=True):
    """
    Play games between two AI algorithms and return the results.
    
    Args:
        ai1: First AI player (typically Minimax)
        ai2: Second AI player (typically MCTS)
        num_games: Number of games to play
        verbose: Whether to print detailed progress for each game
        
    Returns:
        dict: Results of the games
    """
    results = {
        'minimax_wins': 0,
        'mcts_wins': 0,
        'draws': 0
    }
    
    for game in range(num_games):
        # Only print detailed progress if verbose is True (for smaller game counts)
        if verbose:
            print(f"Game {game+1}/{num_games}... ", end="")
        
        # Create a new board
        board = ConnectFourBoard()
        
        # Randomly decide who goes first
        board.current_player = random.choice([1, 2])
        
        # Play until the game is over
        while not board.is_game_over():
            if board.current_player == 1:
                move = ai1.get_move(board)
            else:
                move = ai2.get_move(board)
            
            board.make_move(move)
        
        # Determine the winner
        winner = board.get_winner()
        
        if winner is None:
            results['draws'] += 1
            if verbose:
                print("Draw!")
        elif (winner == 1 and isinstance(ai1, MinimaxAI)) or (winner == 2 and isinstance(ai2, MinimaxAI)):
            results['minimax_wins'] += 1
            if verbose:
                print("Minimax wins!")
        else:
            results['mcts_wins'] += 1
            if verbose:
                print("MCTS wins!")
    
    return results

if __name__ == "__main__":
    compare_performance()


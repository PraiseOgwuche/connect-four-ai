import random
import math
import time

class MinimaxAI:
    """
    AI player using the Minimax algorithm with alpha-beta pruning.
    """
    
    def __init__(self, difficulty='medium'):
        """
        Initialize the AI with a specified difficulty level.
        
        Args:
            difficulty (str): Difficulty level ('easy', 'medium', 'hard')
        """
        self.difficulty = difficulty
        
        # Set the search depth based on difficulty
        if difficulty == 'easy':
            self.max_depth = 2
        elif difficulty == 'medium':
            self.max_depth = 4
        elif difficulty == 'hard':
            self.max_depth = 6
        else:
            self.max_depth = 4  # Default to medium
        
        # Performance metrics
        self.nodes_explored = 0
        self.evaluation_time = 0
        self.pruning_count = 0

        self.transposition_table = {}  # Cache for board evaluations
            
    def get_move(self, board):
        """
        Get the best move for the current player.
        
        Args:
            board (ConnectFourBoard): Current game board
            
        Returns:
            int: Column index (0-based) for the best move
        """
        # Reset performance metrics
        self.nodes_explored = 0
        self.evaluation_time = 0
        self.pruning_count = 0
        self.transposition_table.clear()  # Clear cache between moves
        
        start_time = time.time()
        
        valid_moves = board.get_valid_moves()
        
        if not valid_moves:
            self.evaluation_time = time.time() - start_time
            return None
        
        # If there's only one valid move, return it
        if len(valid_moves) == 1:
            self.evaluation_time = time.time() - start_time
            return valid_moves[0]
        
        # Player is always the current player on the board
        player = board.current_player
        
        best_score = -math.inf
        best_moves = []
        
        # Try each valid move
        for col in valid_moves:
            # Create a copy of the board
            board_copy = self._copy_board(board)
            
            # Make the move
            board_copy.make_move(col)
            
            # Get the score for this move
            score = self._minimax(board_copy, self.max_depth, -math.inf, math.inf, False, player)
            
            # If this move is better than the best so far, update the best move
            if score > best_score:
                best_score = score
                best_moves = [col]
            # If this move is as good as the best so far, add it to the list of best moves
            elif score == best_score:
                best_moves.append(col)
        
        # Record the evaluation time
        self.evaluation_time = time.time() - start_time
        
        # Randomly select one of the best moves
        return random.choice(best_moves)
    
    def _minimax(self, board, depth, alpha, beta, is_maximizing, player):
        """
        Minimax algorithm with alpha-beta pruning and memoization.

        Args:
            board (ConnectFourBoard): Current game board
            depth (int): Current depth of the search tree
            alpha (float): Alpha value for pruning
            beta (float): Beta value for pruning
            is_maximizing (bool): True if maximizing player's turn, False otherwise
            player (int): Player number (1 or 2) for whom we're evaluating

        Returns:
            float: Score for the current board state
        """
        # Track nodes explored
        self.nodes_explored += 1

        # Compute a hash for the current board state
        board_hash = self._get_board_hash(board)

        # Return cached result if available
        if board_hash in self.transposition_table:
            return self.transposition_table[board_hash]

        # Terminal node or depth limit
        if depth == 0 or board.is_game_over():
            value = self._evaluate_board(board, player)
            self.transposition_table[board_hash] = value
            return value

        valid_moves = board.get_valid_moves()

        if is_maximizing:
            value = -math.inf
            for col in valid_moves:
                board_copy = self._copy_board(board)
                board_copy.make_move(col)
                score = self._minimax(board_copy, depth - 1, alpha, beta, False, player)
                value = max(value, score)
                alpha = max(alpha, value)
                if alpha >= beta:
                    self.pruning_count += 1
                    break  # Beta cutoff
            self.transposition_table[board_hash] = value
            return value

        else:  # Minimizing
            value = math.inf
            for col in valid_moves:
                board_copy = self._copy_board(board)
                board_copy.make_move(col)
                score = self._minimax(board_copy, depth - 1, alpha, beta, True, player)
                value = min(value, score)
                beta = min(beta, value)
                if alpha >= beta:
                    self.pruning_count += 1
                    break  # Alpha cutoff
            self.transposition_table[board_hash] = value
            return value

    
    def _evaluate_board(self, board, player):
        """
        Evaluate the board state for the specified player.
        
        Args:
            board (ConnectFourBoard): Current game board
            player (int): Player number (1 or 2)
            
        Returns:
            float: Score for the current board state
        """
        winner = board.get_winner()
        
        # If the game is over, return a high score if the player won,
        # a low score if the opponent won, or 0 for a draw
        if winner is not None:
            if winner == player:
                return 1000  # Player won
            else:
                return -1000  # Opponent won
        
        opponent = 3 - player
        score = 0

        # Encourage center column occupation
        center_col = board.cols // 2
        center_column = [board.board[r][center_col] for r in range(board.rows)]
        center_count = center_column.count(player)
        score += center_count * 3  # Weight = 3 per center disc

        # Horizontal windows
        for r in range(board.rows):
            for c in range(board.cols - 3):
                window = [board.board[r][c+i] for i in range(4)]
                score += self._evaluate_window(window, player, opponent)
        
        # Vertical windows
        for c in range(board.cols):
            for r in range(board.rows - 3):
                window = [board.board[r+i][c] for i in range(4)]
                score += self._evaluate_window(window, player, opponent)
        
        # Diagonal (top-left to bottom-right)
        for r in range(board.rows - 3):
            for c in range(board.cols - 3):
                window = [board.board[r+i][c+i] for i in range(4)]
                score += self._evaluate_window(window, player, opponent)
        
        # Diagonal (bottom-left to top-right)
        for r in range(3, board.rows):
            for c in range(board.cols - 3):
                window = [board.board[r-i][c+i] for i in range(4)]
                score += self._evaluate_window(window, player, opponent)
        
        # Penalize isolated discs
        for r in range(board.rows):
            for c in range(board.cols):
                if board.board[r][c] == player:
                    neighbors = []
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < board.rows and 0 <= nc < board.cols:
                                neighbors.append(board.board[nr][nc])
                    if player not in neighbors:
                        score -= 1  # Penalize for isolation

        return score

    def _evaluate_window(self, window, player, opponent):
        """
        Evaluate a window of 4 consecutive positions.
        
        Args:
            window (list): List of 4 consecutive positions
            player (int): Player number (1 or 2)
            opponent (int): Opponent's player number (1 or 2)
            
        Returns:
            float: Score for the window
        """
        # Count player's pieces, opponent's pieces, and empty spaces in the window
        player_count = window.count(player)
        opponent_count = window.count(opponent)
        empty_count = window.count(0)
        
        # Assign scores based on how many of each piece type are in the window
        if player_count == 4:
            return 100  # Player has 4 in a row (should not happen due to game end check)
        elif player_count == 3 and empty_count == 1:
            return 5  # Player has 3 in a row with an empty space (potential win)
        elif player_count == 2 and empty_count == 2:
            return 2  # Player has 2 in a row with 2 empty spaces
        elif opponent_count == 3 and empty_count == 1:
            return -4  # Opponent has 3 in a row with an empty space (threat)
        
        return 0
    
    def get_performance_stats(self):
        """
        Get performance statistics.
        
        Returns:
            dict: Dictionary of performance statistics
        """
        return {
            'difficulty': self.difficulty,
            'max_depth': self.max_depth,
            'nodes_explored': self.nodes_explored,
            'evaluation_time': self.evaluation_time,
            'pruning_count': self.pruning_count,
            'nodes_per_second': self.nodes_explored / self.evaluation_time if self.evaluation_time > 0 else 0
        }
    
    def _copy_board(self, board):
        """
        Create a deep copy of the board.
        
        Args:
            board (ConnectFourBoard): Board to copy
            
        Returns:
            ConnectFourBoard: Copy of the board
        """
        from src.game.board import ConnectFourBoard
        
        # Create a new board with the same dimensions
        new_board = ConnectFourBoard(board.rows, board.cols)
        
        # Copy the board state
        for r in range(board.rows):
            for c in range(board.cols):
                new_board.board[r][c] = board.board[r][c]
        
        # Copy other attributes
        new_board.last_move = board.last_move
        new_board.current_player = board.current_player
        
        return new_board
    
    def _get_board_hash(self, board):
        """
        Create a hashable representation of the board state.
        Includes the board grid and current player.
        """
        flat_board = tuple(cell for row in board.board for cell in row)
        return (flat_board, board.current_player)

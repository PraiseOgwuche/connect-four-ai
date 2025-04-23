import random
import math
import time
from copy import deepcopy

class MCTSNode:
    """
    Node in the Monte Carlo Tree Search.
    """
    def __init__(self, board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move  # Move that led to this node
        self.children = {}  # Maps moves to child nodes
        self.wins = 0
        self.visits = 0
        self.untried_moves = board.get_valid_moves()
        
    def select_child(self, exploration_weight=1.41):
        """
        Use UCB1 formula to select a child node.
        """
        # Log(sum of parent visits) for UCB1 formula
        log_visits = math.log(self.visits)
        
        # Find child with highest UCB1 value
        best_score = float('-inf')
        best_child = None
        
        for child in self.children.values():
            # UCB1 formula: wins/visits + exploration_weight * sqrt(log(parent_visits) / child_visits)
            if child.visits == 0:
                # Avoid division by zero
                continue
            
            exploitation = child.wins / child.visits
            exploration = exploration_weight * math.sqrt(log_visits / child.visits)
            ucb1 = exploitation + exploration
            
            if ucb1 > best_score:
                best_score = ucb1
                best_child = child
        
        return best_child
    
    def expand(self):
        """
        Expand the tree by adding a new child node.
        """
        if not self.untried_moves:
            return None
        
        # Choose a random untried move
        move = random.choice(self.untried_moves)
        self.untried_moves.remove(move)
        
        # Create a new child node
        board_copy = deepcopy(self.board)
        board_copy.make_move(move)
        child = MCTSNode(board_copy, parent=self, move=move)
        
        # Add child to children dictionary
        self.children[move] = child
        
        return child
    
    def update(self, result):
        """
        Update node statistics with simulation result.
        """
        self.visits += 1
        self.wins += result
    
    def is_fully_expanded(self):
        """
        Check if all possible moves from this node have been tried.
        """
        return len(self.untried_moves) == 0
    
    def is_terminal(self):
        """
        Check if the node represents a terminal state (game over).
        """
        return self.board.is_game_over()

class MCTS_AI:
    """
    AI player using Monte Carlo Tree Search (MCTS).
    """
    def __init__(self, difficulty='medium'):
        """
        Initialize the AI with a specified difficulty level.
        
        Args:
            difficulty (str): Difficulty level ('easy', 'medium', 'hard')
        """
        self.difficulty = difficulty
        
        # Set the number of simulations based on difficulty
        if difficulty == 'easy':
            self.simulations = 500
        elif difficulty == 'medium':
            self.simulations = 1000
        elif difficulty == 'hard':
            self.simulations = 2000
        else:
            self.simulations = 1000  # Default to medium
        
        # Set the exploration weight for UCB1
        self.exploration_weight = 1.41  # sqrt(2)
        
        # Performance metrics
        self.simulation_time = 0
        self.nodes_explored = 0
    
    def get_move(self, board):
        """
        Get the best move for the current player using MCTS.
        
        Args:
            board: Current game board
            
        Returns:
            int: Column index (0-based) for the best move
        """
        start_time = time.time()
        self.nodes_explored = 0
        
        valid_moves = board.get_valid_moves()
        
        if not valid_moves:
            self.simulation_time = time.time() - start_time
            return None
        
        # If there's only one valid move, return it
        if len(valid_moves) == 1:
            self.simulation_time = time.time() - start_time
            return valid_moves[0]
        
        # Initialize root node with current board state
        root = MCTSNode(self._copy_board(board))
        
        # Run MCTS for the specified number of simulations
        for _ in range(self.simulations):
            # Phase 1: Selection - navigate the tree until we find a node that is not fully expanded
            node = root
            self.nodes_explored += 1
            
            while not node.is_terminal() and node.is_fully_expanded():
                node = node.select_child(self.exploration_weight)
                self.nodes_explored += 1
            
            # Phase 2: Expansion - if the node is not terminal and not fully expanded, expand it
            if not node.is_terminal() and not node.is_fully_expanded():
                node = node.expand()
                self.nodes_explored += 1
            
            # Phase 3: Simulation - simulate a random game from this point
            if node is not None:  # In case expansion returned None
                result = self._simulate(node.board, board.current_player)
                
                # Phase 4: Backpropagation - update all nodes in the path with the result
                while node is not None:
                    node.update(result)
                    node = node.parent
        
        # Select the move with the highest win rate
        best_move = None
        best_win_rate = -float('inf')
        
        for move, child in root.children.items():
            if child.visits > 0:
                win_rate = child.wins / child.visits
                if win_rate > best_win_rate:
                    best_win_rate = win_rate
                    best_move = move
        
        # If no move was found, pick a random one
        if best_move is None and valid_moves:
            best_move = random.choice(valid_moves)
        
        self.simulation_time = time.time() - start_time
        
        return best_move
    
    def _simulate(self, board, original_player):
        """
        Simulate a random game from the current board state.
        
        Args:
            board: Starting board state
            original_player: Player for whom to evaluate the result
            
        Returns:
            float: 1 for a win, 0.5 for a draw, 0 for a loss
        """
        # Make a copy of the board
        board = self._copy_board(board)
        
        # Simulate until the game is over
        while not board.is_game_over():
            valid_moves = board.get_valid_moves()
            if not valid_moves:
                break
            # move = random.choice(valid_moves)
            move = self._select_heuristic_move(board, valid_moves, original_player)
            board.make_move(move)
        
        # Evaluate the result
        winner = board.get_winner()
        
        if winner is None:
            # Draw
            return 0.5
        elif winner == original_player:
            # Win
            return 1.0
        else:
            # Loss
            return 0.0

    def _select_heuristic_move(self, board, valid_moves, player):
        """
        Select a move using a lightweight heuristic similar to Minimax.
        """
        opponent = 3 - player
        best_score = float('-inf')
        best_moves = []

        for move in valid_moves:
            board_copy = self._copy_board(board)
            board_copy.make_move(move)

            # Immediate win
            if board_copy.get_winner() == player:
                return move

            # Block opponent win
            board_copy.current_player = opponent
            for opp_move in board_copy.get_valid_moves():
                board_copy_opp = self._copy_board(board_copy)
                board_copy_opp.make_move(opp_move)
                if board_copy_opp.get_winner() == opponent:
                    return move

            # Center preference
            center = board.cols // 2
            score = -abs(move - center)  # Closer to center = higher score

            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        return random.choice(best_moves)

    
    def _copy_board(self, board):
        """
        Create a deep copy of the board.
        
        Args:
            board: Board to copy
            
        Returns:
            Copy of the board
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
    
    def get_performance_stats(self):
        """
        Get performance statistics.
        
        Returns:
            dict: Dictionary of performance statistics
        """
        return {
            'difficulty': self.difficulty,
            'simulations': self.simulations,
            'nodes_explored': self.nodes_explored,
            'simulation_time': self.simulation_time,
            'simulations_per_second': self.simulations / self.simulation_time if self.simulation_time > 0 else 0
        }
import unittest
from unittest.mock import patch, MagicMock
from src.game.board import ConnectFourBoard
from src.ai.minimax import MinimaxAI
import time

class TestMinimaxAI(unittest.TestCase):
    """Test cases for the MinimaxAI class"""

    def setUp(self):
        """Set up a new AI and board before each test"""
        self.board = ConnectFourBoard()
        self.ai = MinimaxAI()

    def test_init(self):
        """Test AI initialization with different difficulty levels"""
        # Default initialization (medium)
        self.assertEqual(self.ai.difficulty, 'medium')
        self.assertEqual(self.ai.max_depth, 4)
        
        # Easy difficulty
        easy_ai = MinimaxAI('easy')
        self.assertEqual(easy_ai.difficulty, 'easy')
        self.assertEqual(easy_ai.max_depth, 2)
        
        # Medium difficulty
        medium_ai = MinimaxAI('medium')
        self.assertEqual(medium_ai.difficulty, 'medium')
        self.assertEqual(medium_ai.max_depth, 4)
        
        # Hard difficulty
        hard_ai = MinimaxAI('hard')
        self.assertEqual(hard_ai.difficulty, 'hard')
        self.assertEqual(hard_ai.max_depth, 6)
        
        # Invalid difficulty (defaults to medium)
        invalid_ai = MinimaxAI('invalid')
        self.assertEqual(invalid_ai.difficulty, 'invalid')
        self.assertEqual(invalid_ai.max_depth, 4)

    def test_get_move_empty_board(self):
        """Test that the AI returns a valid move on an empty board"""
        move = self.ai.get_move(self.board)
        
        # Move should be an integer within the valid column range
        self.assertIsInstance(move, int)
        self.assertGreaterEqual(move, 0)
        self.assertLess(move, self.board.cols)
        
        # Move should be valid according to the board
        self.assertTrue(self.board.is_valid_move(move))

    def test_get_move_one_move_left(self):
        """Test that the AI correctly chooses the only valid move"""
        # Fill all columns except one
        for col in range(self.board.cols):
            if col != 3:  # Leave column 3 open
                for _ in range(self.board.rows):
                    self.board.make_move(col)
        
        # There should be only one valid move (column 3)
        move = self.ai.get_move(self.board)
        self.assertEqual(move, 3)

    def test_get_move_winning_move(self):
        """Test that the AI chooses a winning move when available"""
        # Set up a board where the AI (player 2) can win with its next move
        # O O O _
        self.board.current_player = 2  # AI's turn
        
        # Place three AI pieces in a row
        self.board.board[5][0] = 2
        self.board.board[5][1] = 2
        self.board.board[5][2] = 2
        
        # AI should choose column 3 to win
        move = self.ai.get_move(self.board)
        self.assertEqual(move, 3)

    def test_get_move_blocking_move(self):
        """Test that the AI blocks the opponent from winning"""
        # Set up a board where the player can win with their next move
        # X X X _
        # AI needs to block column 3
        
        # Place three player pieces in a row
        self.board.board[5][0] = 1
        self.board.board[5][1] = 1
        self.board.board[5][2] = 1
        
        # AI should choose column 3 to block
        move = self.ai.get_move(self.board)
        self.assertEqual(move, 3)

    def test_minimax_evaluation(self):
        """Test the minimax evaluation function"""
        # Empty board should have a neutral score
        empty_score = self.ai._evaluate_board(self.board, 2)
        self.assertEqual(empty_score, 0)
        
        # Board with a win for the AI should have a high score
        win_board = ConnectFourBoard()
        win_board.board[5][0] = 2
        win_board.board[5][1] = 2
        win_board.board[5][2] = 2
        win_board.board[5][3] = 2
        win_board.last_move = (5, 3)
        
        win_score = self.ai._evaluate_board(win_board, 2)
        self.assertGreater(win_score, 100)  # High positive score
        
        # Board with a win for the opponent should have a low score
        loss_board = ConnectFourBoard()
        loss_board.board[5][0] = 1
        loss_board.board[5][1] = 1
        loss_board.board[5][2] = 1
        loss_board.board[5][3] = 1
        loss_board.last_move = (5, 3)
        
        loss_score = self.ai._evaluate_board(loss_board, 2)
        self.assertLess(loss_score, -100)  # High negative score

    def test_evaluate_window(self):
        """Test the window evaluation function"""
        # Four AI pieces (win)
        win_window = [2, 2, 2, 2]
        win_score = self.ai._evaluate_window(win_window, 2, 1)
        self.assertGreater(win_score, 0)
        
        # Three AI pieces with an empty slot (potential win)
        potential_win = [2, 2, 2, 0]
        potential_win_score = self.ai._evaluate_window(potential_win, 2, 1)
        self.assertGreater(potential_win_score, 0)
        
        # Three opponent pieces with an empty slot (threat)
        threat = [1, 1, 1, 0]
        threat_score = self.ai._evaluate_window(threat, 2, 1)
        self.assertLess(threat_score, 0)
        
        # Two AI pieces with two empty slots (opportunity)
        opportunity = [2, 2, 0, 0]
        opportunity_score = self.ai._evaluate_window(opportunity, 2, 1)
        self.assertGreater(opportunity_score, 0)
        
        # Mixed window with no clear advantage
        mixed = [1, 2, 0, 1]
        mixed_score = self.ai._evaluate_window(mixed, 2, 1)
        self.assertEqual(mixed_score, 0)

    def test_copy_board(self):
        """Test that the board copying function works correctly"""
        # Make some moves on the original board
        self.board.make_move(3)
        self.board.make_move(4)
        
        # Copy the board
        copied_board = self.ai._copy_board(self.board)
        
        # Check that dimensions match
        self.assertEqual(copied_board.rows, self.board.rows)
        self.assertEqual(copied_board.cols, self.board.cols)
        
        # Check that board state matches
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                self.assertEqual(copied_board.board[r][c], self.board.board[r][c])
        
        # Check that current player matches
        self.assertEqual(copied_board.current_player, self.board.current_player)
        
        # Check that last move matches
        self.assertEqual(copied_board.last_move, self.board.last_move)
        
        # Make a move on the copy and ensure it doesn't affect the original
        copied_board.make_move(2)
        self.assertNotEqual(copied_board.board[5][2], self.board.board[5][2])

    def test_performance_metrics(self):
        """Test that performance metrics are tracked correctly"""
        # Make sure the AI has the required attributes
        self.assertTrue(hasattr(self.ai, 'nodes_explored'))
        self.assertTrue(hasattr(self.ai, 'pruning_count'))
        self.assertTrue(hasattr(self.ai, 'evaluation_time'))
        
        # Get a move and check that metrics are updated
        self.ai.get_move(self.board)
        
        # Check that metrics have been updated
        self.assertGreater(self.ai.nodes_explored, 0)
        
        # Check get_performance_stats method
        stats = self.ai.get_performance_stats()
        self.assertIn('difficulty', stats)
        self.assertIn('max_depth', stats)
        self.assertIn('nodes_explored', stats)
        self.assertIn('pruning_count', stats)
        self.assertIn('evaluation_time', stats)
        self.assertIn('nodes_per_second', stats)

    def test_alpha_beta_pruning(self):
        """Test that alpha-beta pruning reduces the number of nodes explored"""
        # Create a copy of the AI with alpha-beta pruning disabled
        class MinimaxWithoutPruning(MinimaxAI):
            def _minimax(self, board, depth, alpha, beta, is_maximizing, player):
                self.nodes_explored += 1
                
                if depth == 0 or board.is_game_over():
                    return self._evaluate_board(board, player)
                
                valid_moves = board.get_valid_moves()
                
                if is_maximizing:
                    value = float('-inf')
                    for col in valid_moves:
                        board_copy = self._copy_board(board)
                        board_copy.make_move(col)
                        value = max(value, self._minimax(board_copy, depth - 1, alpha, beta, False, player))
                        # No pruning
                    return value
                else:
                    value = float('inf')
                    for col in valid_moves:
                        board_copy = self._copy_board(board)
                        board_copy.make_move(col)
                        value = min(value, self._minimax(board_copy, depth - 1, alpha, beta, True, player))
                        # No pruning
                    return value
        
        # Create instances with same depth but different pruning behavior
        ai_with_pruning = MinimaxAI()
        ai_with_pruning.max_depth = 3
        
        ai_without_pruning = MinimaxWithoutPruning()
        ai_without_pruning.max_depth = 3
        
        # Get moves from both and compare nodes explored
        ai_with_pruning.get_move(self.board)
        nodes_with_pruning = ai_with_pruning.nodes_explored
        
        ai_without_pruning.get_move(self.board)
        nodes_without_pruning = ai_without_pruning.nodes_explored
        
        # Alpha-beta pruning should explore fewer nodes
        self.assertLess(nodes_with_pruning, nodes_without_pruning)

    def test_different_depths(self):
        """Test that different search depths affect the number of nodes explored"""
        # Create AIs with different depths
        easy_ai = MinimaxAI('easy')    # Depth 2
        medium_ai = MinimaxAI('medium')  # Depth 4
        
        # Get moves and compare nodes explored
        easy_ai.get_move(self.board)
        medium_ai.get_move(self.board)
        
        # Higher depth should explore more nodes
        self.assertLess(easy_ai.nodes_explored, medium_ai.nodes_explored)

    def test_ai_execution_time(self):
        """Test that the AI execution time is reasonable"""
        # Time the AI's move calculation
        start_time = time.time()
        self.ai.get_move(self.board)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Medium difficulty should take less than 1 second on an empty board
        self.assertLess(execution_time, 1.0)

if __name__ == '__main__':
    unittest.main()
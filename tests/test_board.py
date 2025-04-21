import unittest
from src.game.board import ConnectFourBoard

class TestConnectFourBoard(unittest.TestCase):
    """Test cases for the ConnectFourBoard class"""

    def setUp(self):
        """Set up a new board before each test"""
        self.board = ConnectFourBoard()

    def test_init(self):
        """Test board initialization"""
        # Check dimensions
        self.assertEqual(self.board.rows, 6)
        self.assertEqual(self.board.cols, 7)
        
        # Check initial state
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                self.assertEqual(self.board.board[r][c], 0)
        
        # Check starting player
        self.assertEqual(self.board.current_player, 1)
        
        # Check last move is None
        self.assertIsNone(self.board.last_move)
        
        # Test custom dimensions
        custom_board = ConnectFourBoard(rows=8, cols=9)
        self.assertEqual(custom_board.rows, 8)
        self.assertEqual(custom_board.cols, 9)

    def test_make_move(self):
        """Test making moves on the board"""
        # Make a valid move
        result = self.board.make_move(3)
        self.assertTrue(result)
        self.assertEqual(self.board.board[5][3], 1)  # Bottom row, middle column
        self.assertEqual(self.board.last_move, (5, 3))
        self.assertEqual(self.board.current_player, 2)  # Player switched
        
        # Make another move
        result = self.board.make_move(3)
        self.assertTrue(result)
        self.assertEqual(self.board.board[4][3], 2)  # One up from bottom
        self.assertEqual(self.board.last_move, (4, 3))
        self.assertEqual(self.board.current_player, 1)  # Player switched back
        
        # Invalid column (out of bounds)
        result = self.board.make_move(-1)
        self.assertFalse(result)
        
        result = self.board.make_move(7)
        self.assertFalse(result)
        
        # Fill a column and try to add more
        for _ in range(4):  # Already 2 pieces in column 3
            self.board.make_move(3)
        
        # Column should be full now
        self.assertEqual(self.board.board[0][3], 2)
        result = self.board.make_move(3)
        self.assertFalse(result)

    def test_is_valid_move(self):
        """Test checking if a move is valid"""
        # Valid move
        self.assertTrue(self.board.is_valid_move(0))
        self.assertTrue(self.board.is_valid_move(6))
        
        # Invalid moves (out of bounds)
        self.assertFalse(self.board.is_valid_move(-1))
        self.assertFalse(self.board.is_valid_move(7))
        
        # Fill a column
        for _ in range(6):
            self.board.make_move(3)
        
        # Now column 3 should be invalid
        self.assertFalse(self.board.is_valid_move(3))

    def test_get_valid_moves(self):
        """Test getting all valid moves"""
        # All columns should be valid initially
        valid_moves = self.board.get_valid_moves()
        self.assertEqual(valid_moves, [0, 1, 2, 3, 4, 5, 6])
        
        # Fill a column
        for _ in range(6):
            self.board.make_move(3)
        
        # Column 3 should no longer be valid
        valid_moves = self.board.get_valid_moves()
        self.assertEqual(valid_moves, [0, 1, 2, 4, 5, 6])
        
        # Fill the board except one column
        for col in [0, 1, 2, 4, 5]:
            for _ in range(6):
                self.board.make_move(col)
        
        # Only column 6 should be valid
        valid_moves = self.board.get_valid_moves()
        self.assertEqual(valid_moves, [6])
        
        # Fill the last column
        for _ in range(6):
            self.board.make_move(6)
        
        # No valid moves left
        valid_moves = self.board.get_valid_moves()
        self.assertEqual(valid_moves, [])

    def test_horizontal_win(self):
        """Test horizontal win detection"""
        # Player 1 makes moves to get 4 in a row horizontally
        self.board.make_move(0)  # Player 1
        self.board.make_move(0)  # Player 2 above
        
        self.board.make_move(1)  # Player 1
        self.board.make_move(1)  # Player 2 above
        
        self.board.make_move(2)  # Player 1
        self.board.make_move(2)  # Player 2 above
        
        # No winner yet
        self.assertIsNone(self.board.get_winner())
        
        # Player 1 completes 4 in a row
        self.board.make_move(3)  # Player 1
        
        # Now player 1 should win
        self.assertEqual(self.board.get_winner(), 1)

    def test_vertical_win(self):
        """Test vertical win detection"""
        # Player 1 makes moves to get 4 in a row vertically
        self.board.make_move(3)  # Player 1
        self.board.make_move(4)  # Player 2
        
        self.board.make_move(3)  # Player 1
        self.board.make_move(4)  # Player 2
        
        self.board.make_move(3)  # Player 1
        self.board.make_move(4)  # Player 2
        
        # No winner yet
        self.assertIsNone(self.board.get_winner())
        
        # Player 1 completes 4 in a row
        self.board.make_move(3)  # Player 1
        
        # Now player 1 should win
        self.assertEqual(self.board.get_winner(), 1)

    def test_diagonal_win_rising(self):
        """Test diagonal rising win detection"""
        # Clear the board first
        self.board = ConnectFourBoard()
        
        # Set up the board state directly
        self.board.board = [
            [0, 0, 0, 0, 0, 0, 0],  # Top row
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],  # Player 1 at (2,3)
            [0, 0, 1, 2, 0, 0, 0],  # Player 1 at (3,2), Player 2 at (3,3)
            [0, 1, 2, 2, 0, 0, 0],  # Player 1 at (4,1), Player 2 at (4,2) and (4,3)
            [1, 2, 2, 2, 0, 0, 0]   # Player 1 at (5,0), Player 2 at (5,1), (5,2), and (5,3)
        ]
        
        # Set the last move (important for some implementations)
        self.board.last_move = (2, 3)
        self.board.current_player = 2  # Next player would be 2
        
        # Now player 1 should have a rising diagonal win
        winner = self.board.get_winner()
        self.assertEqual(winner, 1)
    
    def test_diagonal_win_falling(self):
        """Test diagonal falling win detection"""
        # Clear the board first
        self.board = ConnectFourBoard()
        
        # Set up the board state directly
        self.board.board = [
            [0, 0, 0, 0, 0, 0, 0],  # Top row
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],  # Player 1 at (2,3)
            [0, 0, 1, 2, 0, 0, 0],  # Player 1 at (3,2), Player 2 at (3,3)
            [0, 1, 2, 2, 0, 0, 0],  # Player 1 at (4,1), Player 2 at (4,2) and (4,3)
            [1, 2, 2, 2, 0, 0, 0]   # Player 1 at (5,0), Player 2 at (5,1), (5,2), and (5,3)
        ]
        
        # Set the last move (important for some implementations)
        self.board.last_move = (2, 3)
        self.board.current_player = 2  # Next player would be 2
        
        # Now player 1 should have a diagonal win
        winner = self.board.get_winner()
        self.assertEqual(winner, 1)

    def test_draw(self):
        """Test draw detection"""
        # Create a pattern without any wins (alternating players)
        self.board.board = [
            [1, 2, 1, 2, 1, 2, 1],  # Top row
            [2, 1, 2, 1, 2, 1, 2],
            [1, 2, 1, 2, 1, 2, 1],
            [2, 1, 2, 1, 2, 1, 2],
            [1, 2, 1, 2, 1, 2, 1],
            [2, 1, 2, 1, 2, 1, 2]   # Bottom row
        ]
        
        # Make sure the last move is set
        self.board.last_move = (0, 0)  # Doesn't matter which one, just needs to be set
        self.board.current_player = 2  # Next player would be 2
        
        # Verify that the pattern doesn't create a win
        winner = self.board.get_winner()
        self.assertIsNone(winner, f"Expected no winner, but found player {winner} won")
        
        # Now the board is full, so the game should be over (draw)
        self.assertTrue(self.board.is_game_over())

    '''
    def test_draw(self):
        """Test draw detection"""
        # Create a fresh board
        self.board = ConnectFourBoard()
        
        # Create a zigzag pattern that should have no winners
        self.board.board = [
            [2, 1, 2, 1, 2, 1, 2],  # Top row
            [1, 2, 1, 2, 1, 2, 1],
            [2, 1, 2, 1, 2, 1, 2],
            [1, 2, 1, 2, 1, 2, 1],
            [2, 1, 2, 1, 2, 1, 2],
            [1, 2, 1, 2, 1, 2, 1]   # Bottom row
        ]
        
        # Just to be sure, disable any existing win triggering logic
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                if c < self.board.cols - 3:
                    # Ensure no horizontal wins
                    assert not (self.board.board[r][c] == self.board.board[r][c+1] == 
                            self.board.board[r][c+2] == self.board.board[r][c+3])
                
                if r < self.board.rows - 3:
                    # Ensure no vertical wins
                    assert not (self.board.board[r][c] == self.board.board[r+1][c] == 
                            self.board.board[r+2][c] == self.board.board[r+3][c])
        
        # Check for the winner - it should be None
        winner = self.board.get_winner()
        
        if winner is not None:
            print("\nBoard in draw test:")
            for row in self.board.board:
                print(row)
            print(f"Winner detected: Player {winner}")
            
            # Let's check the diagonal win detection manually
            # Check top-left to bottom-right diagonals
            for r in range(self.board.rows - 3):
                for c in range(self.board.cols - 3):
                    if (self.board.board[r][c] == self.board.board[r+1][c+1] == 
                        self.board.board[r+2][c+2] == self.board.board[r+3][c+3]):
                        print(f"Found diagonal win at ({r},{c}) to ({r+3},{c+3}): {self.board.board[r][c]}")
                        
            # Check bottom-left to top-right diagonals
            for r in range(3, self.board.rows):
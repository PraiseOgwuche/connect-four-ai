class ConnectFourBoard:
    """
    Represents a Connect Four game board.
    """
    
    def __init__(self, rows=6, cols=7):
        """
        Initialize a new game board with specified dimensions.
        
        Args:
            rows (int): Number of rows in the board
            cols (int): Number of columns in the board
        """
        self.rows = rows
        self.cols = cols
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.last_move = None
        self.current_player = 1  # Player 1 starts
    
    def make_move(self, col):
        """
        Make a move in the specified column.
        
        Args:
            col (int): Column index (0-based)
            
        Returns:
            bool: True if move was successful, False otherwise
        """
        # Check if column is valid
        if col < 0 or col >= self.cols:
            return False
        
        # Find the lowest empty row in the column
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                self.last_move = (row, col)
                self.current_player = 3 - self.current_player  # Switch player (1->2, 2->1)
                return True
        
        # Column is full
        return False
    
    def is_valid_move(self, col):
        """
        Check if a move in the specified column is valid.
        
        Args:
            col (int): Column index (0-based)
            
        Returns:
            bool: True if move is valid, False otherwise
        """
        return col >= 0 and col < self.cols and self.board[0][col] == 0
    
    def get_valid_moves(self):
        """
        Get a list of valid column indices for moves.
        
        Returns:
            list: List of valid column indices
        """
        return [col for col in range(self.cols) if self.is_valid_move(col)]
    
    def is_game_over(self):
        """
        Check if the game is over.
        
        Returns:
            bool: True if game is over, False otherwise
        """
        return self.get_winner() is not None or len(self.get_valid_moves()) == 0
    
    def get_winner(self):
        """
        Check if there is a winner.
        
        Returns:
            int or None: Player number (1 or 2) if there is a winner, None otherwise
        """
        # Check for 4 in a row horizontally
        for r in range(self.rows):
            for c in range(self.cols - 3):
                if (self.board[r][c] != 0 and
                    self.board[r][c] == self.board[r][c+1] == self.board[r][c+2] == self.board[r][c+3]):
                    return self.board[r][c]
        
        # Check for 4 in a row vertically
        for c in range(self.cols):
            for r in range(self.rows - 3):
                if (self.board[r][c] != 0 and
                    self.board[r][c] == self.board[r+1][c] == self.board[r+2][c] == self.board[r+3][c]):
                    return self.board[r][c]
        
        # Check for 4 in a row diagonally (top-left to bottom-right)
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                if (self.board[r][c] != 0 and
                    self.board[r][c] == self.board[r+1][c+1] == self.board[r+2][c+2] == self.board[r+3][c+3]):
                    return self.board[r][c]
        
        # Check for 4 in a row diagonally (bottom-left to top-right)
        for r in range(3, self.rows):
            for c in range(self.cols - 3):
                if (self.board[r][c] != 0 and
                    self.board[r][c] == self.board[r-1][c+1] == self.board[r-2][c+2] == self.board[r-3][c+3]):
                    return self.board[r][c]
        
        return None
    
    def __str__(self):
        """
        String representation of the board.
        
        Returns:
            str: String representation of the board
        """
        result = ""
        for row in self.board:
            result += "|"
            for cell in row:
                if cell == 0:
                    result += " "
                elif cell == 1:
                    result += "X"
                else:
                    result += "O"
                result += "|"
            result += "\n"
        result += "-" * (self.cols * 2 + 1) + "\n"
        result += " "
        for col in range(self.cols):
            result += str(col) + " "
        return result
import pygame
import sys
import math
import time
from src.game.board import ConnectFourBoard
from src.ai.minimax import MinimaxAI

class PygameInterface:
    """
    Pygame-based user interface for the Connect Four game.
    """
    
    # Colors
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    LIGHT_GREY = (200, 200, 200)
    
    def __init__(self, board, ai):
        """
        Initialize the interface.
        
        Args:
            board (ConnectFourBoard): Game board
            ai (MinimaxAI): AI player
        """
        self.board = board
        self.ai = ai
        self.stats = {
            'player_wins': 0,
            'ai_wins': 0,
            'draws': 0
        }
        
        # Initialize Pygame
        pygame.init()
        
        # Set up the display
        self.SQUARESIZE = 100
        self.width = self.board.cols * self.SQUARESIZE
        self.height = (self.board.rows + 1) * self.SQUARESIZE
        self.size = (self.width, self.height)
        self.RADIUS = int(self.SQUARESIZE/2 - 5)
        
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Connect Four AI')
        
        # Set up fonts
        self.font = pygame.font.SysFont('monospace', 20)
        self.large_font = pygame.font.SysFont('monospace', 50)
        
        # Game state
        self.game_over = False
        self.turn = 0  # 0 for player, 1 for AI
        self.difficulty = 'medium'
    
    def draw_board(self):
        """
        Draw the game board.
        """
        # Draw the blue background
        for c in range(self.board.cols):
            for r in range(self.board.rows):
                pygame.draw.rect(self.screen, self.BLUE, 
                                 (c*self.SQUARESIZE, (r+1)*self.SQUARESIZE, 
                                 self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(self.screen, self.BLACK, 
                                   (int(c*self.SQUARESIZE + self.SQUARESIZE/2), 
                                    int((r+1)*self.SQUARESIZE + self.SQUARESIZE/2)), 
                                   self.RADIUS)
        
        # Draw the pieces
        for c in range(self.board.cols):
            for r in range(self.board.rows):
                if self.board.board[r][c] == 1:  # Player
                    pygame.draw.circle(self.screen, self.RED, 
                                      (int(c*self.SQUARESIZE + self.SQUARESIZE/2), 
                                       int((r+1)*self.SQUARESIZE + self.SQUARESIZE/2)), 
                                      self.RADIUS)
                elif self.board.board[r][c] == 2:  # AI
                    pygame.draw.circle(self.screen, self.YELLOW, 
                                      (int(c*self.SQUARESIZE + self.SQUARESIZE/2), 
                                       int((r+1)*self.SQUARESIZE + self.SQUARESIZE/2)), 
                                      self.RADIUS)
        
        # Draw the difficulty level
        difficulty_text = self.font.render(f'Difficulty: {self.difficulty.capitalize()}', True, self.WHITE)
        self.screen.blit(difficulty_text, (10, 10))
        
        pygame.display.update()
    
    def draw_game_over(self, winner):
        """
        Draw the game over screen.
        
        Args:
            winner (int or None): Winner of the game (1 for player, 2 for AI, None for draw)
        """
        if winner == 1:
            text = "Player Wins!"
            color = self.RED
        elif winner == 2:
            text = "AI Wins!"
            color = self.YELLOW
        else:
            text = "Draw!"
            color = self.WHITE
        
        label = self.large_font.render(text, True, color)
        self.screen.blit(label, (self.width // 2 - label.get_width() // 2, self.SQUARESIZE // 2))
        
        pygame.display.update()
    
    def draw_performance_stats(self):
        """
        Draw AI performance statistics.
        """
        stats = self.ai.get_performance_stats()
        
        # Background for stats
        pygame.draw.rect(self.screen, self.BLACK, 
                         (0, 0, self.width, self.SQUARESIZE))
        
        # Display stats
        stats_text = [
            f"Nodes: {stats['nodes_explored']}",
            f"Prunes: {stats['pruning_count']}",
            f"Time: {stats['evaluation_time']:.2f}s",
            f"NPS: {stats['nodes_per_second']:.0f}"
        ]
        
        for i, text in enumerate(stats_text):
            label = self.font.render(text, True, self.WHITE)
            self.screen.blit(label, (self.width // 2 + i * 120 - 150, self.SQUARESIZE // 2 - 10))
        
        pygame.display.update()
    
    def select_difficulty(self):
        """
        Let the user select the AI difficulty level.
        """
        # Draw the difficulty selection screen
        self.screen.fill(self.BLACK)
        
        title = self.large_font.render("Select Difficulty", True, self.WHITE)
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 50))
        
        # Define button positions and sizes
        button_width = 200
        button_height = 50
        button_y = 200
        button_spacing = 100
        
        easy_button = pygame.Rect(self.width // 2 - button_width // 2, button_y, button_width, button_height)
        medium_button = pygame.Rect(self.width // 2 - button_width // 2, button_y + button_spacing, button_width, button_height)
        hard_button = pygame.Rect(self.width // 2 - button_width // 2, button_y + 2 * button_spacing, button_width, button_height)
        
        pygame.draw.rect(self.screen, self.BLUE, easy_button)
        pygame.draw.rect(self.screen, self.BLUE, medium_button)
        pygame.draw.rect(self.screen, self.BLUE, hard_button)
        
        easy_text = self.font.render("Easy", True, self.WHITE)
        medium_text = self.font.render("Medium", True, self.WHITE)
        hard_text = self.font.render("Hard", True, self.WHITE)
        
        self.screen.blit(easy_text, (easy_button.centerx - easy_text.get_width() // 2, easy_button.centery - easy_text.get_height() // 2))
        self.screen.blit(medium_text, (medium_button.centerx - medium_text.get_width() // 2, medium_button.centery - medium_text.get_height() // 2))
        self.screen.blit(hard_text, (hard_button.centerx - hard_text.get_width() // 2, hard_button.centery - hard_text.get_height() // 2))
        
        pygame.display.update()
        
        # Wait for the user to click a button
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    
                    if easy_button.collidepoint(mouse_pos):
                        self.difficulty = 'easy'
                        self.ai.difficulty = 'easy'
                        self.ai.max_depth = 2
                        return
                    
                    if medium_button.collidepoint(mouse_pos):
                        self.difficulty = 'medium'
                        self.ai.difficulty = 'medium'
                        self.ai.max_depth = 4
                        return
                    
                    if hard_button.collidepoint(mouse_pos):
                        self.difficulty = 'hard'
                        self.ai.difficulty = 'hard'
                        self.ai.max_depth = 6
                        return
    
    def play_game(self):
        """
        Main game loop.
        """
        # Select difficulty
        self.select_difficulty()
        
        # Reset game state
        self.game_over = False
        self.turn = 0  # Player goes first
        
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Draw the board
                self.screen.fill(self.BLACK)
                self.draw_board()
                
                if self.turn == 0:  # Player's turn
                    # Show where the piece would drop
                    if event.type == pygame.MOUSEMOTION:
                        pygame.draw.rect(self.screen, self.BLACK, (0, 0, self.width, self.SQUARESIZE))
                        posx = event.pos[0]
                        pygame.draw.circle(self.screen, self.RED, (posx, int(self.SQUARESIZE/2)), self.RADIUS)
                        pygame.display.update()
                    
                    # Player makes a move
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.draw.rect(self.screen, self.BLACK, (0, 0, self.width, self.SQUARESIZE))
                        posx = event.pos[0]
                        col = int(math.floor(posx / self.SQUARESIZE))
                        
                        if self.board.is_valid_move(col):
                            self.board.make_move(col)
                            self.turn = 1  # Switch to AI's turn
                            
                            # Check if the player has won
                            if self.board.get_winner() == 1:
                                self.game_over = True
                                self.stats['player_wins'] += 1
                                self.draw_board()
                                self.draw_game_over(1)
                            
                            # Check if the game is a draw
                            elif self.board.is_game_over():
                                self.game_over = True
                                self.stats['draws'] += 1
                                self.draw_board()
                                self.draw_game_over(None)
            
            # AI's turn
            if self.turn == 1 and not self.game_over:
                # Show "AI thinking" text
                pygame.draw.rect(self.screen, self.BLACK, (0, 0, self.width, self.SQUARESIZE))
                thinking_text = self.font.render("AI is thinking...", True, self.WHITE)
                self.screen.blit(thinking_text, (self.width // 2 - thinking_text.get_width() // 2, self.SQUARESIZE // 2 - 10))
                pygame.display.update()
                
                # AI makes a move
                col = self.ai.get_move(self.board)
                if col is not None:
                    self.board.make_move(col)
                    self.turn = 0  # Switch to player's turn
                    
                    # Draw the updated board
                    self.draw_board()
                    
                    # Draw performance stats
                    self.draw_performance_stats()
                    
                    # Check if the AI has won
                    if self.board.get_winner() == 2:
                        self.game_over = True
                        self.stats['ai_wins'] += 1
                        self.draw_game_over(2)
                    
                    # Check if the game is a draw
                    elif self.board.is_game_over():
                        self.game_over = True
                        self.stats['draws'] += 1
                        self.draw_game_over(None)
            
            # Game over, wait for user to close window or play again
            if self.game_over:
                # Display "Play again" button
                pygame.draw.rect(self.screen, self.BLUE, (self.width // 2 - 100, self.height - 60, 200, 40))
                play_again_text = self.font.render("Play Again", True, self.WHITE)
                self.screen.blit(play_again_text, (self.width // 2 - play_again_text.get_width() // 2, self.height - 40))
                pygame.display.update()
                
                # Wait for user to click button or close window
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = event.pos
                            
                            # Check if "Play again" button was clicked
                            if self.width // 2 - 100 <= mouse_pos[0] <= self.width // 2 + 100 and self.height - 60 <= mouse_pos[1] <= self.height - 20:
                                waiting = False
                                # Reset the board
                                self.board = ConnectFourBoard()
                                # Play again
                                self.play_game()
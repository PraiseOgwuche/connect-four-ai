class TerminalInterface:
    """
    Terminal-based user interface for the Connect Four game.
    """
    
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
    
    def select_difficulty(self):
        """
        Let the user select the AI difficulty level.
        
        Returns:
            str: Selected difficulty level
        """
        print("Select AI difficulty level:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        
        while True:
            try:
                choice = int(input("Enter your choice (1-3): "))
                if choice == 1:
                    return 'easy'
                elif choice == 2:
                    return 'medium'
                elif choice == 3:
                    return 'hard'
                else:
                    print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    def display_board(self):
        """
        Display the current state of the board.
        """
        print(self.board)
    
    def get_human_move(self):
        """
        Get a move from the human player.
        
        Returns:
            int: Column index (0-based) for the move
        """
        while True:
            try:
                col = int(input(f"Enter column (0-{self.board.cols-1}): "))
                if self.board.is_valid_move(col):
                    return col
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    def display_stats(self):
        """
        Display game statistics.
        """
        print("\nGame Statistics:")
        print(f"Player wins: {self.stats['player_wins']}")
        print(f"AI wins: {self.stats['ai_wins']}")
        print(f"Draws: {self.stats['draws']}")
    
    def display_ai_performance(self):
        """
        Display AI performance statistics.
        """
        stats = self.ai.get_performance_stats()
        print("\nAI Performance Statistics:")

        if stats.get("difficulty"):
            print(f"Difficulty: {stats['difficulty']}")

        if hasattr(self.ai, "simulations"):
            # MCTS-specific stats
            print(f"Simulations: {stats['simulations']}")
            print(f"Nodes explored: {stats['nodes_explored']}")
            print(f"Simulation time: {stats['simulation_time']:.4f} seconds")
            print(f"Simulations per second: {int(stats['simulations_per_second'])}")
        else:
            # Minimax-specific stats
            print(f"Search depth: {stats['max_depth']}")
            print(f"Nodes explored: {stats['nodes_explored']}")
            print(f"Pruning count: {stats['pruning_count']}")
            print(f"Evaluation time: {stats['evaluation_time']:.4f} seconds")
            print(f"Nodes per second: {int(stats['nodes_per_second'])}")
        #print(f"Total time: {stats['total_time']:.4f} seconds")
        #print(f"Total nodes explored: {stats['total_nodes_explored']}")
        #print(f"Total pruning count: {stats['total_pruning_count']}")
        #print(f"Total nodes per second: {int(stats['total_nodes_per_second'])}")
        #print(f"Total simulation time: {stats['total_simulation_time']:.4f} seconds")
        #print(f"Total simulations per second: {int(stats['total_simulations_per_second'])}")
        #print(f"Total AI wins: {self.stats['ai_wins']}")
        #print(f"Total player wins: {self.stats['player_wins']}")
        #print(f"Total draws: {self.stats['draws']}")
    
    def play_game(self):
        """
        Main game loop.
        """
        from src.game.board import ConnectFourBoard
        
        human_player = 1  # Human is player 1
        
        print("Welcome to Connect Four!")
        print("You are X, the AI is O.")
        
        # Select difficulty level
        difficulty = self.select_difficulty()
        self.ai.difficulty = difficulty
        
        # Set the AI search depth based on difficulty
        if difficulty == 'easy':
            self.ai.max_depth = 2
        elif difficulty == 'medium':
            self.ai.max_depth = 4
        elif difficulty == 'hard':
            self.ai.max_depth = 6
        
        while not self.board.is_game_over():
            self.display_board()
            
            # Human player's turn
            if self.board.current_player == human_player:
                col = self.get_human_move()
            # AI player's turn
            else:
                print("AI is thinking...")
                col = self.ai.get_move(self.board)
                print(f"AI chose column {col}")
                self.display_ai_performance()
            
            self.board.make_move(col)
        
        # Game over
        self.display_board()
        winner = self.board.get_winner()
        
        if winner == human_player:
            print("Congratulations! You win!")
            self.stats['player_wins'] += 1
        elif winner is not None:
            print("AI wins!")
            self.stats['ai_wins'] += 1
        else:
            print("It's a draw!")
            self.stats['draws'] += 1
        
        self.display_stats()
        
        # Ask if the player wants to play again
        play_again = input("\nDo you want to play again? (y/n): ").lower()
        if play_again == 'y':
            # Reset the board
            self.board = ConnectFourBoard()
            self.play_game()
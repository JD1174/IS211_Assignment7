import random
import argparse

class Player:
    def __init__(self, name):
        """Initialize a Player with a name and a score of 0."""
        self.name = name
        self.score = 0

    def reset_score(self):
        """Reset the player's score to 0 (used when restarting the game)."""
        self.score = 0

    def __str__(self):
        """String representation of a player's current state."""
        return f"{self.name}: {self.score} points"

class Die:
    def __init__(self):
        """A simple die that rolls between 1 and 6."""
        pass

    def roll(self):
        """Roll the die and return a random integer between 1 and 6."""
        return random.randint(1, 6)

class PigGame:
    def __init__(self, num_players):
        """Initialize the game with a set number of players."""
        self.players = [Player(f"Player {i+1}") for i in range(num_players)]
        self.die = Die()
        self.current_player_index = 0

    def switch_player(self):
        """Switch to the next player after the current turn."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    # def debug_print_player_states(self):
    #     """Debug function to print the current state of all players."""
    #     print("\n[DEBUG] Current Player States:")
    #     for player in self.players:
    #         print(f"[DEBUG] {player.name}: {player.score} points")
    #     print("[DEBUG] Current player:", self.players[self.current_player_index].name)

    def play_turn(self):
        """Allow the current player to roll or hold, implementing the game rules."""
        current_player = self.players[self.current_player_index]
        turn_total = 0

        # Start of a player's turn
        #print(f"\n{current_player.name}'s turn")
        #self.debug_print_player_states()

        while True:
            roll = self.die.roll()
            print(f"\n{current_player.name} rolled a {roll}")
            
            # Debug output for the roll
            #print(f"[DEBUG] {current_player.name} rolled {roll}")

            if roll == 1:
                print(f"{current_player.name} scores nothing this turn.")
                # Debug: Player rolled a 1, their turn ends without points
                #print(f"[DEBUG] {current_player.name} rolled a 1, ending their turn.")
                break

            # Accumulate turn total
            turn_total += roll
            print(f"Turn total: {turn_total}, {current_player}")

            # Prompt the player for decision: roll again or hold or exit game
            while True:
                decision = input("Roll again (r), hold (h), or quit (q/quit/exit)? ").strip().lower()
                if decision in ['r', 'h', 'q', 'quit', 'exit']:
                    break
                print("Invalid input. Please enter 'r' to roll, 'h' to hold, or 'q' to quit.")

            # Check for quit commands
            if decision in ['q', 'quit', 'exit']:
                print("Thanks for playing! Exiting the game.")
                exit()  # Exit the program immediately

            #print(f"[DEBUG] {current_player.name} decision: {decision}")

            if decision == 'h':
                current_player.score += turn_total
                print(f"{current_player.name} holds. Total score: {current_player.score}")
                # Debug: Player holds, update their score
                #print(f"[DEBUG] {current_player.name} holds. Total score: {current_player.score}")
                break

        # Switch to the next player after the turn ends
        self.switch_player()

    def is_game_over(self):
        """Check if any player has reached a score of 100 or more."""
        return any(player.score >= 100 for player in self.players)

    def play_game(self):
        """Main game loop: play turns until a player reaches the winning score."""
        print("\nWelcome to the game of Pig!\n")
        while not self.is_game_over():
            self.play_turn()
        
        # Identify the winner and display final results
        winner = max(self.players, key=lambda player: player.score)
        print(f"\n{winner.name} wins with {winner.score} points!")
        print("\nFinal Scores:")
        for player in self.players:
            print(player)

        # Debug: Game over, print final states of all players
        #print("[DEBUG] Game Over. Final Player States:")
        self.debug_print_player_states()

    def reset_game(self):
        """Reset the game state to play another round, resetting player scores and turns."""
        for player in self.players:
            player.reset_score()
        self.current_player_index = 0
        # Debug: Game reset
        #print("[DEBUG] Game reset. Player scores are reset.")

def main(num_players):
    """Main entry point for running the game with a specified number of players."""
    game = PigGame(num_players)
    
    while True:
        game.play_game()
        play_again = input("\nWould you like to play another game? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break
        game.reset_game()

if __name__ == "__main__":
    # Set random seed for consistent behavior in testing and debugging
    #random.seed(0)

    # Set up argument parser for command-line argument --numPlayers
    parser = argparse.ArgumentParser(description="Play the game of Pig.")
    parser.add_argument("--numPlayers", type=int, default=2, help="Number of players in the game")
    args = parser.parse_args()

    # Start the game with the specified number of players
    main(args.numPlayers)
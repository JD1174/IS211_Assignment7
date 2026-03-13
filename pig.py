import random
import argparse
import sys

class Player:
    def __init__(self, name):
        """Initialize a Player with a name and a score of 0."""
        self.name = name
        self.score = 0

    def add_score(self, points):
        """Add points to the player's total score."""
        self.score += points

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
        self.players =[Player(f"Player {i+1}") for i in range(num_players)]
        self.die = Die()
        self.current_player_index = 0

    def switch_player(self):
        """Switch to the next player after the current turn."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def play_turn(self):
        """Allow the current player to roll or hold, implementing the game rules."""
        current_player = self.players[self.current_player_index]
        turn_total = 0

        print(f"\n--- {current_player.name}'s turn ---")

        while True:
            roll = self.die.roll()
            print(f"{current_player.name} rolled a {roll}")

            # Rule: Rolling a 1 scores nothing and ends the turn.
            if roll == 1:
                print(f"Rolled a 1! {current_player.name} scores nothing this turn.")
                turn_total = 0
                break

            # Rule: Rolling 2-6 adds to the turn total.
            turn_total += roll
            
            # Requirement: Output roll, current turn score, and total score BEFORE asking for decision.
            print(f"Current score for this turn: {turn_total}")
            print(f"Total score in the game: {current_player.score}")

            # Prompt the player for a decision
            while True:
                decision = input("Roll again (r) or hold (h)? ").strip().lower()
                if decision in ['r', 'h']:
                    break
                print("Invalid input. Please enter 'r' to roll or 'h' to hold.")

            if decision == 'h':
                current_player.add_score(turn_total)
                print(f"{current_player.name} holds. Total score is now {current_player.score}.")
                break

        # Switch to the next player after the turn ends
        self.switch_player()

    def is_game_over(self):
        """Check if any player has reached a score of 100 or more."""
        return any(player.score >= 100 for player in self.players)

    def play_game(self):
        """Main game loop: play turns until a player reaches the winning score."""
        print("\nWelcome to the game of Pig!")
        while not self.is_game_over():
            self.play_turn()
        
        # Identify the winner and display final results
        winner = max(self.players, key=lambda player: player.score)
        print(f"\nGame Over! {winner.name} wins with {winner.score} points!")
        print("\nFinal Scores:")
        for player in self.players:
            print(player)

    def reset_game(self):
        """Reset the game state to play another round."""
        for player in self.players:
            player.reset_score()
        self.current_player_index = 0


def main():
    """Main entry point for running the game."""
    # Configurable number of players via command line parameter
    parser = argparse.ArgumentParser(description="Play the game of Pig.")
    parser.add_argument("--numPlayers", type=int, default=2, help="Number of players in the game")
    args = parser.parse_args()

    # Requirement: Use a seed of 0 at the beginning of the code
    random.seed(0)

    # Initialize Game
    game = PigGame(args.numPlayers)
    
    while True:
        game.play_game()
        
        # Allow for more than one game at a time.
        while True:
            play_again = input("\nWould you like to play another game? (y/n): ").strip().lower()
            if play_again in ['y', 'n']:
                break
            print("Invalid input. Please enter 'y' or 'n'.")
            
        if play_again != 'y':
            print("Thanks for playing!")
            sys.exit()
            
        game.reset_game()

if __name__ == "__main__":
    main()
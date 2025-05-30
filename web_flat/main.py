import sys
import pygame
from game import Game

print("DEBUG: Starting game initialization...")

def main():
    print("DEBUG: Entering main function")
    # Initialize pygame
    pygame.init()
    print("DEBUG: Pygame initialized")
    
    # Create game instance
    print("DEBUG: Creating game instance")
    game = Game()
    print("DEBUG: Game instance created")
    
    # Start the game
    print("DEBUG: Starting game loop")
    game.run()
    print("DEBUG: Game loop ended")
    pygame.quit()
    print("DEBUG: Pygame quit")

print("DEBUG: About to check __main__")
if __name__ == "__main__":
    print("DEBUG: Running main()")
    main()
    print("DEBUG: Main completed") 
import sys
import pygame
from src.game import Game

def main():
    # Initialize pygame
    pygame.init()
    # Create game instance
    game = Game()
    # Start the game
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main() 
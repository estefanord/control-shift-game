import sys
import pygame
import asyncio
from src.game import Game

async def main():
    # Initialize pygame
    pygame.init()
    
    # Create game instance
    game = Game()
    
    # Start the game with async support
    await game.run_async()
    
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main()) 
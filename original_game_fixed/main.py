import asyncio
import sys
import pygame
from src.game import Game

async def main():
    print("Starting game...")
    
    # Initialize pygame
    pygame.init()
    print("Pygame initialized")
    
    # Create game instance with your exact code
    game = Game()
    print("Game instance created")
    
    # Your original game loop but async
    while game.running:
        game.handle_events()
        game.update()
        game.draw()
        
        # This is the key for pygbag - must await with 0
        await asyncio.sleep(0)
    
    pygame.quit()
    print("Game ended")

if __name__ == "__main__":
    asyncio.run(main()) 
import pygame
from src.constants import *
from src.rooms.room_base import Room

class NormalRoom(Room):
    def __init__(self, player, hide_door=False):
        super().__init__(player)
        self.room_name = "The First Step"
        self.hint_text = "Just try different buttons..."
        self.background_color = (20, 20, 40)  # Dark blue-ish background
        self.hide_door = hide_door
    
    def generate_layout(self):
        # Clear platforms
        self.platforms = []
        
        # Add floor with gaps to prevent getting stuck
        self.platforms.extend([
            pygame.Rect(0, SCREEN_HEIGHT - TILE_SIZE, 300, TILE_SIZE),
            pygame.Rect(400, SCREEN_HEIGHT - TILE_SIZE, SCREEN_WIDTH - 400, TILE_SIZE),
        ])
        
        # Add platforms - simple layout for tutorial room
        self.platforms.extend([
            # Left side platform
            pygame.Rect(100, 450, 150, TILE_SIZE),
            
            # Middle platform
            pygame.Rect(300, 380, 200, TILE_SIZE),
            
            # Right side platform (landing pad for the door)
            pygame.Rect(600, SCREEN_HEIGHT - 3*TILE_SIZE, 200, 2*TILE_SIZE),
        ])
        
        # Create exit door unless hidden
        if not self.hide_door:
            self.exit_door = pygame.Rect(SCREEN_WIDTH - 2*TILE_SIZE, SCREEN_HEIGHT - 5*TILE_SIZE, TILE_SIZE, 2*TILE_SIZE)
        else:
            self.exit_door = None
        
        # Set initial position
        self.initial_position = (100, 300)
    
    def draw(self, screen):
        # Draw the room using the base method
        super().draw(screen)
        
        # Draw some welcome text (more quirky)
        font = pygame.font.Font(None, 24)
        instructions = [
            "Wait, where am I?",
            "That door looks interesting...",
            "I should try to reach it somehow."
        ]
        
        y_pos = 70
        for line in instructions:
            text = font.render(line, True, LIGHT_GRAY)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_pos))
            y_pos += 30 
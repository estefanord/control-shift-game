import pygame
from src.constants import *
from src.rooms.room_base import Room

class ReversedRoom(Room):
    def __init__(self, player):
        super().__init__(player)
        self.room_name = "Mirror Maze"
        self.hint_text = "Left is right, right is left!"
        self.background_color = (40, 20, 40)  # Purple-ish background
        
        # Reversed left/right controls
        self.control_scheme = {
            "left": [pygame.K_RIGHT, pygame.K_d],  # Reversed!
            "right": [pygame.K_LEFT, pygame.K_a],  # Reversed!
            "jump": [pygame.K_UP, pygame.K_w, pygame.K_SPACE]  # Jump is the same
        }
    
    def generate_layout(self):
        # Clear platforms
        self.platforms = []
        
        # Add floor with gaps (to allow death and respawn if stuck)
        self.platforms.extend([
            pygame.Rect(0, SCREEN_HEIGHT - TILE_SIZE, 200, TILE_SIZE),
            pygame.Rect(300, SCREEN_HEIGHT - TILE_SIZE, 200, TILE_SIZE),
            pygame.Rect(600, SCREEN_HEIGHT - TILE_SIZE, 200, TILE_SIZE),
        ])
        
        # Add platforms with recovery paths
        self.platforms.extend([
            # Left platform with safety ledge
            pygame.Rect(100, 400, 100, TILE_SIZE),
            pygame.Rect(30, 490, 50, TILE_SIZE),  # Recovery ledge
            
            # Middle platforms (with a challenge)
            pygame.Rect(250, 350, 100, TILE_SIZE),
            pygame.Rect(450, 300, 100, TILE_SIZE),
            pygame.Rect(300, 370, 50, TILE_SIZE),  # Small recovery platform
            
            # Right platform (landing pad for the door)
            pygame.Rect(600, 250, 150, TILE_SIZE),
            pygame.Rect(550, 290, 30, TILE_SIZE),  # Small recovery platform
        ])
        
        # Create exit door
        self.exit_door = pygame.Rect(SCREEN_WIDTH - 2*TILE_SIZE, 250 - 2*TILE_SIZE, TILE_SIZE, 2*TILE_SIZE)
        
        # Set initial position
        self.initial_position = (150, 300)
    
    def draw(self, screen):
        # Draw the room using the base method
        super().draw(screen)
        
        # Draw some flavor text (more mysterious)
        font = pygame.font.Font(None, 24)
        text = font.render("Something feels... backwards?", True, PINK_PASTEL)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 70)) 
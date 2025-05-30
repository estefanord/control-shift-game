import pygame
import platform
from constants import *
from room_base import RoomBase

print("DEBUG: Loading room_normal.py")

def is_web_platform():
    return platform.system().lower() == "emscripten"

class NormalRoom(RoomBase):
    def __init__(self, player, hide_door=False):
        print("DEBUG: NormalRoom.__init__ started")
        try:
            super().__init__(player)
            self.room_name = "The First Step"
            self.hint_text = "Just try different buttons..."
            self.background_color = (20, 20, 40)  # Dark blue-ish background
            self.hide_door = hide_door
            self.init_platforms()
            print("DEBUG: NormalRoom.__init__ completed")
        except Exception as e:
            print(f"DEBUG ERROR: NormalRoom initialization failed: {str(e)}")
            raise

    def init_platforms(self):
        print("DEBUG: NormalRoom.init_platforms started")
        try:
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
            print("DEBUG: NormalRoom.init_platforms completed")
        except Exception as e:
            print(f"DEBUG ERROR: Platform initialization failed: {str(e)}")
            raise

    def update(self):
        try:
            # Update player physics
            keys = pygame.key.get_pressed()
            self.player.update(keys, self.platforms)

            # Check if room is complete
            if self.player.x > 750:  # Right edge of screen
                self.complete = True
        except Exception as e:
            print(f"DEBUG ERROR: Room update failed: {str(e)}")
            raise

    def draw(self, screen):
        try:
            # Clear screen
            screen.fill((200, 200, 200))  # Light gray background

            # Draw platforms
            for platform in self.platforms:
                pygame.draw.rect(screen, (100, 100, 100), platform)

            # Draw player
            pygame.draw.rect(screen, (255, 0, 0), (self.player.x, self.player.y, self.player.width, self.player.height))

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
        except Exception as e:
            print(f"DEBUG ERROR: Room draw failed: {str(e)}")
            raise 
import pygame
from src.constants import *
from src.rooms.room_base import Room

class DelayedRoom(Room):
    def __init__(self, player):
        super().__init__(player)
        self.room_name = "Time Lag Zone"
        self.hint_text = "Your actions seem to be on a delay... think ahead!"
        self.background_color = (40, 40, 60)  # Dark blue background
        
        # Queue for storing delayed inputs
        self.input_queue = []
        self.delay_frames = 30  # Half a second delay (at 60 FPS)
    
    def generate_layout(self):
        # Clear platforms
        self.platforms = []
        
        # Add floor with gaps for reset
        self.platforms.extend([
            pygame.Rect(0, SCREEN_HEIGHT - TILE_SIZE, 300, TILE_SIZE),
            pygame.Rect(400, SCREEN_HEIGHT - TILE_SIZE, 400, TILE_SIZE),
        ])
        
        # Add platforms - requires precise timing
        self.platforms.extend([
            # Starting platform
            pygame.Rect(50, 450, 150, TILE_SIZE),
            
            # Middle platforms - requires timing with the delay
            pygame.Rect(300, 420, 100, TILE_SIZE),
            pygame.Rect(450, 370, 100, TILE_SIZE),
            pygame.Rect(300, 320, 100, TILE_SIZE),
            
            # Recovery platforms
            pygame.Rect(200, 500, 50, TILE_SIZE),
            pygame.Rect(400, 450, 30, TILE_SIZE),
            pygame.Rect(225, 350, 40, TILE_SIZE),
            
            # Final platform
            pygame.Rect(500, 250, 200, TILE_SIZE),
        ])
        
        # Create exit door
        self.exit_door = pygame.Rect(SCREEN_WIDTH - 2*TILE_SIZE, 250 - 2*TILE_SIZE, TILE_SIZE, 2*TILE_SIZE)
        
        # Set initial position
        self.initial_position = (100, 400)
    
    def handle_input(self, keys):
        # Instead of directly applying inputs, add them to the queue
        current_input = {
            "left": any(keys[key] for key in self.control_scheme["left"]),
            "right": any(keys[key] for key in self.control_scheme["right"]),
            "jump": any(keys[key] for key in self.control_scheme["jump"])
        }
        
        # Add the current input to the queue
        self.input_queue.append(current_input)
        
        # If we have enough inputs in the queue, process the oldest one
        if len(self.input_queue) > self.delay_frames:
            delayed_input = self.input_queue.pop(0)
            
            # Create a fake key state dictionary
            fake_keys = {}
            for action, key_list in self.control_scheme.items():
                for key in key_list:
                    fake_keys[key] = delayed_input[action]
            
            # Pass the delayed input to the player
            self.player.handle_input(fake_keys, self.control_scheme)
        else:
            # If we don't have enough inputs yet, don't move
            fake_keys = {key: False for action in self.control_scheme.values() for key in action}
            self.player.handle_input(fake_keys, self.control_scheme)
    
    def draw(self, screen):
        # Draw the room using the base method
        super().draw(screen)
        
        # Draw some flavor text
        font = pygame.font.Font(None, 24)
        text = font.render("Is this place... lagging?", True, PINK_PASTEL)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 70))
        
        # Draw the input queue visualization
        self.draw_input_queue(screen)
    
    def draw_input_queue(self, screen):
        # Draw a visual representation of the input queue
        queue_x = 20
        queue_y = 100
        queue_width = 200
        queue_height = 20
        
        # Draw queue background
        pygame.draw.rect(screen, GRAY, (queue_x, queue_y, queue_width, queue_height))
        
        # Draw queue fill based on how full it is
        fill_width = (len(self.input_queue) / self.delay_frames) * queue_width
        pygame.draw.rect(screen, PINK_PASTEL, (queue_x, queue_y, fill_width, queue_height))
        
        # Draw queue border
        pygame.draw.rect(screen, WHITE, (queue_x, queue_y, queue_width, queue_height), 2)
        
        # Draw label
        font = pygame.font.Font(None, 20)
        label = font.render("???", True, WHITE)
        screen.blit(label, (queue_x, queue_y - 20)) 
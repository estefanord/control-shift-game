import pygame
import random
from constants import *
from room_base import Room

class RandomRoom(Room):
    def __init__(self, player):
        super().__init__(player)
        self.room_name = "Chaos Chamber"
        self.hint_text = "The controls keep changing! Keep pressing different keys!"
        self.background_color = (60, 20, 60)  # Purple-ish background
        
        # Available keys that could be mapped to controls
        self.available_keys = [
            pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, 
            pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_w,
            pygame.K_SPACE, pygame.K_q, pygame.K_e
        ]
        
        # Initialize control display first
        self.control_display = {
            "left": "",
            "right": "",
            "jump": ""
        }
        
        # Randomize controls on init
        self.randomize_controls()
        
        # Timer for re-randomizing controls
        self.randomize_timer = 0
        self.randomize_interval = 600  # Changed from 300 to 600 (10 seconds at 60 FPS)
    
    def randomize_controls(self):
        # Shuffle the available keys
        random.shuffle(self.available_keys)
        
        # Assign the first 3 keys to left, right, and jump
        self.control_scheme = {
            "left": [self.available_keys[0]],
            "right": [self.available_keys[1]],
            "jump": [self.available_keys[2]]
        }
        
        # Update control display
        self.control_display = {
            "left": pygame.key.name(self.available_keys[0]),
            "right": pygame.key.name(self.available_keys[1]),
            "jump": pygame.key.name(self.available_keys[2])
        }
    
    def enter(self):
        # Make sure we initialize controls when entering the room
        super().enter()
        self.randomize_controls()
        self.randomize_timer = 0
    
    def generate_layout(self):
        # Clear platforms
        self.platforms = []
        # Main path platforms (staggered up and right)
        platform_positions = [
            (50, 500, 120),    # Start platform (player starts here)
            (160, 440, 120),   # 1st jump up/right (reduced horizontal gap)
            (270, 380, 120),   # 2nd jump up/right
            (380, 320, 120),   # 3rd jump up/right
            (490, 260, 120),   # 4th jump up/right
            (600, 200, 120),   # 5th jump up/right, near door
        ]
        for x, y, width in platform_positions:
            self.platforms.append(pygame.Rect(x, y, width, TILE_SIZE))
        # Door platform
        self.exit_door = pygame.Rect(SCREEN_WIDTH - 2*TILE_SIZE, 190 - 2*TILE_SIZE, TILE_SIZE, 2*TILE_SIZE)
        # Recovery platforms below each main platform
        recovery_platforms = [
            (110, 550, 60),
            (220, 490, 60),
            (330, 430, 60),
            (440, 370, 60),
            (550, 310, 60),
        ]
        for x, y, width in recovery_platforms:
            self.platforms.append(pygame.Rect(x, y, width, TILE_SIZE))
        # Set initial position
        self.initial_position = (70, 470)
    
    def update(self):
        # Update randomize timer
        self.randomize_timer += 1
        if self.randomize_timer >= self.randomize_interval:
            self.randomize_timer = 0
            self.randomize_controls()
        
        # Call the base update method
        return super().update()
    
    def draw(self, screen):
        # Draw the room using the base method
        super().draw(screen)
        
        # Draw some flavor text
        font = pygame.font.Font(None, 24)
        text = font.render("What key does what now? So confusing!", True, PINK_PASTEL)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 70))
        
        # Draw the current control scheme
        self.draw_control_scheme(screen)
        
        # Draw the randomize timer
        self.draw_randomize_timer(screen)
    
    def draw_control_scheme(self, screen):
        font = pygame.font.Font(None, 20)
        
        # Draw control labels
        control_x = 20
        control_y = 100
        controls = [
            f"??? : {self.control_display.get('left', '?')}",
            f"??? : {self.control_display.get('right', '?')}",
            f"??? : {self.control_display.get('jump', '?')}"
        ]
        
        for i, control in enumerate(controls):
            text = font.render(control, True, WHITE)
            screen.blit(text, (control_x, control_y + i * 20))
    
    def draw_randomize_timer(self, screen):
        # Draw a visual representation of time until next randomization
        timer_x = 20
        timer_y = 170
        timer_width = 200
        timer_height = 10
        
        # Draw timer background
        pygame.draw.rect(screen, GRAY, (timer_x, timer_y, timer_width, timer_height))
        
        # Draw timer fill based on time remaining
        fill_width = (1 - (self.randomize_timer / self.randomize_interval)) * timer_width
        pygame.draw.rect(screen, PINK_PASTEL, (timer_x, timer_y, fill_width, timer_height))
        
        # Draw timer border
        pygame.draw.rect(screen, WHITE, (timer_x, timer_y, timer_width, timer_height), 1)
        
        # Draw label
        font = pygame.font.Font(None, 18)
        label = font.render("????? in:", True, WHITE)
        screen.blit(label, (timer_x, timer_y - 20)) 
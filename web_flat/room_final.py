import pygame
import random
from constants import *
from room_base import Room

class FinalRoom(Room):
    def __init__(self, player):
        super().__init__(player)
        self.room_name = "Chaos Theory"
        self.hint_text = "Each section works differently! Watch how the environment changes!"
        self.background_color = (40, 0, 40)  # Dark purple background
        
        # Control zone tracking
        self.zones = []
        self.current_zone = None
        
        # Delay queue for delayed controls section
        self.input_queue = []
        self.delay_frames = 15  # Quarter second delay
        
        # Momentum for the momentum section
        self.momentum = 0
        self.max_momentum = 12
        self.momentum_increment = 0.5
        self.friction = 0.1
    
    def generate_layout(self):
        # Clear platforms
        self.platforms = []
        
        # Define control zones (rectangles with different control schemes)
        self.zones = [
            {
                "rect": pygame.Rect(0, 0, SCREEN_WIDTH // 4, SCREEN_HEIGHT),
                "type": "normal",
                "color": (30, 30, 50)
            },
            {
                "rect": pygame.Rect(SCREEN_WIDTH // 4, 0, SCREEN_WIDTH // 4, SCREEN_HEIGHT),
                "type": "reversed",
                "color": (50, 30, 50)
            },
            {
                "rect": pygame.Rect(SCREEN_WIDTH // 2, 0, SCREEN_WIDTH // 4, SCREEN_HEIGHT),
                "type": "custom",
                "color": (30, 50, 30)
            },
            {
                "rect": pygame.Rect(SCREEN_WIDTH * 3 // 4, 0, SCREEN_WIDTH // 4, SCREEN_HEIGHT),
                "type": "normal",
                "color": (50, 50, 30)
            }
        ]
        
        # Simple staircase path across all zones
        num_steps = 8
        step_width = 120
        x_start = 40
        y_start = 520
        x_step = (SCREEN_WIDTH - 2 * x_start - step_width) // (num_steps - 1)
        y_step = 40
        
        for i in range(num_steps):
            x = x_start + i * x_step
            y = y_start - i * y_step
            self.platforms.append(pygame.Rect(x, y, step_width, TILE_SIZE))
        
        # Create exit door at the end of the staircase
        self.exit_door = pygame.Rect(x_start + (num_steps - 1) * x_step + step_width - 20, y_start - (num_steps - 1) * y_step - 2 * TILE_SIZE, TILE_SIZE, 2 * TILE_SIZE)
        
        # Set initial position
        self.initial_position = (x_start + 20, y_start - 20)
    
    def get_current_zone(self):
        # Determine which zone the player is in
        player_center_x = self.player.x + self.player.width // 2
        
        for zone in self.zones:
            if zone["rect"].collidepoint(player_center_x, self.player.y):
                return zone
        
        # Default to normal controls if not in any zone
        return self.zones[0]
    
    def handle_input(self, keys):
        # Get the current zone
        self.current_zone = self.get_current_zone()
        zone_type = self.current_zone["type"]
        
        # Handle input based on the current zone type
        if zone_type == "normal":
            self.handle_normal_input(keys)
        elif zone_type == "reversed":
            self.handle_reversed_input(keys)
        elif zone_type == "custom":
            self.handle_custom_input(keys)
        elif zone_type == "momentum":
            self.handle_momentum_input(keys)
    
    def handle_normal_input(self, keys):
        # Normal controls
        control_scheme = {
            "left": [pygame.K_LEFT, pygame.K_a],
            "right": [pygame.K_RIGHT, pygame.K_d],
            "jump": [pygame.K_UP, pygame.K_w, pygame.K_SPACE]
        }
        self.player.handle_input(keys, control_scheme)
    
    def handle_reversed_input(self, keys):
        # True reversed controls: pressing left moves right, pressing right moves left
        control_scheme = {
            "left": [pygame.K_RIGHT, pygame.K_d],   # Pressing right moves left
            "right": [pygame.K_LEFT, pygame.K_a],  # Pressing left moves right
            "jump": [pygame.K_UP, pygame.K_w, pygame.K_SPACE]
        }
        # Swap the actions: when left is pressed, move right; when right is pressed, move left
        swapped_keys = {}
        for key in control_scheme["left"]:
            swapped_keys[key] = any(keys[k] for k in control_scheme["right"])
        for key in control_scheme["right"]:
            swapped_keys[key] = any(keys[k] for k in control_scheme["left"])
        for key in control_scheme["jump"]:
            swapped_keys[key] = keys[key]
        self.player.handle_input(swapped_keys, control_scheme)
    
    def handle_custom_input(self, keys):
        # Only F (left), H (right), T (jump) work
        control_scheme = {
            "left": [pygame.K_f],
            "right": [pygame.K_h],
            "jump": [pygame.K_t]
        }
        self.player.handle_input(keys, control_scheme)
    
    def handle_momentum_input(self, keys):
        # Momentum-based controls
        control_scheme = {
            "left": [pygame.K_LEFT, pygame.K_a],
            "right": [pygame.K_RIGHT, pygame.K_d],
            "jump": [pygame.K_UP, pygame.K_w, pygame.K_SPACE]
        }
        
        going_left = any(keys[key] for key in control_scheme["left"])
        going_right = any(keys[key] for key in control_scheme["right"])
        jumping = any(keys[key] for key in control_scheme["jump"])
        
        # Update momentum
        if going_left and not going_right:
            self.momentum -= self.momentum_increment
        elif going_right and not going_left:
            self.momentum += self.momentum_increment
        else:
            # Apply friction
            if self.momentum > 0:
                self.momentum -= self.friction
                if self.momentum < 0:
                    self.momentum = 0
            elif self.momentum < 0:
                self.momentum += self.friction
                if self.momentum > 0:
                    self.momentum = 0
        
        # Clamp momentum
        self.momentum = max(-self.max_momentum, min(self.momentum, self.max_momentum))
        
        # Apply momentum to player
        self.player.vel_x = self.momentum
        
        # Handle jumping
        if jumping and self.player.on_ground:
            self.player.vel_y = JUMP_STRENGTH
            self.player.on_ground = False
        
        # Update player facing
        if self.momentum > 0:
            self.player.facing_right = True
        elif self.momentum < 0:
            self.player.facing_right = False
    
    def update(self):
        # Update normal game logic
        return super().update()
    
    def draw(self, screen):
        # Draw background with zone colors
        for zone in self.zones:
            pygame.draw.rect(screen, zone["color"], zone["rect"])
        
        # Draw zone dividers
        for i in range(1, len(self.zones)):
            x = i * SCREEN_WIDTH // 4
            pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT), 2)
        
        # Draw platforms
        for platform in self.platforms:
            pygame.draw.rect(screen, GRAY, platform)
        
        # Draw exit door
        pygame.draw.rect(screen, PINK_PASTEL, self.exit_door)
        
        # Draw door handle
        door_handle_x = self.exit_door.x + self.exit_door.width - 8
        door_handle_y = self.exit_door.y + self.exit_door.height // 2
        pygame.draw.circle(screen, YELLOW_PASTEL, (door_handle_x, door_handle_y), 4)
        
        # Draw zone indicators (without explicit labels)
        font = pygame.font.Font(None, 18)
        symbols = ["?", "?", "?", "?"] # Mystery symbols instead of explicit labels
        for i, symbol in enumerate(symbols):
            x = i * SCREEN_WIDTH // 4 + SCREEN_WIDTH // 8
            y = 50
            text = font.render(symbol, True, WHITE)
            screen.blit(text, (x - text.get_width() // 2, y))
        
        # Draw room name
        font = pygame.font.Font(None, 28)
        name_text = font.render(self.room_name, True, LIGHT_GRAY)
        screen.blit(name_text, (20, 20))
        
        # Draw flavor text
        font = pygame.font.Font(None, 24)
        text = font.render("What madness is this?! Everything keeps changing!", True, PINK_PASTEL)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 70))
        
        # Draw player
        self.player.draw(screen)
        
        # Draw current zone indicator (but more mysterious)
        if self.current_zone:
            zone_name = "???"
            indicator = font.render(f"Zone: {zone_name}", True, PINK_PASTEL)
            screen.blit(indicator, (SCREEN_WIDTH - indicator.get_width() - 20, 20))
        
        # Draw hint if revealed
        if self.hint_revealed:
            hint_text = font.render(self.hint_text, True, WHITE)
            screen.blit(hint_text, (10, SCREEN_HEIGHT - 30)) 
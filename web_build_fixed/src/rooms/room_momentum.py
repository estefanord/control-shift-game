import pygame
from src.constants import *
from src.rooms.room_base import Room

class MomentumRoom(Room):
    def __init__(self, player):
        super().__init__(player)
        self.room_name = "Slippery Slide"
        self.hint_text = "Everything's so slippery... try pressing the opposite direction to slow down!"
        self.background_color = (20, 60, 60)  # Teal-ish background
        
        # Momentum parameters
        self.momentum = 0
        self.max_momentum = 15
        self.momentum_increment = 0.5
        self.friction = 0.1
    
    def generate_layout(self):
        # Clear platforms
        self.platforms = []
        # Donkey Kong style: long platforms, alternating gaps
        platform_positions = [
            (0, 550, 700),    # Bottom, gap on right
            (100, 470, 700),  # Next, gap on left
            (0, 390, 700),    # Next, gap on right
            (100, 310, 700),  # Next, gap on left
            (0, 230, 700),    # Next, gap on right
        ]
        for i, (x, y, width) in enumerate(platform_positions):
            self.platforms.append(pygame.Rect(x, y, width, TILE_SIZE))
        # Door at top right
        self.exit_door = pygame.Rect(SCREEN_WIDTH - 2*TILE_SIZE, 230 - 2*TILE_SIZE, TILE_SIZE, 2*TILE_SIZE)
        # Set initial position at bottom left
        self.initial_position = (30, 520)
    
    def handle_input(self, keys):
        # Instead of directly moving, adjust momentum
        going_left = any(keys[key] for key in self.control_scheme["left"])
        going_right = any(keys[key] for key in self.control_scheme["right"])
        jumping = any(keys[key] for key in self.control_scheme["jump"])
        
        # Update momentum based on input
        if going_left and not going_right:
            self.momentum -= self.momentum_increment
        elif going_right and not going_left:
            self.momentum += self.momentum_increment
        else:
            # Apply friction when no directional input
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
        
        # Apply momentum to player velocity
        self.player.vel_x = self.momentum
        
        # Handle jumping (this stays the same)
        if jumping and self.player.on_ground:
            self.player.vel_y = JUMP_STRENGTH
            self.player.on_ground = False
        
        # Update player facing direction based on momentum
        if self.momentum > 0:
            self.player.facing_right = True
        elif self.momentum < 0:
            self.player.facing_right = False
    
    def draw(self, screen):
        # Draw the room using the base method
        super().draw(screen)
        
        # Draw some flavor text
        font = pygame.font.Font(None, 24)
        text = font.render("Whoa... what's with all this ice?!", True, BLUE_PASTEL)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 70))
        
        # Draw platforms with ice-like appearance
        for platform in self.platforms:
            # Draw ice overlay
            ice_rect = platform.copy()
            pygame.draw.rect(screen, BLUE_PASTEL, ice_rect)
            
            # Draw ice shine
            shine_rect = pygame.Rect(ice_rect.x + 5, ice_rect.y + 5, 10, 3)
            pygame.draw.rect(screen, WHITE, shine_rect)
        
        # Redraw the player (since we drew over it)
        self.player.draw(screen)
        
        # Draw momentum indicator
        self.draw_momentum_indicator(screen)
    
    def draw_momentum_indicator(self, screen):
        # Draw a visual representation of momentum
        indicator_x = SCREEN_WIDTH - 220
        indicator_y = 30
        indicator_width = 200
        indicator_height = 20
        
        # Draw indicator background
        pygame.draw.rect(screen, GRAY, (indicator_x, indicator_y, indicator_width, indicator_height))
        
        # Draw center line
        center_x = indicator_x + indicator_width // 2
        pygame.draw.line(screen, WHITE, (center_x, indicator_y), (center_x, indicator_y + indicator_height), 2)
        
        # Draw momentum fill
        fill_width = (self.momentum / self.max_momentum) * (indicator_width // 2)
        if self.momentum > 0:
            fill_rect = pygame.Rect(center_x, indicator_y, fill_width, indicator_height)
        else:
            fill_rect = pygame.Rect(center_x + fill_width, indicator_y, -fill_width, indicator_height)
        
        pygame.draw.rect(screen, PINK_PASTEL, fill_rect)
        
        # Draw indicator border
        pygame.draw.rect(screen, WHITE, (indicator_x, indicator_y, indicator_width, indicator_height), 2)
        
        # Draw label
        font = pygame.font.Font(None, 20)
        label = font.render("Slidey-ness", True, WHITE)
        screen.blit(label, (indicator_x, indicator_y - 20)) 
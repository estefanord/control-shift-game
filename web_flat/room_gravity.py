import pygame
from constants import *
from room_base import Room

class GravityRoom(Room):
    def __init__(self, player):
        super().__init__(player)
        self.room_name = "Upside Down"
        self.hint_text = "Everything's flipped! Try different buttons to jump... or fall?"
        self.background_color = (20, 20, 60)  # Dark blue background
        
        # Gravity is inverted in this room
        self.gravity = -GRAVITY
        
        # Flipped controls
        self.control_scheme = {
            "left": [pygame.K_LEFT, pygame.K_a],
            "right": [pygame.K_RIGHT, pygame.K_d],
            "jump": [pygame.K_DOWN, pygame.K_s]  # Down to "jump" (which is falling)
        }
    
    def generate_layout(self):
        # Clear platforms
        self.platforms = []
        
        # Add "ceiling" (which is actually the floor in reverse gravity)
        self.platforms.append(pygame.Rect(0, 0, SCREEN_WIDTH, TILE_SIZE))
        
        # Add platforms - designed for reverse gravity navigation with recovery paths
        self.platforms.extend([
            # Starting "ceiling" platform
            pygame.Rect(50, TILE_SIZE, 200, TILE_SIZE),
            
            # Middle platforms (adjusted for reachability)
            pygame.Rect(200, 90, 120, TILE_SIZE),   # reachable from start
            pygame.Rect(320, 180, 120, TILE_SIZE),  # reachable from previous
            pygame.Rect(440, 270, 120, TILE_SIZE),  # reachable from previous
            pygame.Rect(560, 360, 120, TILE_SIZE),  # reachable from previous
            
            # Recovery/intermediate platforms
            pygame.Rect(260, 135, 60, TILE_SIZE),
            pygame.Rect(380, 225, 60, TILE_SIZE),
            pygame.Rect(500, 315, 60, TILE_SIZE),
            
            # Final platform
            pygame.Rect(600, 400, 150, TILE_SIZE),
            
            # New platforms to reach the door
            pygame.Rect(650, 480, 100, TILE_SIZE),
            pygame.Rect(700, 560, 80, TILE_SIZE),
        ])
        
        # Add some "bottom" platforms so you don't get permanently stuck if you fall
        self.platforms.extend([
            pygame.Rect(100, SCREEN_HEIGHT - 2*TILE_SIZE, 100, TILE_SIZE),
            pygame.Rect(300, SCREEN_HEIGHT - 2*TILE_SIZE, 100, TILE_SIZE),
            pygame.Rect(500, SCREEN_HEIGHT - 2*TILE_SIZE, 100, TILE_SIZE),
        ])
        
        # Create exit door (at the bottom, which is now like the ceiling)
        self.exit_door = pygame.Rect(SCREEN_WIDTH - 2*TILE_SIZE, SCREEN_HEIGHT - 2*TILE_SIZE, TILE_SIZE, 2*TILE_SIZE)
        
        # Set initial position
        self.initial_position = (100, 50)
    
    def enter(self):
        # Reset player position - near the "ceiling" (now floor)
        self.player.x, self.player.y = self.initial_position
        self.player.vel_x = 0
        self.player.vel_y = 0
        
        # Reset hint
        self.hint_revealed = False
        self.hint_timer = 0
        
        # Generate the room layout
        self.generate_layout()
    
    def handle_input(self, keys):
        # Reset horizontal velocity
        self.player.vel_x = 0
        
        # Apply the current control scheme
        for action, key_list in self.control_scheme.items():
            for key in key_list:
                if keys[key]:
                    if action == "left":
                        self.player.vel_x = -PLAYER_SPEED
                        self.player.facing_right = False
                    elif action == "right":
                        self.player.vel_x = PLAYER_SPEED
                        self.player.facing_right = True
                    elif action == "jump" and self.player.on_ground:
                        # In reversed gravity, "jump" is actually falling downward
                        self.player.vel_y = -JUMP_STRENGTH  # Negate jump strength
                        self.player.on_ground = False
    
    def update(self):
        # Get pressed keys
        keys = pygame.key.get_pressed()
        
        # Handle player input
        self.handle_input(keys)
        
        # Apply reversed gravity
        if not self.player.on_ground:
            self.player.vel_y += self.gravity  # Apply negative gravity
        
        # Update player position
        self.player.x += self.player.vel_x
        self.player.y += self.player.vel_y
        
        # Update player state
        if not self.player.on_ground:
            if self.player.vel_y > 0:  # Moving up in reversed gravity is falling
                self.player.state = "falling"
            else:
                self.player.state = "jumping"
        else:
            if self.player.vel_x == 0:
                self.player.state = "idle"
            else:
                self.player.state = "walking"
        
        # Handle collisions with platforms
        self.check_reversed_collisions()
        
        # Update animation
        self.player.animation_counter += 1
        if self.player.animation_counter >= self.player.animation_delay:
            self.player.animation_counter = 0
            self.player.animation_frame = (self.player.animation_frame + 1) % 4
        
        # Update hint timer
        self.hint_timer += 1
        if self.hint_timer >= self.hint_delay:
            self.hint_revealed = True
        
        # Check if player reached the exit door
        player_rect = self.player.get_rect()
        if player_rect.colliderect(self.exit_door):
            return True  # Room completed
        
        return False  # Room not completed yet
    
    def check_reversed_collisions(self):
        # Create a rect for the player's new position
        player_rect = self.player.get_rect()
        
        # Check collision with platforms
        self.player.on_ground = False
        for platform in self.platforms:
            if player_rect.colliderect(platform):
                # Check if collision is from bottom (player is standing on ceiling)
                if self.player.vel_y < 0 and player_rect.top < platform.bottom and player_rect.top - self.player.vel_y >= platform.bottom - 10:
                    self.player.y = platform.bottom
                    self.player.vel_y = 0
                    self.player.on_ground = True
                # Check if collision is from top (player hitting head, which is actually the floor)
                elif self.player.vel_y > 0 and player_rect.bottom > platform.top and player_rect.bottom - self.player.vel_y <= platform.top + 10:
                    self.player.y = platform.top - self.player.height
                    self.player.vel_y = 0
                # Check if collision is from left
                elif self.player.vel_x > 0 and player_rect.right > platform.left and player_rect.right - self.player.vel_x <= platform.left + 10:
                    self.player.x = platform.left - self.player.width
                # Check if collision is from right
                elif self.player.vel_x < 0 and player_rect.left < platform.right and player_rect.left - self.player.vel_x >= platform.right - 10:
                    self.player.x = platform.right
        
        # Keep player within screen bounds
        if self.player.x < 0:
            self.player.x = 0
        if self.player.x > SCREEN_WIDTH - self.player.width:
            self.player.x = SCREEN_WIDTH - self.player.width
        if self.player.y < 0:
            self.player.y = 0
            self.player.vel_y = 0
            self.player.on_ground = True  # Sticking to ceiling
        if self.player.y > SCREEN_HEIGHT - self.player.height:
            self.player.y = SCREEN_HEIGHT - self.player.height
            self.player.vel_y = 0
    
    def draw(self, screen):
        # Draw background
        screen.fill(self.background_color)
        
        # Draw platforms
        for platform in self.platforms:
            pygame.draw.rect(screen, self.wall_color, platform)
        
        # Draw exit door
        pygame.draw.rect(screen, self.door_color, self.exit_door)
        
        # Draw door handle
        door_handle_x = self.exit_door.x + self.exit_door.width - 8
        door_handle_y = self.exit_door.y + self.exit_door.height // 2
        pygame.draw.circle(screen, YELLOW_PASTEL, (door_handle_x, door_handle_y), 4)
        
        # Draw room name
        font = pygame.font.Font(None, 28)
        name_text = font.render(self.room_name, True, LIGHT_GRAY)
        screen.blit(name_text, (20, 20))
        
        # Draw some flavor text
        font = pygame.font.Font(None, 24)
        text = font.render("Am I walking on the ceiling?!", True, PURPLE_PASTEL)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 70))
        
        # Draw gravity indicator
        arrow_length = 30
        arrow_start = (SCREEN_WIDTH - 50, 130)
        arrow_end = (SCREEN_WIDTH - 50, 100)  # Arrow pointing up for reverse gravity
        pygame.draw.line(screen, PINK_PASTEL, arrow_start, arrow_end, 3)
        
        # Draw arrowhead
        pygame.draw.polygon(screen, PINK_PASTEL, [
            (arrow_end[0] - 5, arrow_end[1] + 5),
            (arrow_end[0] + 5, arrow_end[1] + 5),
            arrow_end
        ])
        
        # Draw gravity label
        font = pygame.font.Font(None, 20)
        gravity_text = font.render("???", True, WHITE)
        screen.blit(gravity_text, (SCREEN_WIDTH - 80, 140))
        
        # Draw player
        self.player.draw(screen)
        
        # Draw hint if revealed
        if self.hint_revealed:
            hint_text = font.render(self.hint_text, True, WHITE)
            screen.blit(hint_text, (10, SCREEN_HEIGHT - 30)) 
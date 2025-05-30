import pygame
import platform
from constants import *
import random

print("DEBUG: Loading room_base.py")

def is_web_platform():
    return platform.system().lower() == "emscripten"

class Room:
    def __init__(self, player):
        self.player = player
        self.platforms = []
        self.exit_door = None
        self.background_color = BLACK
        self.wall_color = GRAY
        self.door_color = PINK_PASTEL
        self.hint_revealed = False
        self.hint_timer = 0
        self.hint_delay = 300  # Show hint after 5 seconds (60 frames per second * 5)
        
        # Control scheme (default)
        self.control_scheme = {
            "left": [pygame.K_LEFT, pygame.K_a],
            "right": [pygame.K_RIGHT, pygame.K_d],
            "jump": [pygame.K_UP, pygame.K_w, pygame.K_SPACE]
        }
        
        # Custom messages for this room
        self.room_name = "???"
        self.hint_text = "Hmm... how do I move here?"
        
        # Death and respawn
        self.initial_position = (100, 300)
        self.death_cooldown = 0
        self.death_sound_played = False
        self.platform_seed = random.randint(0, 100000)
        # Fruit mechanic
        self.fruit_timer = 0
        self.fruit_spawned = False
        self.fruit_collected = False
        self.fruit_rect = None
        self.fruit_aura_angle = 0
        self.fruit_duration = 7200  # 2 minutes at 60 FPS
        self.normal_controls_active = False
    
    def enter(self):
        # Reset player position
        self.player.x, self.player.y = self.initial_position
        self.player.vel_x = 0
        self.player.vel_y = 0
        
        # Reset hint
        self.hint_revealed = False
        self.hint_timer = 0
        
        # Generate the room layout
        self.generate_layout()
        # Reset fruit
        self.fruit_timer = 0
        self.fruit_spawned = False
        self.fruit_collected = False
        self.fruit_rect = None
        self.fruit_aura_angle = 0
        self.normal_controls_active = False
    
    def generate_layout(self):
        # Default room layout - should be overridden
        self.platforms = [
            # Floor
            pygame.Rect(0, SCREEN_HEIGHT - TILE_SIZE, SCREEN_WIDTH, TILE_SIZE),
            
            # Platforms
            pygame.Rect(100, 400, 200, TILE_SIZE),
            pygame.Rect(400, 350, 200, TILE_SIZE),
            pygame.Rect(200, 250, 200, TILE_SIZE),
        ]
        
        # Create exit door
        self.exit_door = pygame.Rect(SCREEN_WIDTH - 2*TILE_SIZE, SCREEN_HEIGHT - 3*TILE_SIZE, TILE_SIZE, 2*TILE_SIZE)
        
        # Set initial position
        self.initial_position = (100, 300)
    
    def handle_event(self, event):
        pass  # To be implemented by subclasses
    
    def check_death(self):
        # Check if player has fallen off the platforms
        if self.player.y > SCREEN_HEIGHT + 50:
            return True
            
        # Add more death conditions if needed
        return False
    
    def respawn_player(self):
        # Reset player to initial position in this room
        self.player.x, self.player.y = self.initial_position
        self.player.vel_x = 0
        self.player.vel_y = 0
        self.death_cooldown = 30  # Half-second cooldown (at 60 FPS)
        self.death_sound_played = False
    
    def update(self):
        try:
            # Get pressed keys
            keys = pygame.key.get_pressed()
            
            # Update death cooldown
            if self.death_cooldown > 0:
                self.death_cooldown -= 1
                return False
            
            # Check for death
            if self.check_death():
                self.respawn_player()
                return False
            
            # Fruit timer logic
            if not self.fruit_collected:
                self.fruit_timer += 1
                if self.fruit_timer >= self.fruit_duration and not self.fruit_spawned:
                    self.spawn_fruit()
            
            # Handle player input
            if self.normal_controls_active:
                normal_scheme = {
                    "left": [pygame.K_LEFT, pygame.K_a],
                    "right": [pygame.K_RIGHT, pygame.K_d],
                    "jump": [pygame.K_UP, pygame.K_w, pygame.K_SPACE]
                }
                self.player.handle_input(keys, normal_scheme)
            else:
                self.handle_input(keys)
            
            # Update player
            self.player.update(self.platforms)
            
            # Update hint timer
            self.hint_timer += 1
            if self.hint_timer >= self.hint_delay:
                self.hint_revealed = True
            
            # Fruit collision
            if self.fruit_spawned and not self.fruit_collected and self.fruit_rect:
                if self.player.get_rect().colliderect(self.fruit_rect):
                    self.fruit_collected = True
                    self.normal_controls_active = True
            
            # Check if player reached the exit door
            player_rect = self.player.get_rect()
            if self.exit_door is not None and player_rect.colliderect(self.exit_door):
                return True  # Room completed
            return False  # Room not completed yet
        except Exception as e:
            print(f"DEBUG ERROR: Room update failed: {str(e)}")
            return False
    
    def handle_input(self, keys):
        # Default implementation - just pass the control scheme to the player
        self.player.handle_input(keys, self.control_scheme)
    
    def draw_8bit_block(self, screen, rect, color, pattern_type=0):
        # Draw a block with a simple 8-bit pattern
        block = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        block.fill(color)
        random.seed(self.platform_seed + rect.x + rect.y + pattern_type)
        # Add a checker or stripe pattern
        for y in range(0, rect.height, 4):
            for x in range(0, rect.width, 4):
                if pattern_type == 0:  # Checker
                    if (x//4 + y//4) % 2 == 0:
                        pygame.draw.rect(block, (min(color[0]+30,255), min(color[1]+30,255), min(color[2]+30,255)), (x, y, 4, 4))
                elif pattern_type == 1:  # Stripes
                    if (y//4) % 2 == 0:
                        pygame.draw.rect(block, (max(color[0]-30,0), max(color[1]-30,0), max(color[2]-30,0)), (x, y, 4, 4))
                elif pattern_type == 2:  # Dots
                    if random.random() < 0.2:
                        pygame.draw.rect(block, (255,255,255), (x, y, 2, 2))
        screen.blit(block, (rect.x, rect.y))

    def draw(self, screen):
        try:
            # Draw background
            screen.fill(self.background_color)
            # Draw platforms with 8-bit patterns
            for i, platform in enumerate(self.platforms):
                if platform.height > TILE_SIZE:  # Floor
                    self.draw_8bit_block(screen, platform, self.wall_color, pattern_type=1)
                else:  # Platform
                    self.draw_8bit_block(screen, platform, self.wall_color, pattern_type=0)
            # Draw exit door
            if self.exit_door is not None:
                pygame.draw.rect(screen, self.door_color, self.exit_door)
                # Draw door handle
                door_handle_x = self.exit_door.x + self.exit_door.width - 8
                door_handle_y = self.exit_door.y + self.exit_door.height // 2
                pygame.draw.circle(screen, YELLOW_PASTEL, (door_handle_x, door_handle_y), 4)
            # Draw room name (more subtle)
            font = pygame.font.Font(None, 28)
            name_text = font.render(self.room_name, True, LIGHT_GRAY)
            screen.blit(name_text, (20, 20))
            # Draw fruit
            self.draw_fruit(screen)
            # Draw player
            self.player.draw(screen)
        except Exception as e:
            print(f"DEBUG ERROR: Room drawing failed: {str(e)}")
            # Fallback to black screen
            screen.fill(BLACK)
    
    def get_hint(self):
        # Only return hint if it's been revealed
        if self.hint_revealed:
            return self.hint_text
        return ""

    def spawn_fruit(self):
        # Find the bottom platform (floor)
        floor = None
        for plat in self.platforms:
            if plat.height > TILE_SIZE:
                if floor is None or plat.y > floor.y:
                    floor = plat
        if floor:
            # Place fruit at the far right if player is left, far left if player is right
            if self.player.x < SCREEN_WIDTH // 2:
                fruit_x = floor.x + floor.width - TILE_SIZE
            else:
                fruit_x = floor.x
            fruit_y = floor.y - TILE_SIZE
            self.fruit_rect = pygame.Rect(fruit_x + TILE_SIZE//4, fruit_y + TILE_SIZE//4, TILE_SIZE//2, TILE_SIZE//2)
            self.fruit_spawned = True

    def draw_fruit(self, screen):
        if self.fruit_spawned and not self.fruit_collected and self.fruit_rect:
            # Draw animated aura
            center = self.fruit_rect.center
            for i in range(8):
                angle = self.fruit_aura_angle + i * (360 // 8)
                rad = angle * 3.14159 / 180
                aura_x = int(center[0] + 18 * pygame.math.Vector2(1,0).rotate(angle).x)
                aura_y = int(center[1] + 18 * pygame.math.Vector2(1,0).rotate(angle).y)
                pygame.draw.circle(screen, (255,255,120,120), (aura_x, aura_y), 7)
            # Draw fruit (shiny yellow with white highlight)
            pygame.draw.ellipse(screen, (255,255,0), self.fruit_rect)
            pygame.draw.ellipse(screen, (255,255,180), self.fruit_rect.inflate(-8,-8))
            pygame.draw.ellipse(screen, (255,255,255), self.fruit_rect.inflate(-16,-16))
            self.fruit_aura_angle = (self.fruit_aura_angle + 4) % 360 
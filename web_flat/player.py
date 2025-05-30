import pygame
import platform
from constants import *

print("DEBUG: Loading player.py")

def is_web_platform():
    return platform.system().lower() == "emscripten"

class Player:
    def __init__(self):
        print("DEBUG: Player.__init__ started")
        try:
            self.width = 24
            self.height = 32
            self.x = SCREEN_WIDTH // 2
            self.y = SCREEN_HEIGHT - 100
            self.vel_x = 0
            self.vel_y = 0
            self.on_ground = False
            self.facing_right = True
            self.state = "idle"
            self.animation_frame = 0
            self.animation_delay = 6
            self.animation_counter = 0
            self.generate_sprites()
            print("DEBUG: Player.__init__ completed")
        except Exception as e:
            print(f"DEBUG ERROR: Player initialization failed: {str(e)}")
            raise

    def generate_sprites(self):
        print("DEBUG: Generating player sprites")
        try:
            # Generate simple rectangle for player
            self.sprite = pygame.Surface((self.width, self.height))
            self.sprite.fill((255, 0, 0))  # Red color
            print("DEBUG: Player sprites generated")
        except Exception as e:
            print(f"DEBUG ERROR: Sprite generation failed: {str(e)}")
            raise

    def update(self, keys, platforms):
        try:
            # Store previous position
            prev_x = self.x
            prev_y = self.y

            # Handle input with web-specific checks
            if is_web_platform():
                print("DEBUG: Web platform input handling")
                # Use a more forgiving input system for web
                self.vel_x = 0
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.vel_x = -self.speed
                    self.facing_right = False
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.vel_x = self.speed
                    self.facing_right = True
                if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground:
                    self.vel_y = self.jump_power
                    self.on_ground = False
            else:
                # Desktop input handling
                self.vel_x = 0
                if keys[pygame.K_LEFT]:
                    self.vel_x = -self.speed
                    self.facing_right = False
                if keys[pygame.K_RIGHT]:
                    self.vel_x = self.speed
                    self.facing_right = True
                if keys[pygame.K_SPACE] and self.on_ground:
                    self.vel_y = self.jump_power
                    self.on_ground = False

            # Apply gravity
            if not self.on_ground:
                self.vel_y += self.gravity

            # Update position
            self.x += self.vel_x
            self.y += self.vel_y

            # Check boundaries with debug info
            if self.x < 0:
                print("DEBUG: Hit left boundary")
                self.x = 0
            elif self.x > SCREEN_WIDTH - self.width:
                print("DEBUG: Hit right boundary")
                self.x = SCREEN_WIDTH - self.width

            # Platform collision
            self.on_ground = False
            for platform in platforms:
                if self.collides_with(platform):
                    print("DEBUG: Platform collision detected")
                    # Vertical collision
                    if self.vel_y > 0:
                        self.y = platform.y - self.height
                        self.vel_y = 0
                        self.on_ground = True
                    elif self.vel_y < 0:
                        self.y = platform.y + platform.height
                        self.vel_y = 0
                    # Horizontal collision
                    elif self.vel_x > 0:
                        self.x = platform.x - self.width
                    elif self.vel_x < 0:
                        self.x = platform.x + platform.width

            print(f"DEBUG: Player position updated - x:{self.x}, y:{self.y}, vel_x:{self.vel_x}, vel_y:{self.vel_y}")
        except Exception as e:
            print(f"DEBUG ERROR: Player update failed: {str(e)}")
            raise

    def collides_with(self, other):
        try:
            return (self.x < other.x + other.width and
                    self.x + self.width > other.x and
                    self.y < other.y + other.height and
                    self.y + self.height > other.y)
        except Exception as e:
            print(f"DEBUG ERROR: Collision check failed: {str(e)}")
            raise

    def draw(self, screen):
        try:
            screen.blit(self.sprite, (self.x, self.y))
            print("DEBUG: Player drawn to screen")
        except Exception as e:
            print(f"DEBUG ERROR: Player draw failed: {str(e)}")
            raise 
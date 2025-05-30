import pygame
from src.constants import *

class Player:
    def __init__(self):
        self.width = 24
        self.height = 32
        self.x = 100
        self.y = 300
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        self.state = "idle"
        self.animation_frame = 0
        self.animation_delay = 6
        self.animation_counter = 0
        self.generate_sprites()

    def generate_sprites(self):
        # Generate 8-bit style pixel art for player
        self.sprites = {"idle": [], "walk": [], "jump": []}
        # Idle: standing
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw_pixel_player(surf, eye_offset=0)
        self.sprites["idle"].append(surf)
        # Walk: 2 frames
        for i in range(2):
            surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.draw_pixel_player(surf, eye_offset=i*2-1, leg_up=(i==1))
            self.sprites["walk"].append(surf)
        # Jump: 1 frame
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw_pixel_player(surf, eye_offset=0, arms_up=True)
        self.sprites["jump"].append(surf)

    def draw_pixel_player(self, surf, eye_offset=0, leg_up=False, arms_up=False):
        # Body
        pygame.draw.rect(surf, PINK_PASTEL, (8, 8, 8, 16))
        # Head
        pygame.draw.rect(surf, (255, 220, 230), (6, 0, 12, 10))
        # Eyes
        pygame.draw.rect(surf, BLACK, (10+eye_offset, 4, 2, 2))
        pygame.draw.rect(surf, BLACK, (14+eye_offset, 4, 2, 2))
        # Arms
        if arms_up:
            pygame.draw.rect(surf, (255, 182, 193), (4, 4, 4, 4))
            pygame.draw.rect(surf, (255, 182, 193), (16, 4, 4, 4))
        else:
            pygame.draw.rect(surf, (255, 182, 193), (4, 16, 4, 4))
            pygame.draw.rect(surf, (255, 182, 193), (16, 16, 4, 4))
        # Legs
        if leg_up:
            pygame.draw.rect(surf, (200, 100, 120), (8, 24, 4, 6))
            pygame.draw.rect(surf, (200, 100, 120), (12, 26, 4, 4))
        else:
            pygame.draw.rect(surf, (200, 100, 120), (8, 24, 4, 8))
            pygame.draw.rect(surf, (200, 100, 120), (12, 24, 4, 8))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def handle_input(self, keys, control_scheme):
        self.vel_x = 0
        for action, key_list in control_scheme.items():
            for key in key_list:
                if keys[key]:
                    if action == "left":
                        self.vel_x = -PLAYER_SPEED
                        self.facing_right = False
                    elif action == "right":
                        self.vel_x = PLAYER_SPEED
                        self.facing_right = True
                    elif action == "jump" and self.on_ground:
                        self.vel_y = JUMP_STRENGTH
                        self.on_ground = False

    def update(self, platforms):
        if not self.on_ground:
            self.vel_y += GRAVITY
        self.x += self.vel_x
        self.y += self.vel_y
        if not self.on_ground:
            if self.vel_y < 0:
                self.state = "jump"
            else:
                self.state = "jump"
        else:
            if self.vel_x == 0:
                self.state = "idle"
            else:
                self.state = "walk"
        self.check_collisions(platforms)
        self.animation_counter += 1
        if self.animation_counter >= self.animation_delay:
            self.animation_counter = 0
            self.animation_frame = (self.animation_frame + 1) % 2

    def check_collisions(self, platforms):
        player_rect = self.get_rect()
        self.on_ground = False
        for platform in platforms:
            if player_rect.colliderect(platform):
                if self.vel_y > 0 and player_rect.bottom > platform.top and player_rect.bottom - self.vel_y <= platform.top + 10:
                    self.y = platform.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0 and player_rect.top < platform.bottom and player_rect.top - self.vel_y >= platform.bottom - 10:
                    self.y = platform.bottom
                    self.vel_y = 0
                elif self.vel_x > 0 and player_rect.right > platform.left and player_rect.right - self.vel_x <= platform.left + 10:
                    self.x = platform.left - self.width
                elif self.vel_x < 0 and player_rect.left < platform.right and player_rect.left - self.vel_x >= platform.right - 10:
                    self.x = platform.right
        if self.x < 0:
            self.x = 0
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
        if self.y < 0:
            self.y = 0
            self.vel_y = 0
        if self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
            self.vel_y = 0
            self.on_ground = True

    def draw(self, screen):
        if self.state == "idle":
            sprite = self.sprites["idle"][0]
        elif self.state == "walk":
            sprite = self.sprites["walk"][self.animation_frame]
        else:
            sprite = self.sprites["jump"][0]
        if self.facing_right:
            screen.blit(sprite, (self.x, self.y))
        else:
            flipped = pygame.transform.flip(sprite, True, False)
            screen.blit(flipped, (self.x, self.y)) 
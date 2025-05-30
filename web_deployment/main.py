import asyncio
import pygame
import os
import random
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.8
PLAYER_SPEED = 5
JUMP_STRENGTH = -12

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
PINK_PASTEL = (255, 182, 193)
BLUE_PASTEL = (173, 216, 230)
YELLOW_PASTEL = (255, 255, 204)
GREEN_PASTEL = (204, 255, 204)
PURPLE_PASTEL = (221, 160, 221)

TILE_SIZE = 32
ROOM_ROWS = 15
ROOM_COLS = 25

class MusicManager:
    def __init__(self):
        self.music_files = [
            'assets/music/room1.ogg',
            'assets/music/room2.ogg',
            'assets/music/room3.ogg',
            'assets/music/room4.ogg',
            'assets/music/room5.ogg',
            'assets/music/room6.ogg',
            'assets/music/room7.ogg',
        ]
        self.current_index = -1

    def play(self, index):
        try:
            if index != self.current_index and 0 <= index < len(self.music_files):
                if os.path.exists(self.music_files[index]):
                    pygame.mixer.music.load(self.music_files[index])
                    pygame.mixer.music.play(-1)
                    self.current_index = index
                else:
                    pygame.mixer.music.stop()
                    self.current_index = -1
        except:
            # Gracefully handle audio issues in web
            pass

    def stop(self):
        try:
            pygame.mixer.music.stop()
            self.current_index = -1
        except:
            pass

class Narrator:
    def __init__(self):
        self.font = pygame.font.Font(None, 32)
        self.messages = []
        self.active = False
        self.counter = 0
        self.max_counter = 120
        self.current_message = ""

    def show_message(self, message):
        self.current_message = message
        self.active = True
        self.counter = 0

    def update(self):
        if self.active:
            self.counter += 1
            if self.counter > self.max_counter:
                self.active = False

    def draw(self, screen):
        if self.active:
            box_rect = pygame.Rect(100, 100, SCREEN_WIDTH-200, 100)
            pygame.draw.rect(screen, (30,0,30), box_rect)
            pygame.draw.rect(screen, PINK_PASTEL, box_rect, 3)
            offset = random.randint(-2,2)
            text = self.font.render(self.current_message, True, (255,255,255))
            screen.blit(text, (box_rect.x+20+offset, box_rect.y+30+offset))

class Player:
    def __init__(self):
        self.x = 50
        self.y = 300
        self.width = 20
        self.height = 30
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.color = PINK_PASTEL
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, keys, platforms):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED
        else:
            self.vel_x = 0

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = JUMP_STRENGTH

        self.vel_y += GRAVITY
        if self.vel_y > 15:
            self.vel_y = 15

        self.x += self.vel_x
        self.y += self.vel_y

        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width

        if self.y > SCREEN_HEIGHT:
            self.y = 300
            self.x = 50

        self.rect.x = self.x
        self.rect.y = self.y

        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform) and self.vel_y > 0:
                self.y = platform.top - self.height
                self.vel_y = 0
                self.on_ground = True
                break

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.circle(screen, YELLOW_PASTEL, (self.x + self.width//2, self.y + 5), 5)

class RoomBase:
    def __init__(self, player):
        self.player = player
        self.platforms = []
        self.goal = None
        self.setup_platforms()
        self.setup_goal()

    def setup_platforms(self):
        pass

    def setup_goal(self):
        self.goal = pygame.Rect(750, 250, 30, 30)

    def check_goal_reached(self):
        return self.player.rect.colliderect(self.goal)

    def update(self, keys):
        self.player.update(keys, self.platforms)

    def draw(self, screen):
        for platform in self.platforms:
            pygame.draw.rect(screen, GRAY, platform)
        if self.goal:
            pygame.draw.rect(screen, GREEN, self.goal)
        self.player.draw(screen)

class RoomNormal(RoomBase):
    def setup_platforms(self):
        self.platforms = [
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(200, 450, 100, 20),
            pygame.Rect(400, 350, 100, 20),
            pygame.Rect(600, 250, 100, 20)
        ]

class RoomGravity(RoomBase):
    def __init__(self, player):
        super().__init__(player)
        self.gravity_multiplier = 2

    def setup_platforms(self):
        self.platforms = [
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(150, 450, 80, 20),
            pygame.Rect(300, 350, 80, 20),
            pygame.Rect(450, 250, 80, 20),
            pygame.Rect(600, 150, 80, 20)
        ]

    def update(self, keys):
        original_gravity = GRAVITY
        global GRAVITY
        GRAVITY = original_gravity * self.gravity_multiplier
        self.player.update(keys, self.platforms)
        GRAVITY = original_gravity

class RoomMomentum(RoomBase):
    def __init__(self, player):
        super().__init__(player)
        self.friction = 0.8

    def setup_platforms(self):
        self.platforms = [
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(100, 450, 60, 20),
            pygame.Rect(250, 350, 60, 20),
            pygame.Rect(400, 250, 60, 20),
            pygame.Rect(550, 150, 60, 20),
            pygame.Rect(700, 100, 60, 20)
        ]

    def update(self, keys):
        self.player.update(keys, self.platforms)
        self.player.vel_x *= self.friction

class RoomReversed(RoomBase):
    def update(self, keys):
        reversed_keys = {}
        for key in keys:
            reversed_keys[key] = False
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            reversed_keys[pygame.K_RIGHT] = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            reversed_keys[pygame.K_LEFT] = True
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            reversed_keys[pygame.K_SPACE] = True
            
        self.player.update(reversed_keys, self.platforms)

    def setup_platforms(self):
        self.platforms = [
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(250, 450, 100, 20),
            pygame.Rect(450, 350, 100, 20)
        ]

class RoomRandom(RoomBase):
    def __init__(self, player):
        super().__init__(player)
        self.platform_timer = 0
        self.platform_change_interval = 120

    def setup_platforms(self):
        self.regenerate_platforms()

    def regenerate_platforms(self):
        self.platforms = [pygame.Rect(0, 550, 800, 50)]
        for i in range(5):
            x = random.randint(50, 700)
            y = random.randint(200, 500)
            width = random.randint(60, 120)
            self.platforms.append(pygame.Rect(x, y, width, 20))

    def update(self, keys):
        self.platform_timer += 1
        if self.platform_timer >= self.platform_change_interval:
            self.regenerate_platforms()
            self.platform_timer = 0
        self.player.update(keys, self.platforms)

class RoomDelayed(RoomBase):
    def __init__(self, player):
        super().__init__(player)
        self.input_buffer = []
        self.buffer_size = 30

    def setup_platforms(self):
        self.platforms = [
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(200, 450, 100, 20),
            pygame.Rect(400, 350, 100, 20),
            pygame.Rect(100, 250, 100, 20),
            pygame.Rect(600, 200, 100, 20)
        ]

    def update(self, keys):
        current_keys = {}
        for key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_UP]:
            current_keys[key] = keys[key]

        self.input_buffer.append(current_keys)
        if len(self.input_buffer) > self.buffer_size:
            delayed_keys = self.input_buffer.pop(0)
            self.player.update(delayed_keys, self.platforms)
        else:
            empty_keys = {key: False for key in current_keys}
            self.player.update(empty_keys, self.platforms)

class RoomFinal(RoomBase):
    def __init__(self, player):
        super().__init__(player)
        self.effects = ['gravity', 'momentum', 'reversed', 'random', 'delayed']
        self.current_effect = 0
        self.effect_timer = 0
        self.effect_duration = 180
        self.gravity_multiplier = 2
        self.friction = 0.8
        self.input_buffer = []
        self.buffer_size = 30
        self.platform_timer = 0
        self.platform_change_interval = 120

    def setup_platforms(self):
        self.platforms = [
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(100, 450, 80, 20),
            pygame.Rect(250, 380, 80, 20),
            pygame.Rect(400, 310, 80, 20),
            pygame.Rect(550, 240, 80, 20),
            pygame.Rect(350, 170, 80, 20),
            pygame.Rect(200, 100, 80, 20)
        ]

    def setup_goal(self):
        self.goal = pygame.Rect(220, 50, 30, 30)

    def update(self, keys):
        self.effect_timer += 1
        if self.effect_timer >= self.effect_duration:
            self.current_effect = (self.current_effect + 1) % len(self.effects)
            self.effect_timer = 0

        effect = self.effects[self.current_effect]
        
        if effect == 'gravity':
            original_gravity = GRAVITY
            global GRAVITY
            GRAVITY = original_gravity * self.gravity_multiplier
            self.player.update(keys, self.platforms)
            GRAVITY = original_gravity
        elif effect == 'momentum':
            self.player.update(keys, self.platforms)
            self.player.vel_x *= self.friction
        elif effect == 'reversed':
            reversed_keys = {}
            for key in keys:
                reversed_keys[key] = False
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                reversed_keys[pygame.K_RIGHT] = True
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                reversed_keys[pygame.K_LEFT] = True
            if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
                reversed_keys[pygame.K_SPACE] = True
            self.player.update(reversed_keys, self.platforms)
        elif effect == 'random':
            self.platform_timer += 1
            if self.platform_timer >= self.platform_change_interval:
                self.regenerate_platforms()
                self.platform_timer = 0
            self.player.update(keys, self.platforms)
        elif effect == 'delayed':
            current_keys = {}
            for key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_UP]:
                current_keys[key] = keys[key]
            self.input_buffer.append(current_keys)
            if len(self.input_buffer) > self.buffer_size:
                delayed_keys = self.input_buffer.pop(0)
                self.player.update(delayed_keys, self.platforms)
            else:
                empty_keys = {key: False for key in current_keys}
                self.player.update(empty_keys, self.platforms)

    def regenerate_platforms(self):
        self.platforms = [pygame.Rect(0, 550, 800, 50)]
        for i in range(6):
            x = random.randint(50, 650)
            y = random.randint(100, 500)
            width = random.randint(60, 100)
            self.platforms.append(pygame.Rect(x, y, width, 20))

    def draw(self, screen):
        super().draw(screen)
        font = pygame.font.Font(None, 24)
        effect_text = font.render(f"Effect: {self.effects[self.current_effect]}", True, WHITE)
        screen.blit(effect_text, (10, 10))

class RoomManager:
    def __init__(self, player):
        self.player = player
        self.rooms = [
            RoomNormal(player),
            RoomGravity(player),
            RoomMomentum(player),
            RoomReversed(player),
            RoomRandom(player),
            RoomDelayed(player),
            RoomFinal(player)
        ]
        self.current_room = 0

    def get_current_room(self):
        return self.rooms[self.current_room]

    def next_room(self):
        if self.current_room < len(self.rooms) - 1:
            self.current_room += 1
            self.player.x = 50
            self.player.y = 300
            self.player.vel_x = 0
            self.player.vel_y = 0
            return True
        return False

    def get_room_count(self):
        return len(self.rooms)

    def set_room(self, room_index):
        if 0 <= room_index < len(self.rooms):
            self.current_room = room_index
            self.player.x = 50
            self.player.y = 300
            self.player.vel_x = 0
            self.player.vel_y = 0

class EndingSequence:
    def __init__(self):
        self.state = "dialogue"
        self.dialogues = [
            "oh you are here",
            "well...",
            "I should've expected that"
        ]
        self.dialogue_index = 0
        self.dialogue_timer = 0
        self.dialogue_duration = 5 * FPS
        self.done = False
        self.fade_timer = 0
        self.fade_duration = FPS
        self.choice_options = ["get revenge", "forgive him"]
        self.selected_option = 0
        self.choice_active = False
        self.choice_made = False

    def update(self, keys, player):
        if self.state == "dialogue":
            self.dialogue_timer += 1
            if self.dialogue_timer >= self.dialogue_duration:
                self.dialogue_index += 1
                self.dialogue_timer = 0
                if self.dialogue_index >= len(self.dialogues):
                    self.state = "fade"
                    self.fade_timer = 0
        elif self.state == "fade":
            self.fade_timer += 1
            if self.fade_timer >= self.fade_duration:
                self.state = "choice"
                self.choice_active = True
        elif self.state == "choice":
            if not self.choice_made:
                if keys[pygame.K_LEFT]:
                    self.selected_option = 0
                elif keys[pygame.K_RIGHT]:
                    self.selected_option = 1
                if keys[pygame.K_SPACE]:
                    self.choice_made = True
                    if self.selected_option == 0:
                        pygame.quit()
                        sys.exit()
                    else:
                        self.done = True
        elif self.state == "game_over":
            self.done = True
        return not self.done

    def draw(self, screen, player):
        screen.fill((20, 0, 20))
        if self.state == "dialogue":
            pygame.draw.rect(screen, GRAY, (350, 200, 100, 80))
            pygame.draw.rect(screen, BLACK, (360, 210, 80, 60))
            pygame.draw.rect(screen, GRAY, (370, 280, 60, 40))
            pygame.draw.rect(screen, PINK_PASTEL, (400, 240, 20, 40))
            pygame.draw.circle(screen, YELLOW_PASTEL, (410, 230), 10)
            if self.dialogue_index < len(self.dialogues):
                font = pygame.font.Font(None, 40)
                text = font.render(self.dialogues[self.dialogue_index], True, WHITE)
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 350))
        elif self.state == "fade":
            fade_alpha = int(255 * (self.fade_timer / self.fade_duration))
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))
        elif self.state == "choice":
            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 48)
            for i, option in enumerate(self.choice_options):
                if i == self.selected_option:
                    color = PINK_PASTEL
                else:
                    color = GRAY
                text = font.render(f"[{option}]", True, color)
                x = SCREEN_WIDTH // 2 - 200 + i * 400 - text.get_width() // 2
                y = SCREEN_HEIGHT // 2 - text.get_height() // 2
                screen.blit(text, (x, y))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Control Shift")
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.room_manager = RoomManager(self.player)
        self.running = True
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        self.game_state = "PLAYING"
        self.transition_counter = 0
        self.transition_message = ""
        self.title_screen = True
        self.level_select_screen = False
        self.music_manager = MusicManager()
        self.narrator = Narrator()
        self.current_room_index = 0
        self.background_seed = 0
        try:
            pygame.mixer.init()
            self.music_manager.play(self.current_room_index)
        except:
            pass
        self.ending_sequence = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.title_screen:
                    if event.key == pygame.K_SPACE:
                        self.title_screen = False
                    elif event.key == pygame.K_l:
                        self.title_screen = False
                        self.level_select_screen = True
                elif self.level_select_screen:
                    if event.key >= pygame.K_1 and event.key <= pygame.K_7:
                        level = event.key - pygame.K_1
                        self.room_manager.set_room(level)
                        self.current_room_index = level
                        self.music_manager.play(self.current_room_index)
                        self.level_select_screen = False
                        self.narrator.show_message(f"Jumped to level {level + 1}")
                    elif event.key == pygame.K_ESCAPE:
                        self.level_select_screen = False
                        self.title_screen = True

    def update(self):
        if self.title_screen or self.level_select_screen:
            return

        if self.game_state == "ENDING_SEQUENCE":
            keys = pygame.key.get_pressed()
            if not self.ending_sequence.update(keys, self.player):
                self.current_room_index = 0
                self.room_manager.set_room(0)
                self.music_manager.play(0)
                self.game_state = "PLAYING"
                self.ending_sequence = None
            return

        if self.game_state == "TRANSITION":
            self.transition_counter += 1
            if self.transition_counter >= 180:
                self.game_state = "PLAYING"
                self.transition_counter = 0
            return

        keys = pygame.key.get_pressed()
        current_room = self.room_manager.get_current_room()
        current_room.update(keys)
        self.narrator.update()

        if current_room.check_goal_reached():
            if self.room_manager.current_room == self.room_manager.get_room_count() - 1:
                self.game_state = "ENDING_SEQUENCE"
                self.ending_sequence = EndingSequence()
            else:
                if self.room_manager.next_room():
                    self.current_room_index = self.room_manager.current_room
                    self.music_manager.play(self.current_room_index)
                    self.transition_to_next_room(f"Level {self.current_room_index + 1}")

    def transition_to_next_room(self, message):
        self.game_state = "TRANSITION"
        self.transition_counter = 0
        self.transition_message = message
        random.seed(self.current_room_index)
        self.background_seed = random.randint(0, 1000)

    def draw(self):
        if self.title_screen:
            self.draw_title_screen()
        elif self.level_select_screen:
            self.draw_level_select_screen()
        elif self.game_state == "ENDING_SEQUENCE":
            self.ending_sequence.draw(self.screen, self.player)
        elif self.game_state == "TRANSITION":
            self.draw_transition_screen()
        else:
            self.draw_background(self.current_room_index)
            current_room = self.room_manager.get_current_room()
            current_room.draw(self.screen)
            room_text = self.font.render(f"Room {self.current_room_index + 1}/{self.room_manager.get_room_count()}", True, WHITE)
            self.screen.blit(room_text, (10, 10))
            self.narrator.draw(self.screen)

        pygame.display.flip()

    def draw_background(self, room_index):
        random.seed(room_index + self.background_seed)
        self.screen.fill(BLACK)
        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(1, 3)
            brightness = random.randint(100, 255)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.screen, color, (x, y), size)

    def draw_title_screen(self):
        self.screen.fill(BLACK)
        title_text = self.large_font.render("Control Shift", True, PINK_PASTEL)
        start_text = self.font.render("Press SPACE to start", True, WHITE)
        level_select_text = self.font.render("Press L for level select", True, WHITE)
        
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        level_rect = level_select_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        
        self.screen.blit(title_text, title_rect)
        self.screen.blit(start_text, start_rect)
        self.screen.blit(level_select_text, level_rect)

    def draw_level_select_screen(self):
        self.screen.fill(BLACK)
        title_text = self.large_font.render("Level Select", True, PINK_PASTEL)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title_text, title_rect)
        
        level_names = [
            "1. Normal Room",
            "2. High Gravity",
            "3. Momentum",
            "4. Reversed Controls",
            "5. Random Platforms",
            "6. Delayed Input",
            "7. Final Challenge"
        ]
        
        for i, name in enumerate(level_names):
            text = self.font.render(name, True, WHITE)
            y = 200 + i * 40
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, y))
            self.screen.blit(text, text_rect)
        
        escape_text = self.font.render("Press ESC to return", True, GRAY)
        escape_rect = escape_text.get_rect(center=(SCREEN_WIDTH//2, 500))
        self.screen.blit(escape_text, escape_rect)

    def draw_transition_screen(self):
        self.screen.fill(BLACK)
        text = self.large_font.render(self.transition_message, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, text_rect)

    async def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            await asyncio.sleep(0)

async def main():
    pygame.init()
    game = Game()
    await game.run()
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main()) 
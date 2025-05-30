import pygame
import asyncio
from src.constants import *
from src.player import Player
from src.rooms.room_manager import RoomManager
import os
import sys
import random

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class MusicManager:
    def __init__(self):
        self.music_files = [
            get_resource_path('assets/music/room1.ogg'),
            get_resource_path('assets/music/room2.ogg'),
            get_resource_path('assets/music/room3.ogg'),
            get_resource_path('assets/music/room4.ogg'),
            get_resource_path('assets/music/room5.ogg'),
            get_resource_path('assets/music/room6.ogg'),
            get_resource_path('assets/music/room7.ogg'),
        ]
        self.current_index = -1

    def play(self, index):
        if index != self.current_index and 0 <= index < len(self.music_files):
            music_file = self.music_files[index]
            print(f"Trying to play: {music_file}")  # Debug output
            if os.path.exists(music_file):
                try:
                    pygame.mixer.music.load(music_file)
                    pygame.mixer.music.play(-1)
                    self.current_index = index
                    print(f"✅ Playing music: {music_file}")
                except pygame.error as e:
                    print(f"❌ Failed to play music: {e}")
                    pygame.mixer.music.stop()
                    self.current_index = -1
            else:
                print(f"❌ Music file not found: {music_file}")
                pygame.mixer.music.stop()
                self.current_index = -1

    def stop(self):
        pygame.mixer.music.stop()
        self.current_index = -1

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
            # Draw a glitchy text box
            box_rect = pygame.Rect(100, 100, SCREEN_WIDTH-200, 100)
            pygame.draw.rect(screen, (30,0,30), box_rect)
            pygame.draw.rect(screen, PINK_PASTEL, box_rect, 3)
            # Glitch effect
            offset = random.randint(-2,2)
            text = self.font.render(self.current_message, True, (255,255,255))
            screen.blit(text, (box_rect.x+20+offset, box_rect.y+30+offset))

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
        self.dialogue_duration = 5 * FPS  # 5 seconds per line
        self.done = False
        self.fade_timer = 0
        self.fade_duration = FPS  # 1 second fade
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
                        # get revenge: quit game
                        import sys
                        pygame.quit()
                        sys.exit()
                    else:
                        # forgive him: restart at first level, no door
                        self.done = True
        elif self.state == "game_over":
            self.done = True
        return not self.done

    def draw(self, screen, player):
        screen.fill((20, 0, 20))
        if self.state == "dialogue":
            # Draw computer
            pygame.draw.rect(screen, GRAY, (350, 200, 100, 80))
            pygame.draw.rect(screen, BLACK, (360, 210, 80, 60))
            pygame.draw.rect(screen, GRAY, (370, 280, 60, 40))
            # Draw evil character at computer
            pygame.draw.rect(screen, PINK_PASTEL, (400, 240, 20, 40))
            pygame.draw.circle(screen, YELLOW_PASTEL, (410, 230), 10)
            if self.dialogue_index < len(self.dialogues):
                font = pygame.font.Font(None, 40)
                text = font.render(self.dialogues[self.dialogue_index], True, WHITE)
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 350))
        elif self.state == "fade":
            # Fade to black
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
        elif self.state == "game_over":
            screen.fill((20, 0, 20))
            font = pygame.font.Font(None, 64)
            text = font.render("GAME OVER (for him)", True, RED)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

class Game:
    def __init__(self):
        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Control Shift")
        
        # Set up the clock
        self.clock = pygame.time.Clock()
        
        # Set up game objects
        self.player = Player()
        self.room_manager = RoomManager(self.player)
        
        # Game state
        self.running = True
        
        # Font for displaying messages
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        
        # Game state
        self.game_state = "PLAYING"  # PLAYING, TRANSITION, ENDING_SEQUENCE, CREDITS, LEVEL_SELECT
        self.transition_counter = 0
        self.transition_message = ""
        
        # Load game title screen
        self.title_screen = True
        self.level_select_screen = False
        
        # Music manager
        self.music_manager = MusicManager()
        self.narrator = Narrator()
        self.current_room_index = 0
        self.background_seed = 0
        pygame.mixer.init()
        self.music_manager.play(self.current_room_index)
        
        self.ending_sequence = None
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Handle title screen input
            if self.title_screen and event.type == pygame.KEYDOWN:
                self.title_screen = False
                self.level_select_screen = True
                return
                
            # Handle level select screen
            if self.level_select_screen and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Start from beginning
                    self.level_select_screen = False
                    self.game_state = "PLAYING"
                elif event.key >= pygame.K_1 and event.key <= pygame.K_7:
                    # Jump to specific level
                    level_num = event.key - pygame.K_1
                    self.level_select_screen = False
                    self.game_state = "PLAYING"
                    self.room_manager.current_room_index = level_num
                    self.room_manager.current_room = self.room_manager.rooms[level_num]
                    self.room_manager.current_room.enter()
                    self.current_room_index = level_num
                    self.music_manager.play(self.current_room_index)
                return
                
            # In transition state, wait for any key to continue
            if self.game_state == "TRANSITION" and event.type == pygame.KEYDOWN:
                self.game_state = "PLAYING"
                self.narrator.active = False
                return
                
            # Let the current room handle the input if we're playing
            if self.game_state == "PLAYING":
                self.room_manager.handle_event(event)
            elif self.game_state == "ENDING_SEQUENCE":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.ending_sequence:
                        keys = pygame.key.get_pressed()
                        self.ending_sequence.update(keys, self.player)
    
    def update(self):
        if self.title_screen or self.level_select_screen or self.game_state == "TRANSITION":
            self.narrator.update()
            return
        if self.game_state == "ENDING_SEQUENCE":
            if self.ending_sequence:
                keys = pygame.key.get_pressed()
                still_running = self.ending_sequence.update(keys, self.player)
                if not still_running:
                    # Check if forgiveness was chosen
                    if hasattr(self.ending_sequence, 'state') and self.ending_sequence.state == 'choice' and self.ending_sequence.selected_option == 1:
                        self.room_manager.reset_first_room_no_door()
                        self.game_state = "PLAYING"
                        self.ending_sequence = None
                    else:
                        self.game_state = "CREDITS"
            return
            
        # Update the current room
        room_completed, message = self.room_manager.update()
        
        # Handle room transition if the current room is completed
        if room_completed:
            self.transition_to_next_room(message)
    
    def transition_to_next_room(self, message):
        self.game_state = "TRANSITION"
        self.transition_counter = 0
        self.transition_message = message
        self.room_manager.next_room()
        self.current_room_index = self.room_manager.current_room_index
        self.music_manager.play(self.current_room_index)
        self.background_seed = random.randint(0,10000)
        evil_lines = [
            "Did you like that? Let's make it harder...",
            "You thought you had control? Think again!",
            "I'm just getting started...",
            "Your hands are not your own!",
            "Try to keep up!",
            "I can do this all day...",
            "This is my world now!"
        ]
        self.narrator.show_message(random.choice(evil_lines))
        if self.current_room_index == 0:  # Completed all rooms
            self.game_state = "ENDING_SEQUENCE"
            self.ending_sequence = EndingSequence()
    
    def draw(self):
        self.draw_background(self.current_room_index)
        # Clear the screen
        self.screen.fill(BLACK)
        
        if self.title_screen:
            self.draw_title_screen()
        elif self.level_select_screen:
            self.draw_level_select_screen()
        elif self.game_state == "TRANSITION":
            self.draw_transition_screen()
            self.narrator.draw(self.screen)
        elif self.game_state == "ENDING_SEQUENCE":
            if self.ending_sequence:
                self.ending_sequence.draw(self.screen, self.player)
        elif self.game_state == "CREDITS":
            self.screen.fill(BLACK)
            font = pygame.font.Font(None, 48)
            text1 = font.render("GAME OVER (for him)", True, RED)
            text2 = font.render("Congratulations!", True, GREEN)
            text3 = font.render("Thanks for playing Control Shift!", True, WHITE)
            self.screen.blit(text1, (SCREEN_WIDTH // 2 - text1.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
            self.screen.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
            self.screen.blit(text3, (SCREEN_WIDTH // 2 - text3.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
        else:
            # Draw the current room
            self.room_manager.draw(self.screen)
            
            # Draw UI elements like hints
            control_hint = self.room_manager.get_control_hint()
            if control_hint:
                hint_text = self.font.render(control_hint, True, WHITE)
                self.screen.blit(hint_text, (10, SCREEN_HEIGHT - 30))
        
        # Update the display
        pygame.display.flip()
    
    def draw_background(self, room_index):
        random.seed(self.background_seed + room_index)
        # Choose a base color per room
        base_colors = [
            (20, 20, 60), (40, 20, 40), (20, 40, 20), (40, 40, 20),
            (20, 40, 60), (60, 20, 40), (40, 60, 20)
        ]
        color = base_colors[room_index % len(base_colors)]
        self.screen.fill(color)
        # Draw 8-bit geometric patterns
        pattern_type = room_index % 3
        for y in range(0, SCREEN_HEIGHT, 16):
            for x in range(0, SCREEN_WIDTH, 16):
                if pattern_type == 0:  # Checker
                    if (x//16 + y//16) % 2 == 0:
                        pygame.draw.rect(self.screen, (min(color[0]+30,255), min(color[1]+30,255), min(color[2]+30,255)), (x, y, 16, 16))
                elif pattern_type == 1:  # Stripes
                    if (y//16) % 2 == 0:
                        pygame.draw.rect(self.screen, (max(color[0]-20,0), max(color[1]-20,0), max(color[2]-20,0)), (x, y, 16, 16))
                elif pattern_type == 2:  # Dots
                    if random.random() < 0.2:
                        pygame.draw.circle(self.screen, (255,255,255), (x+8, y+8), 2)

    def draw_title_screen(self):
        # Draw title
        title = self.large_font.render("CONTROL SHIFT", True, PINK_PASTEL)
        subtitle = self.font.render("Something strange is happening to your controls...", True, WHITE)
        start_text = self.font.render("Press any key to begin", True, LIGHT_GRAY)
        
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT * 2 // 3))

    def draw_level_select_screen(self):
        # Draw level select screen
        self.screen.fill((30, 0, 50))
        
        title = self.large_font.render("SELECT LEVEL", True, PINK_PASTEL)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        # Level descriptions
        levels = [
            "1 - Normal: Learn the basics",
            "2 - Reversed: Left is right, right is left",
            "3 - Delayed: Your inputs are delayed",
            "4 - Chaos: Controls change randomly",
            "5 - Momentum: Slippery ice physics",
            "6 - Gravity: Everything is upside down",
            "7 - Final: The ultimate challenge"
        ]
        
        y_start = 150
        for i, level_desc in enumerate(levels):
            color = WHITE if i < len(self.room_manager.rooms) else GRAY
            text = self.font.render(level_desc, True, color)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_start + i * 40))
        
        # Instructions
        instructions = [
            "Press 1-7 to jump to a specific level",
            "Press SPACE to start from the beginning",
        ]
        
        y_start = 450
        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, LIGHT_GRAY)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_start + i * 30))

    def draw_transition_screen(self):
        # Draw transition message
        message = self.large_font.render(self.transition_message, True, PINK_PASTEL)
        continue_text = self.font.render("Press any key to continue", True, WHITE)
        
        self.screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        
        # Increment transition counter
        self.transition_counter += 1

    def run(self):
        # Main game loop
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    async def run_async(self):
        # Async main game loop for web deployment
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            await asyncio.sleep(0)  # Allow other tasks to run

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
    pygame.quit() 
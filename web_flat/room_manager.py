import pygame
import platform
from constants import *
from room_normal import NormalRoom
from room_reversed import ReversedRoom
from room_inverted import InvertedRoom
from room_gravity import GravityRoom
from room_speed import SpeedRoom
from room_dark import DarkRoom
from room_final import FinalRoom

print("DEBUG: Loading room_manager.py")

def is_web_platform():
    return platform.system().lower() == "emscripten"

class RoomManager:
    def __init__(self, player):
        print("DEBUG: RoomManager.__init__ started")
        try:
            self.player = player
            self.current_room_index = 0
            
            # Quirky transition messages
            self.transition_messages = [
                "Something changed...",
                "What's happening?",
                "The rules just shifted!",
                "The controls feel weird...",
                "This is getting strange!",
                "Everything's upside down!",
                "Pure chaos ahead..."
            ]
            
            # Create all the rooms
            print("DEBUG: Creating rooms")
            self.rooms = [
                NormalRoom(player),           # Room 1: Normal controls
                ReversedRoom(player),         # Room 2: Left is right, right is left
                InvertedRoom(player),         # Room 3: Up is down, down is up
                GravityRoom(player),          # Room 4: Low gravity
                SpeedRoom(player),            # Room 5: Super speed
                DarkRoom(player),             # Room 6: Limited visibility
                FinalRoom(player)             # Room 7: The end
            ]
            print("DEBUG: Rooms created")
            
            # Initialize font with error handling
            print("DEBUG: Initializing font")
            try:
                pygame.font.init()
                self.font = pygame.font.Font(None, 36)
                print("DEBUG: Font initialized")
            except Exception as e:
                print(f"DEBUG ERROR: Font initialization failed: {str(e)}")
                try:
                    self.font = pygame.font.SysFont('Arial', 36)
                    print("DEBUG: Fallback font initialized")
                except Exception as e2:
                    print(f"DEBUG ERROR: Fallback font failed: {str(e2)}")
                    self.font = None
            
            # Initialize transition state
            self.transition_timer = 0
            self.transition_duration = 60  # frames
            self.in_transition = False
            self.transition_message = ""
            print("DEBUG: RoomManager initialization complete")
            
        except Exception as e:
            print(f"DEBUG ERROR: RoomManager initialization failed: {str(e)}")
            raise

    def get_current_room(self):
        try:
            return self.rooms[self.current_room_index]
        except Exception as e:
            print(f"DEBUG ERROR: Failed to get current room: {str(e)}")
            return self.rooms[0]  # Fallback to first room

    def update(self, keys):
        try:
            if self.in_transition:
                self.transition_timer += 1
                if self.transition_timer >= self.transition_duration:
                    self.in_transition = False
                    self.transition_timer = 0
            else:
                current_room = self.get_current_room()
                if current_room.is_complete():
                    print("DEBUG: Room complete, transitioning")
                    self.start_transition()
                else:
                    current_room.update(keys)
        except Exception as e:
            print(f"DEBUG ERROR: Room update failed: {str(e)}")
            self.in_transition = False
            self.transition_timer = 0

    def start_transition(self):
        try:
            if self.current_room_index < len(self.rooms) - 1:
                self.current_room_index += 1
                self.in_transition = True
                self.transition_timer = 0
                self.transition_message = self.transition_messages[self.current_room_index - 1]
                print(f"DEBUG: Starting transition to room {self.current_room_index}")
            else:
                print("DEBUG: Game complete")
        except Exception as e:
            print(f"DEBUG ERROR: Transition failed: {str(e)}")
            self.in_transition = False

    def draw(self, screen):
        try:
            if self.in_transition:
                # Draw transition screen
                screen.fill(BLACK)
                if self.font:
                    try:
                        text = self.font.render(self.transition_message, True, WHITE)
                        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                        screen.blit(text, text_rect)
                    except Exception as e:
                        print(f"DEBUG ERROR: Transition text rendering failed: {str(e)}")
            else:
                # Draw current room
                current_room = self.get_current_room()
                current_room.draw(screen)
        except Exception as e:
            print(f"DEBUG ERROR: Room drawing failed: {str(e)}")
            # Fallback to black screen
            screen.fill(BLACK)
    
    def handle_event(self, event):
        try:
            self.current_room.handle_event(event)
        except Exception as e:
            print(f"DEBUG ERROR: Room event handling failed: {str(e)}")
    
    def next_room(self):
        try:
            print("DEBUG: Moving to next room")
            # Increment the room index
            self.current_room_index = (self.current_room_index + 1) % len(self.rooms)
            
            # Update the current room
            self.current_room = self.rooms[self.current_room_index]
            self.current_room.enter()
            print(f"DEBUG: Moved to room {self.current_room_index}")
        except Exception as e:
            print(f"DEBUG ERROR: Room transition failed: {str(e)}")
    
    def get_control_hint(self):
        try:
            # Get the hint from the current room
            return self.current_room.get_hint()
        except Exception as e:
            print(f"DEBUG ERROR: Getting control hint failed: {str(e)}")
            return ""
    
    def reset_first_room_no_door(self):
        try:
            print("DEBUG: Resetting first room without door")
            # Replace the first room with a version that has no door
            self.rooms[0] = NormalRoom(self.player, hide_door=True)
            self.current_room_index = 0
            self.current_room = self.rooms[0]
            self.current_room.enter()
            print("DEBUG: First room reset complete")
        except Exception as e:
            print(f"DEBUG ERROR: Resetting first room failed: {str(e)}") 
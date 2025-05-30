import pygame
from src.constants import *
from src.rooms.room_normal import NormalRoom
from src.rooms.room_reversed import ReversedRoom
from src.rooms.room_delayed import DelayedRoom
from src.rooms.room_random import RandomRoom
from src.rooms.room_momentum import MomentumRoom
from src.rooms.room_gravity import GravityRoom
from src.rooms.room_final import FinalRoom

class RoomManager:
    def __init__(self, player):
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
        self.rooms = [
            NormalRoom(player),           # Room 1: Normal controls
            ReversedRoom(player),         # Room 2: Left/right reversed
            DelayedRoom(player),          # Room 3: Delayed controls
            RandomRoom(player),           # Room 4: Random key mappings
            MomentumRoom(player),         # Room 5: Momentum-based movement
            GravityRoom(player),          # Room 6: Reversed gravity
            FinalRoom(player)             # Room 7: Final challenge combining mechanics
        ]
        
        # Initialize the first room
        self.current_room = self.rooms[self.current_room_index]
        self.current_room.enter()
    
    def handle_event(self, event):
        self.current_room.handle_event(event)
    
    def update(self):
        # Update the current room
        room_completed = self.current_room.update()
        
        # Return completion status and transition message
        if room_completed:
            return True, self.transition_messages[self.current_room_index]
        
        return False, ""
    
    def next_room(self):
        # Increment the room index
        self.current_room_index = (self.current_room_index + 1) % len(self.rooms)
        
        # Update the current room
        self.current_room = self.rooms[self.current_room_index]
        self.current_room.enter()
    
    def draw(self, screen):
        # Draw the current room
        self.current_room.draw(screen)
    
    def get_control_hint(self):
        # Get the hint from the current room
        return self.current_room.get_hint()
    
    def reset_first_room_no_door(self):
        # Replace the first room with a version that has no door
        self.rooms[0] = NormalRoom(self.player, hide_door=True)
        self.current_room_index = 0
        self.current_room = self.rooms[0]
        self.current_room.enter() 
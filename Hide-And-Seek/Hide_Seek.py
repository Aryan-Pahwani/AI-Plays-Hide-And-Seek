import pygame
import random
import math
from enum import Enum
from Player import Player

pygame.init()

class GameInformation:
    def __init__(self, time):
        self.time = time

class Game:
    #Information
    TIME_FONT = pygame.font.SysFont("monospace", 50)
    walls = []
    
    class Color(Enum):    
        BG = (0, 0, 0)
        SEEKER = (255, 86, 102)
        HIDER = (67, 129, 193)
        HIDER_RAYCAST = (124, 165, 184)
        SEEKER_RAYCAST = (254, 168, 47)
        WALL = (255, 255, 255)
    
    class Wall(object):
        def __init__(self, position, side):
            self.walls.append(self)
            self.rect = pygame.Rect(position[0], position[1], side, side)


    
    def __init__(self, window, window_width, window_height, game_map):
        self.window_width = window_width
        self.window_height = window_height

        #
        # Important Game Object Defining
        #


        
        self.map = game_map
        
        self.Time_Left = 0

        _construct_walls(self, 30, self.map) # Defines walls
        
        Seeker = Player(self.walls)
        Hider = Player(self.walls)

    
    def _draw_time(self):
        """
        Draws current time on Screen.
        """
        Time_Text = self.TIME_FONT.render(f"{self.Time_Left}", 1, self.Color.WALL)
        self.window.blit(Time_Text, (self.window_width//4 - Time_Text.get_width()//2, 20))


    
    def _construct_walls(self, side : int, map):
        """
        Constructs walls based on --> map.
        
        Each wall will be a square --> size*size

        """
        # TODO: Wall Construction Logic
        # Parser
        x = y = 0
        for row in map:
            for column in row:
                if column == "1":
                    Wall((x, y), side)
                x+=side
            y+=side
            x=0


    
    def _player_raycasts(self):
        """
        Handles raycasts emitted by the player.
        
        Constructs the raycast.

        Also checks for collision.
        """
        # TODO: Raycast Logic
        pass


    
    def draw(self, draw_time=True, draw_raycast=False):
        self.window.fill(self.Color.BG)

        if draw_time == True:
            self._draw_time()

        # TODO: Hider & Seeker Drawing Logic
        for wall in self.walls:
            pygame.draw.rect(display, self.Color.WALL, wall.rect)
            # for i in range(len(Hiderrays)):
            #     if wall.rect.clipline(Hiderrays[i].Line):
            #         HiderEyes[i] = "wall"
            # for j in range(len(Seekerrays)):
            #     if wall.rect.clipline(Seekerrays[j].Line):
            #         SeekerEyes[j] = "wall"
    
        # TODO: Raycast Drawing Logic



    
    def Move_Character(self, character : Player, direction, speed):
        """
        Moves the specified character. (might instead use seperate script instead, idk)

        Direction must be in the form (x, y)
        """
        
        # TODO: Player Movement Logic
        character.move(direction*speed)


    
    def loop(self):
        """
        Executes one single game loop.
        """
        
        game_info = GameInformation(self.map, self.time)

        return game_info
        #pass



    
    def reset(self):
        """
        resets the entire game
        """
        # TODO: Implement reset (if necessary)
        pass
import pygame
import sys
import os
import random
import neat
import math
pygame.init()

# Global Constants

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

PLAYER_SIZE = 30 #Size in pixels


# player class

class player:
    MOV_SPEED = 10
    colour = (0, 0, 0)
    def __init__(self, player_size, SCREEN):
        self.rect = pygame.Rect((0, 0), (player_size, player_size))
        self.SCREEN = SCREEN
    
    def move(self, dx, dy):
        
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self._movesingleaxis(dx*self.MOV_SPEED, 0)
        if dy != 0:
            self._movesingleaxis(0, dy*self.MOV_SPEED)

    def _movesingleaxis(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        
    
    def draw(self):
        pygame.draw.rect(self.SCREEN, self.colour, self.rect)


# Hider


class Hider(player):
    def __init__(self):
        super().__init__(PLAYER_SIZE, SCREEN)
        # Stuff
        self.MOV_SPEED = 10
        self.rect.x = self.rect.y = random.randint(1, 100)

        

class Seeker(player):
    def __init__(self):
        super().__init__(PLAYER_SIZE, SCREEN)
        self.SCREEN = SCREEN
        self.MOV_SPEED = 15
        self.rect.x = self.rect.y = 20

PlayerCount = 10
def Game():
    clock = pygame.time.Clock()
    hiders = []
    seekers = []
    for Player in range(PlayerCount):
        hiders.append(Hider())
        seekers.append(Seeker())

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        SCREEN.fill((255, 255, 255))

        for hider in hiders:
            hider.draw() 
        for seeker in seekers:
            seeker.draw()
            
        # player movement
        user_input = pygame.key.get_pressed()
        for i in range(len(hiders)):
            #Hider Movement
            if user_input[pygame.K_DOWN]:
                hiders[i].move(0, 1)
            if user_input[pygame.K_UP]:
                hiders[i].move(0, -1)
            if user_input[pygame.K_RIGHT]:
                hiders[i].move(1, 0)
            if user_input[pygame.K_LEFT]:
                hiders[i].move(-1, 0)
            #Seeker Movement
            if user_input[pygame.K_s]:
                seekers[i].move(0, 1)
            if user_input[pygame.K_w]:
                seekers[i].move(0, -1)
            if user_input[pygame.K_d]:
                seekers[i].move(1, 0)
            if user_input[pygame.K_a]:
                seekers[i].move(-1, 0)

            #Collision
            if pygame.Rect.colliderect(hiders[i].rect, seekers[i].rect):
                hiders[i].colour = (255, 0, 0)
                print(f"Hider {i}, is out!")
        clock.tick(30)
        pygame.display.update()
        SCREEN.fill((255, 255, 255))

Game()
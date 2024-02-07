import pygame
import sys
import os
import random
import neat
import math
from Levels import level

""" initialize pygame """
pygame.init()


""" Constants """
SCREEN_HEIGHT = 640
SCREEN_WIDTH = 1792
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

PLAYER_SIZE = 30 #Size in pixels

FONT = pygame.font.Font('Noto.ttf', 20)

#Walls

""" Walls """
walls = [] # store list of walls

class Wall(object): # Creates a wall object
        def __init__(self, position, width):
            self.rect = pygame.Rect(position[0], position[1], width, width)  # places a square of width (width) at position (x, y), 


""" Level """

# Imports level from different script because it ruins the code
maze = level.Levels[1]



wall_size = 64 # Size of each wall + gap between each wall

# Magic wall generation code
x = y = 0
for row in maze:
    x = 0
    for col in row:
        if col == 1:
            walls.append(Wall([x, y], wall_size))
        x+=wall_size
    y+=wall_size

""" Player / Hiders / Seekers """

class player:
    MOV_SPEED = 10
    colour = (0, 0, 0)
    ID = 0
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
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom
    def draw(self):
        pygame.draw.rect(self.SCREEN, self.colour, self.rect)
        text = FONT.render(f'{self.ID}', True, (255, 255, 255))
        SCREEN.blit(text, (self.rect.center[0]-self.rect.width//2, self.rect.center[1]-self.rect.height//2))



# Hider
class Hider(player):
    def __init__(self, ID, color = (0, 0, 0)):
        super().__init__(PLAYER_SIZE, SCREEN)
        # Stuff
        self.colour = color
        self.ID = ID
        self.MOV_SPEED = 10
        self.rect.x = 1200
        self.rect.y = 100
        
#Seeker
class Seeker(player):
    def __init__(self, ID, color = (0, 0, 0)):
        super().__init__(PLAYER_SIZE, SCREEN)
        self.colour = color
        self.ID = ID
        self.MOV_SPEED = 15
        self.rect.x = self.rect.y = 64


# Removes game at index i
def remove(index):
    hiders.pop(index)
    seekers.pop(index)
    ge.pop(index)
    nets.pop(index)


# Input Funcs
def Angle(A, B):
    return math.atan2(B[1]-A[1], B[0]-A[0]) * (180/math.pi)

def Distance(A, B):
    return math.sqrt(abs((A[0]**2 - B[0]**2)+(A[1]**2 - B[1]**2)))

# Evaluate the genomes
def eval_genomes(genomes, config):
    global hiders, seekers, ge, nets
    
    clock = pygame.time.Clock()

    seekers = []
    ge = []
    nets = []

    hiders = []




    
    n = 0
    first_run = True
    for genome_id, genome in genomes:
        colour = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
        n+=1
        if first_run:
            seekers.append(Seeker(n, colour))
            if n > len(genomes)//2 - 1:
                n = 0
                first_run = False
        else:
            hiders.append(Hider(n, colour))
        
        
        
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)

        genome.fitness = 0


    
    play_time = 5
    time = pygame.time.get_ticks()


    
    run = True
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
        SCREEN.fill((255, 255, 255))



        

        user_input = pygame.key.get_pressed()
        for i, hider in enumerate(hiders):
            output = nets[i].activate([Angle(seekers[i].rect.center, hiders[i].rect.center), Distance(seekers[i].rect.center, hiders[i].rect.center), hider.rect.center[0], hider.rect.center[1], 0]) # Hider AGENT
            
            if output[0] > 0.5:
                hider.move(0, 1)
                
            if output[1] > 0.5:
                hider.move(0, -1)
                
            if output[2] > 0.5:
                hider.move(1, 0)
                
            if output[3] > 0.5:
                hider.move(-1, 0)


            
            # Collision
            if pygame.Rect.colliderect(hiders[i].rect, seekers[i].rect) and (hiders[i].ID == seekers[i].ID):
                ge[i].fitness += 2
                ge[i+len(genomes)//2].fitness -= 2
                remove(i)



        
        for i, seeker in enumerate(seekers):
            output = nets[i].activate([Angle(seekers[i].rect.center, hiders[i].rect.center), Distance(seekers[i].rect.center, hiders[i].rect.center), seeker.rect.center[0], seeker.rect.center[1], 0])   
            
            if output[0] > 0.5:
                seeker.move(0, 1)
                
            if output[1] > 0.5:
                seeker.move(0, -1)
                
            if output[2] > 0.5:
                seeker.move(1, 0)
                
            if output[3] > 0.5:
                seeker.move(-1, 0)
                

        
        if pygame.time.get_ticks()-time > play_time*1000:
            for i, seeker in enumerate(seekers):
                ge[i].fitness-=1
                ge[i+len(genomes)//2].fitness += 1
                remove(i)

        for wall in walls:
            pygame.draw.rect(SCREEN, (0, 0, 0), wall.rect)

        
        for hider in hiders:
            hider.draw() 

        
        for seeker in seekers:
            seeker.draw()

        
        if len(seekers) == 0:
            break
        
        clock.tick(30)

        pygame.display.update()
        SCREEN.fill((255, 255, 255))

def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    Pop = neat.Population(config)


    Pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    Pop.add_reporter(stats)



    winner = Pop.run(eval_genomes, 100)

    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

        
if __name__ == '__main__':
    config_path = os.path.join("C:/Users/Flame32/Desktop/PyProj/Hide-And-Seek", 'config.txt')
    run(config_path)
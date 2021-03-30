import pygame
import math
import random

# planing to make a function to detect if 2 planets collide and merge then into 1 with the sum of masses

gravityConstant = (6 * 10 ** -9)
class CelestialBody():
    def __init__(self, position, mass, color):
        self.pos = position
        self.mass = mass
        self.size = math.sqrt(mass/1000)
        self.color = color
        self.speed = [0, 0]
        self.lastpositions = []
        self.tickcount = 0
        self.trail = []
        self.pathlenght = 100

    
    def update(self):
        self.force()
        self.updatePosition()
        self.path()
        self.draw()
    
    def force(self):
        for body in bodies:
            # gets the distance between the center of 2 planets
            distance = math.sqrt(((body.pos[0] - self.pos[0]) ** 2) + (body.pos[1] - self.pos[1]) ** 2)
            if body != self and distance > (body.size + self.size):
                # gravity force
                acc = (gravityConstant * self.mass * body.mass) / (distance * distance)
                # direction(normalized) to the planet
                direction = [(body.pos[0] - self.pos[0])/distance, (body.pos[1] - self.pos[1])/distance]
                velocity = [ direction[0]*acc, direction[1]*acc ]
                self.speed[0] += velocity[0]
                self.speed[1] += velocity[1]
            elif body != self:
                # if 2 planets collide they stop right next to each other
                self.speed = [0, 0]
                body.speed = [0, 0]

    def updatePosition(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.pos), self.size)
    
    def path(self):
        fadedcolor = (self.color[0]/3, self.color[1]/3, self.color[2]/3)
        self.trail.append(tuple(self.pos))
        for place in self.trail:
            pygame.draw.circle(screen, fadedcolor, place, self.size)
        if len(self.trail) > self.pathlenght:
            self.trail.pop(0)
        # visualize the trail or path the body leaves behind

    def stopped(self):
        # holds the last 10 positions of the planet, add 1 position after 2 frames and 
        # remove the last one after the lenght goes past 10
        self.tickcount = (self.tickcount + 1) % 1   # 1 a cada 2 ticks
        if self.tickcount == 0:    
            self.lastpositions.append((int(float(str(self.pos[0])[:3])), int(float(str(self.pos[1])[:3]))))
            if len(self.lastpositions) > 10:
                self.lastpositions.pop(0)

        # if half of the positons are equal to the last it declares the planet "stopped" or return True
        # else it declares it not "stopped"
        count = 0
        for i in range(int(len(self.lastpositions)/2)):
            if self.lastpositions[-1] != self.lastpositions[i]:
                count += 1
        if count == 0:
            return True
        else:
            return False

    
    def drawVector(self):
        # triangle hypotenuse with side of x speed and y speed
        d = math.sqrt(self.speed[0]**2 + self.speed[1]**2)    
        # if hypotenuse diferent than 0 and the body is moving  
        if d != 0 and not self.stopped():          
            # target is the point 15 units in front of the planet, pointing its direction
            target = [self.speed[0]/d*15, self.speed[1]/d*15]
            target = [target[0]+self.pos[0], target[1] + self.pos[1]]
            pygame.draw.line(screen, red, (self.pos), (target), width=2)
        






gameover= False

height = 800
width = 800

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame!")
clock = pygame.time.Clock()


bodies = []
color = white
cb = CelestialBody([width/2, height/2], 100000, color)
bodies.append(cb)

drawVector = False
while not gameover:
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v:           # press "V" to see the direction at which the body is heading
                if not drawVector:
                    drawVector = True
                else:
                    drawVector = False
        if event.type == pygame.MOUSEBUTTONDOWN:  # left clicking with your mouse to spawn a planet
            if event.button == 1:
                mx, my = pygame.mouse.get_pos()
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                cb = CelestialBody([mx, my], 100000, color)
                bodies.append(cb)

    for body in bodies:
        body.update()
        if drawVector:
            body.drawVector()

    pygame.display.update()
    clock.tick_busy_loop(60)

pygame.quit()



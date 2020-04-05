# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 21:48:56 2020

@author: admin
"""

import sys, pygame, random
import numpy as np
from pygame.locals import *

size = width, height = 1000, 800
colour = 221,160,221


maxVelocity = 10
numBoids = 30
boids = []

class Boid:
    def __init__(self, x, y):
        self.position = np.array([x,y])
        self.velocity = np.array([random.randint(1, 10) / 10.0, random.randint(1, 10) / 10.0])
        
        
    def rule1(self,closeBoids): #move closer
        pc = np.array([0,0])
        
        for boid in boids:
            if boid != self:
                pc = pc + boid.position
                
        pc = pc/len(boids)-1
        return (pc-self.position)/4000 #40% towards center
    
    def rule2(self,closeBoids): #move away
        c = np.array([0,0])
        
        for boid in boids:
            if boid != self:
                if all(abs(boid.position - self.position)< 40):
                    #d = abs(boid.position - self.position)
                    #print(d)
                    c = c - (boid.position - self.position)          
        return c
    
    def rule3(self,closeBoids): #match velocity
        pv = np.array([0,0])
        
        for boid in boids:
            if boid != self:
                pv = pv + boid.velocity 
                
        pv = pv/len(boids)-1
        return (pv-self.velocity)/8
      
    def limit_velocity(self):
        vlim = 10
        
        if abs(self.velocity[0]) > vlim:
            self.velocity[0] = (self.velocity[0]/abs(self.velocity[0]))*vlim
            
        if abs(self.velocity[1]) > vlim:
            self.velocity[1] = (self.velocity[1]/abs(self.velocity[1]))*vlim
            
    def bound_position(self):
        Xmin = 50
        Ymin = 50
        Ymax = 800
        Xmax = 800
        v = np.array([0,0])
        
         
        if self.position[0] < Xmin:
            v[0] = 10
        elif self.position[0] > Xmax:
            v[0] = -10
            
        if self.position[1] < Ymin:
            v[1] = 10
        elif self.position[1] > Ymax:
            v[1] = -10
            
        return v
            

def initalize_positions():
    pygame.init()
    screen = pygame.display.set_mode(size)

    ball = pygame.image.load("arrow.png")
    ballrect = ball.get_rect()
    
    # create boids at random positions
    for i in range(numBoids):
        boids.append(Boid(random.randint(0, width), random.randint(0, height))) 
   
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        draw_boids(screen, ball, ballrect)
        move_all_boids_to_new_positions()
      
        


#draws all the boids in their current positions
def draw_boids(screen,ball,ballrect):
    screen.fill(colour)
    for boid in boids:
        boidRect = pygame.Rect(ballrect)
        boidRect.x = boid.position[0]
        boidRect.y = boid.position[1]
        screen.blit(ball, boidRect)
    pygame.display.flip()
    pygame.time.delay(10)
    

def move_all_boids_to_new_positions():
    v1 = np.array([0,0])
    v2 = np.array([0,0])
    v3 = np.array([0,0])
    
    for b in boids:
        v1 = b.rule1(boids)
        v2 = b.rule2(boids)
        v3 = b.rule3(boids)
        
        b.velocity = b.velocity + v1 + v2 + v3
        b.limit_velocity()
        b.position = b.position + b.velocity 
        #vp = b.bound_position()
        #b.position = b.position +vp
        border = 40
        if b.position[0] < border and b.velocity[0] < 0:
            b.velocity[0] = -b.velocity[0] * random.random()
        if b.position[0] > width - border and b.velocity[0] > 0:
            b.velocity[0] = -b.velocity[0] * random.random()
        if b.position[1] < border and b.velocity[1] < 0:
            b.velocity[1] = -b.velocity[1] * random.random()
        if b.position[1] > height - border and b.velocity[1] > 0:
            b.velocity[1] = -b.velocity[1] * random.random()
        
       
def main():
    initalize_positions()
main()

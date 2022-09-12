import numpy as np
import pygame
import operator

class Point:
    def __init__(self, p_c):
        self.p_c = p_c
        self.p = self.p_c
        
        self.p_list = self.p
        
        self.connected_parts = []
        
        self.e = np.matrix([[1,0,0],[0,1,0], [0,0,1]])
        self.dt = 0.01
        
        self.drawing_flag = False
        
    def save(self):
        """Lists for tracking the position, velocity and acceleration"""
        
        self.p_list = np.append(self.p_list, self.p, axis=1)
        
    def export(self):
        np.savetxt('p_list.csv', self.p_list, delimiter=',')

    def visual(self, screen, offset):
        self.screen = screen
        self.scale = 10
        self.offset = offset
        self.color =(0,255,255) # LT_BLUE 
        self.size = 10
        
    def draw(self, i):
        point_loc = (int(self.scale * self.p_list[0,i]), int(self.scale * - self.p_list[1,i]))
        point_loc = tuple(map(operator.add, point_loc, self.offset))
        pygame.draw.circle(self.screen, self.color, point_loc , self.size)
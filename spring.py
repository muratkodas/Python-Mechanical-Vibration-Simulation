import numpy as np
import pygame
import operator
from point import Point
from mass import Mass

class Spring:
    def __init__(self, k, l, s_p_connection):
        self.k = k # spring coeffient
        self.l = l # initial spring lenght
        self.s_p_connection = s_p_connection
        
        self.s_p = self.s_p_func()
        self.p1 = self.s_p[0] # fixed
        self.p2 = self.s_p[1] # free on the part
        
        self.r_initial = self.p2 - self.p1
        
        self.p1_list = self.p1
        self.p2_list = self.p2
        self.force_list = np.matrix([[0], [0], [0]]) #force list
        self.force_total_list = np.matrix([[0]]) #force list
        
        
        self.energy_p_func()
        self.energy_list = self.energy_p
        
        
    def s_p_func(self):
        s_p = [np.matrix([[0], [0], [0]]), np.matrix([[0], [0], [0]])]
        for i in range(2):
            s_p[i] = self.s_p_connection[i].p        
        return s_p
    
    def energy_p_func(self):
        vec_spring = self.p1 - self.p2
        vec_spring_lenght = np.sqrt(np.tensordot(vec_spring, vec_spring))
        self.energy_p = np.matrix([[0.5 * self.k * np.square(np.abs(vec_spring_lenght - self.l))]])
        return self.energy_p
    
    def update(self):
        s_p = self.s_p_func()
        self.p1 = s_p[0]
        self.p2 = s_p[1]
        
        self.r = self.p2 - self.p1 #updated vector of the spring
        self.r_n = np.linalg.norm(self.r) #normalization of r
        self.er = self.r/self.r_n
        
        self.delta = self.r_n - self.l
        
        self.force = self.k * self.delta #self.er , self.er was moved to the mass class for better direction handling

    def pos_update(self, p):
        d = p - self.p_c
        self.p2 = self.p_c + d + self.offset
        
    def save(self):
        self.p1_list = np.append(self.p1_list, self.p1, axis=1)
        self.p2_list = np.append(self.p2_list, self.p2, axis=1)
        self.energy_list = np.append(self.energy_list, self.energy_p, axis=1)
        self.force_list = np.append(self.force_list, self.force * self.er, axis=1)
        self.force_total_list = np.append(self.force_total_list, np.matrix([[self.force]]), axis=1)
        
    def visual(self, screen, offset):
        self.screen = screen
        self.scale = 10
        self.offset = offset
        self.color = (0,0,255)# Blue
        self.size = 5
        
    def draw(self, i):
        point_loc1 = (int(self.scale * self.p1_list[0,i]), int(self.scale * - self.p1_list[1,i]))
        point_loc1 = tuple(map(operator.add, point_loc1, self.offset))
        
        point_loc2 = (int(self.scale * self.p2_list[0,i]), int(self.scale * - self.p2_list[1,i]))
        point_loc2 = tuple(map(operator.add, point_loc2, self.offset))

        pygame.draw.line(self.screen, self.color, point_loc1 , point_loc2, width = 1)
        
        
    def comment(self):
        print(f"self.p:\n{self.p}")
        #print(f"self.p1:\n{self.p1}")
        #print(f"self.p2:\n{self.p2}")
        print(f"self.r:\n{self.r}")
        print(f"self.r_n:\n{self.r_n}")
        print(f"self.er:\n{self.er}")
        print(f"self.delta:\n{self.delta}")
        print(f"self.force:\n{self.force}")
        print("\n\n")

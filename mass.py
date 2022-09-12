#multiple masses, exporting the saves
import numpy as np
import pygame
import operator

class Mass:
    def __init__(self,m, p_c):
        self.m = m
        self.p_c = p_c
        
        self.connected_parts = []
        
        self.e = np.matrix([[1,0,0],[0,1,0], [0,0,1]])
        self.dt = 0.01
        
        self.p = self.p_c #np.matrix([[0], [0], [0]]) #position
        self.vel = np.matrix([[0], [0], [0]]) #velocity
        self.acc = np.matrix([[0], [0], [0]]) #acceleration
        
        self.ke = 0.5 * self.m * np.tensordot(self.vel, self.vel)
        self.pe = 0
        self.te = self.ke + self.pe
        
        self.p_list = self.p
        self.vel_list = self.vel
        self.acc_list = self.acc

        self.force_cal_first_run = True
        self.drawing_flag = False
    
    def initial(self, g):
        self.y = np.append(self.p, self.vel, axis=0) # matrix for calculation in RG4
        self.g = g #gravity
        
    def energy_update(self):
        self.ke = 0.5 * self.m * np.tensordot(self.vel, self.vel)
        self.pe =  - (self.g.transpose() *self.p).item()
        #print(self.pe)
        return self.ke , self.pe
        
    def force_applied(self):
        if self.force_cal_first_run:
            self.connected_parts_cycle = []
            for part in self.connected_parts:
                #print(f"part.s_p_connection[0]: {part.s_p_connection[0]}")
                #print(f"self: {self}")
                if part.s_p_connection[0] == self:
                    # print("here1")
                    self.connected_parts_cycle.append(True)
                else:
                    # print("here2")
                    self.connected_parts_cycle.append(False)
            self.force_cal_first_run = False
            
            
                    
        force = np.matrix([[0], [0], [0]])
        i = 0
        for part in self.connected_parts:
            if self.connected_parts_cycle[i]: 
                p1 = part.s_p_connection[0].p
                p2 = part.s_p_connection[1].p
            else: 
                p2 = part.s_p_connection[0].p
                p1 = part.s_p_connection[1].p
                
            r = p2 - p1 #updated vector of the spring
            r_n = np.linalg.norm(r) #normalization of r
            er = r/r_n
            
            force = force +  part.force * er 
            i = i+1
        
        x_dd = ( np.dot(self.e,force) / self.m ) #+ self.g
        y_dot = np.append(self.vel, x_dd, axis=0)
        
        return y_dot
    
    
        
    def save(self):
        """Lists for tracking the position, velocity and acceleration"""
        
        self.p_list = np.append(self.p_list, self.p, axis=1)
        self.vel_list = np.append(self.vel_list, self.vel, axis=1)
        self.acc_list = np.append(self.acc_list, self.acc, axis=1)
        
    def export(self):
        np.savetxt('p_list.csv', self.p_list, delimiter=',')
        
    

    def update(self, p, vel, acc, y):
        self.p, self.vel, self.acc, self.y = p, vel, acc, y
        
    def visual(self, screen, offset):
        self.screen = screen
        self.scale = 10
        self.offset = offset
        self.color = (255,0,0)# RED
        self.size = 10
        
    def draw(self, i):
        point_loc = (int(self.scale * self.p_list[0,i]), int(self.scale * - self.p_list[1,i]))
        point_loc = tuple(map(operator.add, point_loc, self.offset))
        pygame.draw.circle(self.screen, self.color, point_loc , self.size)
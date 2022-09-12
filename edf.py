import numpy as np

from point import Point
from mass import Mass
from spring import Spring 

"""Class to manage test conditions"""
class Element_Defination:
    def __init__(self):
        None
    

    def define(self, name):
        if name == "SDOF_Test":
            self.SDOF_Test() 
        elif name == "DDOF_Test":
            self.DDOF_Test() 
        elif name == "CS1_Test":
            self.CS1_Test() 

        return self.points, self.nof_points, self.masses, self.nof_mass, self.springs, self.nof_springs
        
        
    def SDOF_Test(self):
        #p1:fixed p2:moveable
        point1 = Point(np.matrix([[0], [10], [0]]))
        
        self.points = [point1]
        self.nof_points = np.shape(self.points)[0]

        #matrix shape info: 1st: row 2nd:column
        m = 1
        p_c1 = np.matrix([[0], [0], [0]])
        m1 = Mass(m,p_c1)
        
        
        self.masses = [m1]
        self.nof_mass = np.shape(self.masses)[0]

        k = 4
        l = 10 # initial spring lenght
        
        s1_p_connection = [self.points[0], self.masses[0]]
        s1 = Spring(k, l, s1_p_connection)
        self.masses[0].connected_parts.append(s1)
        
        self.springs = [s1] #, s2, s3, s4
        self.nof_springs = np.shape(self.springs)[0]
        
        
    def DDOF_Test(self):
        #p1:fixed p2:moveable
        point1 = Point(np.matrix([[0], [10], [0]]))
        
        self.points = [point1]
        self.nof_points = np.shape(self.points)[0]

        #matrix shape info: 1st: row 2nd:column
        m = 1
        p_c1 = np.matrix([[0], [0], [0]])
        m1 = Mass(m,p_c1)
        p_c2 = np.matrix([[0], [-10], [0]])
        m2 = Mass(m,p_c2)
        
        self.masses = [m1, m2]
        self.nof_mass = np.shape(self.masses)[0]

        k = 4
        l = 10 # initial spring lenght
        
        s1_p_connection = [self.points[0], self.masses[0]]
        s1 = Spring(k, l, s1_p_connection)
        self.masses[0].connected_parts.append(s1)
        
        
        s2_p_connection = [self.masses[0], self.masses[1]]
        s2 = Spring(k, l, s2_p_connection)
        self.masses[0].connected_parts.append(s2)
        self.masses[1].connected_parts.append(s2)
        
        self.springs = [s1, s2]
        self.nof_springs = np.shape(self.springs)[0]       
        
    def CS1_Test(self):
        #p1:fixed p2:moveable
        point1 = Point(np.matrix([[6], [8], [0]]))
        point2 = Point(np.matrix([[-6], [8], [0]]))
        point3 = Point(np.matrix([[10], [-10], [0]]))
        
        self.points = [point1, point2, point3]
        self.nof_points = np.shape(self.points)[0]

        #matrix shape info: 1st: row 2nd:column
        m = 1
        p_c1 = np.matrix([[0], [0], [0]])
        m1 = Mass(m,p_c1)
        p_c2 = np.matrix([[0], [-10], [0]])
        m2 = Mass(m,p_c2)
        
        self.masses = [m1, m2]
        self.nof_mass = np.shape(self.masses)[0]

        k = 4
        l = 10 # initial spring lenght
        
        s1_p_connection = [self.points[0], self.masses[0]]
        s1 = Spring(k, l, s1_p_connection)
        self.masses[0].connected_parts.append(s1)
        
        s2_p_connection = [self.points[1], self.masses[0]]
        s2 = Spring(k, l, s2_p_connection)
        self.masses[0].connected_parts.append(s2)
        
        s3_p_connection = [self.masses[0], self.masses[1]]
        s3 = Spring(k, l, s3_p_connection)
        self.masses[0].connected_parts.append(s3)
        self.masses[1].connected_parts.append(s3)
        
        s4_p_connection = [self.masses[1], self.points[2]]
        s4 = Spring(k, l, s4_p_connection)
        self.masses[1].connected_parts.append(s4)
        
        self.springs = [s1, s2, s3, s4]
        self.nof_springs = np.shape(self.springs)[0]
        
    def definitions(self):
        self.point_defination()
        self.mass_defination()
        self.spring_defination()
        
        
        
    def point_defination(self):
        #p1:fixed p2:moveable
        point1 = Point(np.matrix([[6], [8], [0]]))
        point2 = Point(np.matrix([[-6], [8], [0]]))
        point3 = Point(np.matrix([[10], [-10], [0]]))
        
        self.points = [point1, point2, point3]
        self.nof_points = np.shape(self.points)[0]
        
        
    def mass_defination(self):
        #matrix shape info: 1st: row 2nd:column
        m = 1
        p_c1 = np.matrix([[0], [0], [0]])
        m1 = Mass(m,p_c1)
        p_c2 = np.matrix([[0], [-10], [0]])
        m2 = Mass(m,p_c2)
        
        self.masses = [m1] #, m2
        self.nof_mass = np.shape(self.masses)[0]
        
    def spring_defination(self):
        k = 4
        l = 10 # initial spring lenght
        
        s1_p_connection = [self.points[0], self.masses[0]]
        s1 = Spring(k, l, s1_p_connection)
        self.masses[0].connected_parts.append(s1)
        
        # s2_p_connection = [self.points[1], self.masses[0]]
        # s2 = Spring(k, l, s2_p_connection)
        # self.masses[0].connected_parts.append(s2)
        
        # s3_p_connection = [self.masses[0], self.masses[1]]
        # s3 = Spring(k, l, s3_p_connection)
        # self.masses[0].connected_parts.append(s3)
        # self.masses[1].connected_parts.append(s3)
        
        # s4_p_connection = [self.masses[1], self.points[2]]
        # s4 = Spring(k, l, s4_p_connection)
        # self.masses[1].connected_parts.append(s4)
        
        self.springs = [s1] #, s2, s3, s4
        self.nof_springs = np.shape(self.springs)[0]
     
        
        
import numpy as np
import matplotlib.pyplot as plt

from edf import Element_Defination

"""Class to manage calculation of the vibration simulation"""
class Vibration_Calculation:
    def __init__(self):
        self.e = np.matrix([[1,0,0],[0,1,0], [0,0,1]])
        self.dt = 0.01
        self.time = [0]
        
        self.edf_flag = "CS1_Test"
        
        if self.edf_flag:
            edf = Element_Defination()
            self.points, self.nof_points, self.masses, self.nof_mass, self.springs, self.nof_springs = edf.define(self.edf_flag)
        else:
            pass
        self.simulation_condition()
        self.energy_initialization()
        self.control = False
        
        self.simulation_size = 0
        
    def simulation_condition(self):
        self.g = np.matrix([[0], [0], [0]]) #m/s2 #
        self.e_g = self.g / np.abs( self.g )
        self.e_g = np.nan_to_num(self.e_g, False, 0, None, None) # g direction(unit vector)
        
        self.masses[0].p = np.matrix([[-1], [-1], [0]]) #position
        
        for mass in self.masses:
            mass.initial(self.g)
        
    def energy_initialization(self):
        self.ke, self.pe, self.te_initial = self.energy_calculation()
        #print(f'Initial Total Energy: {self.te_initial}')
        self.ke_list, self.pe_list, self.te_list = self.ke, self.pe, self.te_initial
        
    def energy_calculation(self):
        mass_ke, mass_pe = self.masses_energy_func()
        springs_pe = self.springs_energy_p_func()
        ke = np.matrix([[mass_ke]])
        pe = np.matrix([[mass_pe + springs_pe]])
        te = ke + pe
    
        return ke, pe, te
        
    def masses_energy_func(self):
        masses_ke, masses_pe = 0 , 0
        for mass in self.masses:
            mass_ke, mass_pe = mass.energy_update()
            masses_ke, masses_pe = masses_ke + mass_ke, masses_pe + mass_pe
        return masses_ke, masses_pe
    
    def springs_energy_p_func(self):
        springs_energy_p = 0
        for s in self.springs: 
            springs_energy_p = springs_energy_p + s.energy_p_func()[0,0]
        return springs_energy_p
    
    
    def main_sim_loop(self):
        self.time = np.arange(0.0,10.001,self.dt)
        
        for t in self.time:
            rf4_output = self.RK4_step(t)
            
            for i in range(0, self.nof_mass, 1):
                self.masses[i].acc = self.masses[i].y[3:,0]
                self.masses[i].y = self.masses[i].y + self.dt * rf4_output[i]
                self.masses[i].p = self.masses[i].y[0:3,0] # just for saving
                self.masses[i].vel = self.masses[i].y[3:,0] # just for saving
            
            self.save_process()
                
        self.time = np.insert(self.time, 0, 0, axis=0)
        self.time = self.time.reshape((np.shape(self.time)[0],1))
        self.simulation_size = np.shape(self.time)[0]
            
    def RK4_step(self, t):
        dt = self.dt
        
        
        k1_yi = []
        for i in range(0, self.nof_mass, 1):
            k1_yi.append(self.masses[i].y)

        # print(f"k1_yi: {k1_yi}\n")
        k1 = self.G(k1_yi, t)
        
        # print(f"k1: {k1}\n")
        
        k2_yi = []
        for i in range(0, self.nof_mass, 1):
            k2_yi.append(self.masses[i].y + 0.5*k1[i]*dt)
             
        k2 = self.G(k2_yi, t +0.5*dt)
        
        #print(f"k2: {k2}\n")
        
        k3_yi = []
        for i in range(0, self.nof_mass, 1):
            k3_yi.append(self.masses[i].y + 0.5*k2[i]*dt)
             
        k3 = self.G(k3_yi, t +0.5*dt)
        
        #print(f"k3: {k3}\n")
        
        
        k4_yi = []
        for i in range(0, self.nof_mass, 1):
            k4_yi.append(self.masses[i].y + k3[i]*dt)
             
        k4 = self.G(k4_yi, t +dt)
        
        #print(f"k4: {k4}\n")
        
        y_dot = []
        for i in range(0, self.nof_mass, 1):
            y_dot.append((k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) / 6)
        
        #print(f"y_dot: {y_dot}\n")
        return y_dot
        
    def G(self, y, t):
        for i in range(0, self.nof_mass, 1):
            self.masses[i].p = y[i][0:3, 0]
            self.masses[i].vel = y[i][3:, 0]
            # print(f"y[i]: {y[i]}\n")
            # print(f"self.masses[i].p: {self.masses[i].p}\n")
            # print(f"self.masses[i].vel: {self.masses[i].vel}\n")
            
        #pos update
        self.force_updates()
         
        y_dot = []
         
        for mass in self.masses:
            y_dot.append(mass.force_applied())
        
        return y_dot
    
    def force_updates(self):        
        for s in self.springs:
            s.update()


    def save_process(self):
        
        self.ke, self.pe, self.te = self.energy_calculation()
               
        self.ke_list = np.append(self.ke_list, self.ke, axis=1)
        self.pe_list = np.append(self.pe_list, self.pe, axis=1)
        self.te_list = np.append(self.te_list, self.te, axis=1)
        
        for m in self.masses:
            m.save()
        for point in self.points:
            point.save()
        for s in self.springs:
            s.save()
        # for d in self.dampers:
        #     d.save()       

        
    def export_saves(self):
        
        # for m in self.masses:
        #     m.export()
        # for s in self.springs:
        #     s.save()
        # for d in self.dampers:
        #     d.save()
        pass
        
    def plotting(self):
        plt.plot(self.time, self.te_list[0,:].transpose(), label = 'total energy')
        # plt.plot(self.time, self.ke_list[0,:].transpose(), label = 'kinetic energy')
        # plt.plot(self.time, self.pe_list[0,:].transpose(), label = 'potential energy')
        # plt.plot(self.time, self.springs[0].force_list[0,:].transpose(), label = 'spring_force_x')
        
        # i = 0
        # for s in self.springs:
        #     plt.plot(self.time, s.force_list[0,:].transpose(), label = f'force{i}_x')
        #     i = i +1
        
        
        # i = 0
        # for s in self.springs:
        #     plt.plot(self.time, s.force_list[1,:].transpose(), label = f'force{i}_y')
        #     i = i +1
            
        # i = 0
        # for s in self.springs:
        #     plt.plot(self.time, s.force_total_list[0,:].transpose(), label = f'force_total{i}')
        #     i = i +1
           
        # i = 0
        # for m in self.masses:
        #     plt.plot(self.time, m.p_list[0,:].transpose(), label = f'p{i}_x')
        #     i = i +1
           
        i = 0
        for m in self.masses:
            plt.plot(self.time, m.p_list[1,:].transpose(), label = f'p{i}_y')
            i = i +1
        
        # i = 0
        # for s in self.springs:
        #     plt.plot(self.time, s.energy_list[0,:].transpose(), label = f's{i}_energy')
        #     i = i +1

        #plt.plot(self.time, self.springs[3].force_list[1,:].transpose(), label = 'spring3_force_y')
        # plt.plot(self.time, self.dampers[0].force_list[0,:].transpose(), label = 'damper_force_x')
        # plt.plot(self.time, self.dampers[0].force_list[1,:].transpose(), label = 'damper_force_y')
        #plt.plot(self.time, self.masses[0].p_list[0,:].transpose(), label = 'p_list_x')
        #plt.plot(self.time, self.masses[0].p_list[1,:].transpose(), label = 'p1_list_y')
        #plt.plot(self.time, self.masses[1].p_list[2,:].transpose(), label = 'p2_list_y')
        #plt.plot(self.time, self.masses[0].vel_list[0,:].transpose(), label = 'vel_list_x')
        # plt.plot(self.time, self.masses[0].vel_list[1,:].transpose(), label = 'vel1_list_y')
        #plt.plot(self.time, self.masses[1].vel_list[1,:].transpose(), label = 'vel2_list_y')
        plt.legend()#loc = 'lower right'
        plt.ylabel('output')
        plt.xlabel('time')
        plt.show()
        
if __name__ == '__main__':
    calculation = Vibration_Calculation()
    calculation.control = False
    calculation_flag = True
    show = True
    if calculation_flag:
        calculation.main_sim_loop()
    if show:
        calculation.plotting()
    print("FINISHED")
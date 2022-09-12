from vib_cal import Vibration_Calculation 
from pygame_simulation import Game


WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (240,240,0)
LT_BLUE = (230,230,255)

if __name__ == '__main__':
    calculation = Vibration_Calculation()
    calculation_flag = True
    if calculation_flag:
        calculation.main_sim_loop()
        print("Calculation was completed")
    #calculation.export_saves()
    
    calculation.control = False
    show_plotting = False
    show_simulation = True
    
    if show_plotting:
        calculation.plotting()
    
    
    if show_simulation :
        print("SIMULATION IS STARTING")
        simulation_size = calculation.simulation_size
        particles = calculation.masses
        particles.extend(calculation.points)
        particles.extend(calculation.springs)
        # particles.extend(calculation.dampers)
        #print(particles)
        
        game = Game()
        #game.define_simulation(points, springs)
        game.run_game(simulation_size, particles)
        
    print("FINISHED")
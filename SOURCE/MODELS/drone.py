import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import numpy as np
from functools import partial
from ..CONTROLLER.lin_ctrl import *
from ..DATA.pygame_assets import *


#######################################################################################################
#######################################################################################################


class drone():
    def __init__(self, drone_mass, drone_length, g_acc, beta):
        # Terms are self explanatory & beta is damping factor
        self.b = beta
        self.num_inputs = 2
        self.num_states = 6
        self.M = drone_mass
        self.d = drone_length

        self.dt = 0.01
        self.load(reset=1)
        self.acc_0 = np.array([0., g_acc, 0.])

        # Stabilising Force needed to counter Gravity at equilibrium
        self.F_stable = np.ones(self.num_inputs)*drone_mass*g_acc/2.


    def load(self, goal=np.zeros(2), reset=2):
        '''
        6 states:
        x: x position of drone,
        y: y position of drone,
        phi: Angle of drone,
        v_x: Linear velocity along x of drone,
        v_y: Linear velocity along y of drone,
        omega_phi: Angular Velocity of drone
        
        curr_state is th current state
        steady_state is the desired state
        reset = 1 resets curr_state and steady_state and assigns goal
        reset = 2 just assigns the goal
        '''
        if reset == 1:
            self.curr_state = np.zeros(self.num_states)
            self.steady_state = np.zeros(self.num_states)
        if reset >= 1:
            self.steady_state[:2] = goal


    def step_sim(self, F):
        '''
        Calculate new State values from given Force (F)
        F is the feedback force which needs to be added to
        the stabilizing force F_stable to reach equilibrium
        The force has two componenents for left & right wing
        '''
        sine = np.sin(self.curr_state[2])
        cosine = np.cos(self.curr_state[2])

        # F is the feedback force
        # Feedback forces are added to it for reaching equilibrium
        accelerations = ((F + self.F_stable)/self.M
                         @ np.array([[-sine, -cosine, -4/self.d], 
                                     [-sine, -cosine, 4/self.d]])
                         - self.curr_state[-self.num_states//2:]*self.b
                         + self.acc_0)
        
        # Euler's method... :)
        del_vel = accelerations*self.dt        
        self.curr_state[:self.num_states//2] += (self.curr_state[-self.num_states//2:] + del_vel/2.)*self.dt
        self.curr_state[-self.num_states//2:] += del_vel
        
        # Confine abs value of angle within 0 to 2pi
        if abs(self.curr_state[2]) > 2*np.pi:
            self.curr_state[2] -= np.copysign(2*np.pi, self.curr_state[2])
        
        return accelerations
    

#######################################################################################################
#######################################################################################################


class pygame_drone(drone):
    # For Pygame Simulation with visualisation
    def __init__(self, screen, **drone_params):
        super().__init__(**drone_params)
        
        # Passing the main 
        # pygame screen to draw on
        self.screen = screen
        self.get_drone_screen()


    def get_drone_screen(self):
        # Draw the drone once only
        drone_body_radius = self.d/4
        drone_half_length = self.d/2
        drone_blade_radius = self.d/3
        drone_blade_height = self.d/10
        
        drone_base = np.array([drone_half_length + drone_blade_radius, 
                               drone_blade_height*2 + drone_body_radius])

        wing_pos = lambda l_r_sign, u_d_sign : drone_base - np.array([l_r_sign*drone_half_length,
                                                                      u_d_sign*drone_body_radius])
        
        blade_span = lambda wing_base, l_r_sign : wing_base - np.array([l_r_sign*drone_blade_radius,
                                                                        drone_blade_height])

        self.drone_screen = pygame.Surface(drone_base*2)
        self.drone_screen.fill(grey)
        pygame.draw.line(self.drone_screen, yellow, wing_pos(-1, 0), wing_pos(1, 0), int(drone_blade_height))
        pygame.draw.circle(self.drone_screen, purple, drone_base, drone_body_radius)
        pygame.draw.circle(self.drone_screen, yellow, drone_base, drone_body_radius, int(drone_blade_height/2))
        
        l_r_sign = -1
        for _ in range(2):
            l_r_sign *= -1
            curr_wing = wing_pos(l_r_sign, 1)
            pygame.draw.polygon(self.drone_screen, red, 
                                [blade_span(curr_wing, 1), 
                                 blade_span(curr_wing, -1), 
                                 curr_wing])

            blade_base_rect = pygame.Rect((blade_span(curr_wing, drone_blade_height/drone_blade_radius), 
                                           (2*drone_blade_height, 1.5*drone_blade_radius)))
            
            pygame.draw.ellipse(self.drone_screen, green, blade_base_rect)



    def draw_game(self):
        # Draw the entire game screen here
        self.screen.fill(grey)
        drone_base = self.curr_state[0:2]
        
        # Reusing the drone screen again and again
        curr_drone_screen = pygame.transform.rotate(self.drone_screen, np.degrees(self.curr_state[2]))
        curr_drone_rect = curr_drone_screen.get_rect(); curr_drone_rect.center = drone_base
        self.screen.blit(curr_drone_screen, curr_drone_rect)
        pygame.draw.circle(self.screen, white, self.steady_state[:2], self.d//20, 2)


#######################################################################################################
#######################################################################################################


class simulate_drone(drone):
    # Simulating without visualisation
    def __init__(self, goal, max_steps, max_fitness=2000., **sys_params):
        super().__init__(**sys_params)

        A, B = get_sys_matrix(self)
        self.get_K = partial(get_K_matrix, A, B)
        self.max_fitness = max_fitness
        self.max_steps = max_steps
        self.goal = goal


    def get_Q_R(self, chrom):
        '''
        Obtaining Q and R from the chromsomes

        For obtaining Q:
        x, y both penalised by chromosome[0]
        drone angle penalised by chromosome[1]
        linear velocities along x, y both penalised by chromosome[2]
        angular velocity of drone penalised by chromosome[3]
        
        For obtaining R:
        R is the last element chrom[4]

        '''
        R = np.ones(self.num_inputs)*chrom[4]
        Q = np.concatenate((np.ones(2)*chrom[0],
                           [chrom[1]],
                           np.ones(2)*chrom[2],
                           [chrom[3]]))
        return Q, R


    def run(self, chrom, chrom_index):
        '''
        Running simulation with current value of K
        Returns the index of the chromosome used to get Q and R
        and the Fitness of the current bot
        '''
        iter = 0
        avg_dist = 0
        running = True
        self.load(goal=self.goal, reset=1)
        Q, R = self.get_Q_R(chrom)
        K = self.get_K(Q, R)

        while running:
            Force, err = get_force(K, self)
            self.step_sim(Force)

            curr_dist_goal = np.sqrt(np.linalg.norm(err[:2]))
            if curr_dist_goal < 1. or iter > self.max_steps:
                running = False
            
            avg_dist += curr_dist_goal*self.dt
            iter += 1
            
        tot_time = iter*self.dt
        return self.max_fitness - tot_time - avg_dist/tot_time, chrom_index


#######################################################################################################
#######################################################################################################

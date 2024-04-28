import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import numpy as np
from functools import partial
from ..CONTROLLER.lin_ctrl import *
from ..DATA.pygame_assets import *


#######################################################################################################
#######################################################################################################


class cart_pole():
    def __init__(self, pend_length, pend_mass, cart_mass, g_acc):
        # Terms are self explanatory
        self.l = pend_length
        self.m = pend_mass
        self.M = cart_mass
        self.g = g_acc # acceleration due to gravity
        
        self.dt = 0.01
        self.num_states = 4
        self.num_inputs = 1
        self.load(reset=1)

    
    def load(self, goal=np.zeros(2), reset=2):
        '''
        4 states:
        x: x position of cart,
        theta: Angle of pendulum,
        v: Linear velocity along x of cart,
        omega: Angular Velocity of pendulum
        
        curr_state is th current state
        steady_state is the desired state
        reset = 1 resets curr_state and steady_state and assigns goal
        reset = 2 just assigns the goal
        '''
        if reset == 1:
            self.curr_state = np.zeros(self.num_states)
            self.steady_state = np.zeros(self.num_states)
        if reset >= 1:
            # Goal is by default 2D, but we only need x component
            self.steady_state[0] = goal[0]
    

    def step_sim(self, F):
        '''
        Calculate new State values from given Force (F)
        F is the feedback force with 1 componenent
        '''
        sine = np.sin(self.curr_state[1]); cosine = np.cos(self.curr_state[1])
        A = np.array([[self.M+self.m, -self.m*self.l*cosine], [-cosine, self.l]])
        B = np.array([[F - self.m*np.square(self.curr_state[3])*self.l*sine], [self.g*sine]])
        accelerations = np.squeeze(np.linalg.inv(A) @ B)

        # Euler's method... :)
        del_vel = accelerations*self.dt
        self.curr_state[:self.num_states//2] += self.curr_state[self.num_states//2:]*self.dt + 0.5*del_vel*self.dt
        self.curr_state[self.num_states//2:] += del_vel

        # Confine abs value of angle within 0 to 2pi
        if abs(self.curr_state[1]) > 2*np.pi:
            self.curr_state[1] -= np.copysign(2*np.pi, self.curr_state[1])
        
        return accelerations


#######################################################################################################
#######################################################################################################


class pygame_cart_pole(cart_pole):
    # For Pygame Simulation with visualisation
    def __init__(self, screen, **cart_pole_params):
        pygame.init()
        pygame.display.set_caption("CART POLE!")
        super().__init__(**cart_pole_params)
        
        # Passing the main 
        # pygame screen to draw on
        self.screen = screen
        self.get_cart_screen()
    

    def get_cart_screen(self):
        # Draw the car pole once only
        x_screen, y_screen = self.screen.get_size()
        cart_height = y_screen/10
        wheel_radius = cart_height/3
        cart_half_width = x_screen/20
        self.pend_radius = y_screen//50
        screen_height = cart_height + wheel_radius
        screen_width = 2*(cart_half_width + wheel_radius)
        
        pend_base = np.array([screen_width/2., 0.])
        left_wheel = pend_base + np.array([-cart_half_width, cart_height])
        right_wheel = pend_base + np.array([cart_half_width, cart_height])
        self.pend_base = lambda x: np.array([x, y_screen - screen_height])
        self.cart_pos = lambda curr_pend_base: curr_pend_base - pend_base

        self.cart_screen = pygame.Surface((screen_width, screen_height))
        self.cart_screen.fill(grey)
        pygame.draw.polygon(self.cart_screen, green, [pend_base, left_wheel, right_wheel])
        pygame.draw.circle(self.cart_screen, yellow, left_wheel, wheel_radius)
        pygame.draw.circle(self.cart_screen, yellow, right_wheel, wheel_radius)


    def draw_game(self):
        # Draw the entire game screen here
        self.screen.fill(grey)
        pend_base = self.pend_base(self.curr_state[0])
        
        # Reusing the cart pole screen again and again
        self.screen.blit(self.cart_screen, self.cart_pos(pend_base))
        pygame.draw.circle(self.screen, white, self.pend_base(self.steady_state[0]), self.pend_radius//2, 2)

        # Drawing the pendulum
        pend_pos =  pend_base - np.array([np.sin(self.curr_state[1]), np.cos(self.curr_state[1])])*self.l
        pygame.draw.line(self.screen, white, pend_base, pend_pos, self.pend_radius//4)
        pygame.draw.circle(self.screen, red, pend_pos, self.pend_radius)
        pygame.draw.circle(self.screen, white, pend_base, self.pend_radius//2)
    

#######################################################################################################
#######################################################################################################


class simulate_cart_pole(cart_pole):
    # Simulating without visualisation
    def __init__(self, goal, max_steps, max_fitness=1000., **sys_params):
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
        x is penalised by chromosome[0]
        pendulum angle penalised by chromosome[1]
        linear velocity along x both penalised by chromosome[2]
        angular velocity of pendulum penalised by chromosome[3]
        
        For obtaining R:
        R is the last element chrom[4]

        '''
        R = np.expand_dims(chrom[-1], axis=0)
        Q = chrom[:-1]
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

            curr_dist_goal = abs(err[0])
            if curr_dist_goal < 1. or iter > self.max_steps:
                running = False
            
            avg_dist += curr_dist_goal*self.dt
            iter += 1
            
        tot_time = iter*self.dt
        return self.max_fitness - tot_time - avg_dist/tot_time, chrom_index


#######################################################################################################
#######################################################################################################



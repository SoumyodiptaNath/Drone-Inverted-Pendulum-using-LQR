import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import numpy as np
import matplotlib.pyplot as plt
from .lin_ctrl import get_force
from ..DATA.pygame_assets import *


#######################################################################################################
#######################################################################################################


def plot_states(state_list):
    num_states = len(state_list[0])
    duration = np.arange(len(state_list))
    
    states = np.array(state_list)
    for i in range(num_states):
        plt.plot(duration, states[:,i])
    
    text = str(np.arange(num_states))[1:-1].split(' ')
    plt.legend(text)
    plt.show()


#######################################################################################################
#######################################################################################################


class pygame_sys():
    # PyGame simulation
    def __init__(self, x_screen, y_screen, caption):
        pygame.init()
        pygame.display.set_caption(caption)

        self.running = False
        self.goal = np.zeros(2)
        self.x_screen = x_screen
        self.y_screen = y_screen
        self.text_size = y_screen//20
        self.screen = pygame.display.set_mode((x_screen, y_screen))
    

    def quit(self):
        pygame.quit()


    def place_text(self, text_dict):
        pygame.draw.rect(self.screen, green, text_dict["button"].scale_by(1.25,1.25), 0, 5)
        self.screen.blit(text_dict["text"], text_dict["button"])


    def text_box(self, text, text_pos):
        # Generating a given text at a given coordinate
        font = pygame.font.Font('freesansbold.ttf', self.text_size)
        text = font.render(text, True, red, green)
        text_rect = text.get_rect()
        text_rect.center = text_pos
        return {"button": text_rect, "text": text}
    

    def get_menu(self, sys_list):
        # Generating the openning screen menu
        mid_y_screen = self.y_screen//2
        mid_x_screen = self.x_screen//2
        num_buttons = len(sys_list)
        text_pos_y = np.linspace(mid_y_screen-(num_buttons//2)*self.text_size*1.25,
                                 mid_y_screen+(num_buttons//2)*self.text_size*1.25,
                                 num_buttons)
        self.button_list = []
        for i, system in enumerate(sys_list):
            # Storing the text boxes and buttons
            text_dict = self.text_box(system.name, (mid_x_screen, text_pos_y[i]))
            self.button_list.append(text_dict)


    def button_pressed(self):
        # Checking button pressing action
        running = True
        self.screen.fill(grey)

        for val in self.button_list:
            # Draw buttons once
            self.place_text(val)
            
        while running:
            self.goal *= 0
            self.update_goal_running()
            keys = pygame.key.get_pressed()

            # Press Z to exit the menu
            if keys[pygame.K_z]: return
            for index, val in enumerate(self.button_list):
                # Check button press
                if val["button"].collidepoint(self.goal): return index
            pygame.display.update()


    def update_goal_running(self):
        # Capture goal from Mouse Pointer
        keys = pygame.key.get_pressed()
        # Press Q to pause simulation and return to menu
        if keys[pygame.K_q]: self.running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Capture goal
                self.goal = np.array(pygame.mouse.get_pos())
                

    def simulate(self, K, system, plot_flag=0):
        # Final Simulation Function
        t = 0.
        state_list = []
        force_list = []
        self.running = True

        while self.running:
            self.update_goal_running()
            system.load(goal=self.goal)
            text_dict = self.text_box("{:.2f}".format(t), (self.x_screen//2, 20))
            
            system.draw_game()
            self.place_text(text_dict)
            pygame.display.update()

            F, _ = get_force(K, system)
            system.step_sim(F)
            t += system.dt

            if plot_flag:
                # Plotting states and forces using plot_flag
                state_list.append(np.copy(system.curr_state))
                force_list.append(F)
        
        if plot_flag:
            plot_states(state_list)
            plot_states(force_list)


#######################################################################################################
#######################################################################################################

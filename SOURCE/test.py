from sys import path
from os import listdir
from os.path import join
import customtkinter as ctk

from .DATA.read_write_bin import read_bin
from .CONTROLLER.pygame_handler import pygame_sys
from .DATA.pygame_assets import x_screen, y_screen

from .MODELS.drone import pygame_drone
from .MODELS.cart_pole import pygame_cart_pole
from .MODELS.drone_pole import pygame_drone_pole


# Supported modes : Light, Dark, System
ctk.set_appearance_mode("System")  
 
# Supported themes : green, dark-blue, blue
ctk.set_default_color_theme("green")   
 
# Dimensions of the window
appWidth, appHeight = 650, 350


#File Path and Test Environments
file_path = join(path[0], "SOURCE", "DATA", "")
test_systems = {"cart_pole": pygame_cart_pole,
                "drone": pygame_drone,
                "drone_pole": pygame_drone_pole}


# Class for handling the 
# systems to be simulated
class get_new_sys():
    def __init__(self, sys_type, sys_src_file, sys_name) -> None:
        # data[2] -> corresponding system config
        # data[3] -> K value for controller (A-Bk)
        data = read_bin(f"{file_path}{sys_src_file}")
        self.K = data[3]
        self.config = data[2]
        self.name = sys_name
        self.type = sys_type


# CustomTkinter App
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("LQR SIMULATOR")  
        self.geometry(f"{appWidth}x{appHeight}")
        self.resizable(0,0)
        
        iter = 0
        self.sys_list = []
        self.wlcm_txt = "HI!! Welcome to the Simulator!!!\nThank you for choosing it...\nChoose the system and the source file correctly!"

        # Buttons and Textboxes for various functions
        sys_type_label = ctk.CTkLabel(self, text="Choose System Type")
        sys_type_label.grid(row=iter, column=0, padx=10, pady=10, sticky="ew")
        
        self.sys_type_menu = ctk.CTkComboBox(self, values=list(test_systems.keys()))
        self.sys_type_menu.grid(row=iter, column=1, columnspan=1, padx=10, pady=10, sticky="ew")
        iter+=1
        
        file_label = ctk.CTkLabel(self, text="Choose Source File")
        file_label.grid(row=iter, column=0, padx=10, pady=10, sticky="ew")
        
        self.file_menu = ctk.CTkComboBox(self, values=self.get_files_list(file_path))
        self.file_menu.grid(row=iter, column=1, columnspan=1, padx=10, pady=10, sticky="ew")
        iter+=1

        sys_name_label = ctk.CTkLabel(self, text="Name of the System")
        sys_name_label.grid(row=iter, column=0, padx=10, pady=10, sticky="ew")

        self.sys_name = ctk.CTkTextbox(self, width=30, height=30)
        self.sys_name.grid(row=iter, column=1, columnspan=1, padx=10, pady=10, sticky="ew")
        iter+=1
        
        load_button = ctk.CTkButton(self, text="Load Data", command=self.load)
        load_button.grid(row=iter, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        iter+=1

        refresh_button = ctk.CTkButton(self, text="Refresh", command=self.refresh)
        refresh_button.grid(row=iter, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        iter+=1

        simulate_button = ctk.CTkButton(self, text="Simulate", command=self.simulate)
        simulate_button.grid(row=iter, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        iter+=1

        self.display = ctk.CTkTextbox(self, width=300, height=300) 
        self.display.grid(row=0, column=3, columnspan=4, rowspan=10, padx=10, pady=10)        
        self.display.insert("0.0", self.wlcm_txt)

    
    def get_files_list(self, file_path):
        files = listdir(file_path)
        return files


    def load(self):
        # Load the config of chosen system
        sys_type = self.sys_type_menu.get()
        sys_src_file = self.file_menu.get()
        sys_name = self.sys_name.get("0.0", "end")[:-1]
        curr_sys = get_new_sys(sys_type, sys_src_file, sys_name)
        if sys_name == "":
            details = "Please Enter Filename!"
        else:
            self.sys_list.append(curr_sys)
            details = "Systems to be Tested:\n"
            for system in self.sys_list:
                details += f"{system.name}\n"
            
        details += "\nChoose Your System to Begin!\Click to make it move to the Mouse Pointer\nPress Q to Pause Simulation\nPress Z at Main Menu to Exit"
        self.display.delete("0.0", "end")
        self.display.insert("0.0", details)


    def simulate(self):
        # PyGame Window for running simulations
        game = pygame_sys(x_screen, y_screen, "TEST")
        game.get_menu(self.sys_list)

        for system in self.sys_list:
            # Pass the Main Game Screen to be drawn on alongiwth the system configs
            system.func = test_systems[system.type](game.screen, **system.config)
            
        running = True
        while running:
            sys_index = game.button_pressed()
            if sys_index == None:
                running = False
            else:
                curr_sys = self.sys_list[sys_index]
                game.simulate(K=curr_sys.K, system=curr_sys.func)
        game.quit()


    def refresh(self):
        self.sys_list = []
        self.file_menu.configure(values=self.get_files_list(file_path))
        self.sys_type_menu.configure(values=list(test_systems.keys()))
        self.sys_name.delete("0.0", "end")
        self.display.delete("0.0", "end")
        self.display.insert("0.0", self.wlcm_txt)

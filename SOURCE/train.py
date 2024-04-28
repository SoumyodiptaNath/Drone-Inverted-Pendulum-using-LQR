from sys import path, exit
from os import listdir
from os.path import join
import customtkinter as ctk

from .DATA.read_write_bin import *
from .CONTROLLER.genetic_algo_QR import genetic_algo

from .MODELS.drone import simulate_drone
from .MODELS.cart_pole import simulate_cart_pole
from .MODELS.drone_pole import simulate_drone_pole


# Supported modes : Light, Dark, System
ctk.set_appearance_mode("System")  
 
# Supported themes : green, dark-blue, blue
ctk.set_default_color_theme("blue")   
 
# Dimensions of the window
appWidth, appHeight = 650, 450

#File Path and Test Environments
file_path = join(path[0], "SOURCE", "DATA", "")
params = {"GA Config": 0, "Training Config": 1, "System Config": 2}
train_systems = {"cart_pole": simulate_cart_pole,
                 "drone": simulate_drone, 
                 "drone_pole": simulate_drone_pole}


# Class for handling the 
# systems to be simulated
class get_new_sys():
    def __init__(self, sys_type, sys_src_file, sys_name) -> None:
        # data[0] -> genetic algo config
        # data[1] -> training config
        # data[2] -> corresponding system config
        # data[3] -> K value for controller (A-Bk)
        data = read_bin(f"{file_path}{sys_src_file}")
        self.data = data
        self.name = sys_name
        self.type = sys_type
    

# CustomTkinter App
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("LQR TRAINER USING GA")  
        self.geometry(f"{appWidth}x{appHeight}")
        self.resizable(0,0)
        
        iter = 0
        self.wlcm_txt = "HI!! Welcome to the Trainer!!!\nThank you for choosing it...\nChoose the paramters\nSet Output Filename\nFetch the file\nEdit the values here!"

        # Buttons and Textboxes for various functions
        sys_type_label = ctk.CTkLabel(self, text="Choose System Type")
        sys_type_label.grid(row=iter, column=0, padx=10, pady=10, sticky="ew")
        
        self.sys_type_menu = ctk.CTkComboBox(self, values=list(train_systems.keys()))
        self.sys_type_menu.grid(row=iter, column=1, columnspan=1, padx=10, pady=10, sticky="ew")
        iter+=1

        file_label = ctk.CTkLabel(self, text="Choose Source File")
        file_label.grid(row=iter, column=0, padx=10, pady=10, sticky="ew")
        
        self.file_menu = ctk.CTkComboBox(self, values=self.get_files_list(file_path))
        self.file_menu.grid(row=iter, column=1, columnspan=1, padx=10, pady=10, sticky="ew")
        iter+=1

        sys_name_label = ctk.CTkLabel(self, text="Output File Name")
        sys_name_label.grid(row=iter, column=0, padx=10, pady=10, sticky="ew")

        self.sys_name = ctk.CTkTextbox(self, width=30, height=30)
        self.sys_name.grid(row=iter, column=1, columnspan=1, padx=10, pady=10, sticky="ew")
        iter+=1

        fetch_button = ctk.CTkButton(self, text="Fetch", command=self.fetch)
        fetch_button.grid(row=iter, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        iter+=1

        param_label = ctk.CTkLabel(self, text="What to Change")
        param_label.grid(row=iter, column=0, padx=10, pady=10, sticky="ew")
        
        self.param_menu = ctk.CTkComboBox(self, values=list(params.keys()))
        self.param_menu.grid(row=iter, column=1, columnspan=1, padx=10, pady=10, sticky="ew")
        iter+=1

        fetch_button = ctk.CTkButton(self, text="Show", command=self.show)
        fetch_button.grid(row=iter, column=0, columnspan=1, padx=10, pady=10, sticky="ew")

        fetch_button = ctk.CTkButton(self, text="Change", command=self.change)
        fetch_button.grid(row=iter, column=1, columnspan=1, padx=10, pady=10, sticky="ew")
        iter+=1

        save_button = ctk.CTkButton(self, text="Save All", command=self.save)
        save_button.grid(row=iter, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        iter+=1

        train_button = ctk.CTkButton(self, text="Train", command=self.train)
        train_button.grid(row=iter, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        iter+=1

        refresh_button = ctk.CTkButton(self, text="Refresh", command=self.refresh)
        refresh_button.grid(row=iter, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        iter+=1

        self.display = ctk.CTkTextbox(self, width=300, height=425) 
        self.display.grid(row=0, column=3, columnspan=4, rowspan=10, padx=10, pady=10)        
        self.display.insert("0.0", self.wlcm_txt)

    
    def get_files_list(self, file_path):
        # Get files from directory
        files = listdir(file_path)
        return files


    def show_text(self, text):
        self.display.delete("0.0", "end")
        self.display.insert("0.0", text)


    def save(self):
        # Save the system config
        write_bin(self.sys.data, f"{file_path}{self.sys.name}")
        print("\nConfig & Weights Saved Succesfully!")

        
    def fetch(self):
        # Fetch the system accoding to entered data
        sys_type = self.sys_type_menu.get()
        sys_src_file = self.file_menu.get()
        sys_name = self.sys_name.get("0.0", "end")[:-1]
        if sys_name == "":
            details = "Please Enter Filename!"
        else:
            details = "File Fetched Successfully!"
            self.sys = get_new_sys(sys_type, sys_src_file, sys_name)
            if len(self.sys.data) < 3:
                details += f"\nMissing Paramters in Data!\nPlease Ensure that {'',''.join(list(params.keys()))} are Present!"
        self.show_text(details)
        

    def show(self):
        # Show config details
        if hasattr(self, 'sys'):
            index = params[self.param_menu.get()]
            details = ""
            for key, val in self.sys.data[index].items():
                details += f'"{key}":{val}\n'
        else:
            details = "Please Fetch the File first!"
        self.show_text(details)
    

    def change(self):
        # Change config details
        if hasattr(self, 'sys'):
            param = self.param_menu.get()
            index = params[param]
            details = '{' + ','.join(self.display.get("0.0", "end").split('\n')[:-2]) + '}'
            self.sys.data[index] = eval(details)
            print(f"{param} -> {self.sys.data[index]}")
            details = "Changes were made Successfully!"
        else:
            details = "Please Fetch the File first!"
        self.show_text(details)


    def train(self):
        # Train GA
        self.withdraw()
        self.quit()
        self.sys.data[0]["system"] = train_systems[self.sys.type]
        GA = genetic_algo(**self.sys.data[0], **self.sys.data[2])
        elite_chrom, max_fitness = GA.train(**self.sys.data[1])

        curr_bot = GA.pop_concur[0]
        Q, R = curr_bot.get_Q_R(elite_chrom)
        K = curr_bot.get_K(Q, R)
        details = f"\nR->{R}\nQ->{Q}\nK->{K}\nMax Fitness->{max_fitness}"
        print(f"\nTraining Results:\n{details}")

        if len(self.sys.data) < 4:
            self.sys.data.append(K)
        else:
            self.sys.data[3] = K
        del self.sys.data[0]["system"]
        self.save()
        exit()


    def refresh(self):
        del self.sys
        self.file_menu.configure(values=self.get_files_list(file_path))
        self.sys_type_menu.configure(values=list(train_systems.keys()))
        self.sys_name.delete("0.0", "end")
        self.show_text(self.wlcm_txt)
# Drone-Pole using LQR
![](https://github.com/SoumyodiptaNath/Drone-Pole-using-LQR/assets/122808862/7a3aa22f-4b79-4645-bb67-0531fedd3266)

A Python interface for balancing an iverted pendulum on a drone using a Linear Quadratic Controller where the Q and R matrices for penalising various state variables are fine-tuned using a Evolutionary Genetic Algorithm for best results.

Alongwith the drone-pole, a normal cart-pole and a drone have been implemented as well. All their weights and configuration files have been supplied for training and testing purposes.

HAVE FUN!!!


## Usage/Examples

- Download the project repository to your local machine
- Navigate to the project directory using ```cd```
- Install dependencies using ```pip install -r requirements.txt```
- Run `python3 run.py` if on Linux or Mac
- Run `python run.py` if on Windows
- Type 1 for training & 2 for testing any system


## Testing

<br>
<img width="487" alt="test_ss_1" src="https://github.com/SoumyodiptaNath/Drone-Pole-using-LQR/assets/122808862/c609706c-6009-4183-a286-bf3dd99c8f4c">
<br><br>

In the GUI:
- ```Choose System Type``` using dropdown menu
- ```Choose Source File``` (of the system) using dropdown menu
- Enter ```Name of the System``` to be displayed during simulation
- ```Load Data``` to get the details from source file
- Multiple Systems can be loaded simultaneously
- Their names appear in the text-box
- ```Simulate``` to intiate simulation

<br>
<img width="960" alt="test_ss_2" src="https://github.com/SoumyodiptaNath/Drone-Pole-using-LQR/assets/122808862/57c0aa11-57ff-4ad4-8898-3576b33bab4c">
<br><br>

- A new window launches for simulation
- Choose the system name in the menu to simulate
- Press ```Q``` to pause the simulation and return to main menu
- Press ```Z``` at the main menu to exit
- ```Refresh``` to start-over
  
<br>
<img width="959" alt="test_ss_3" src="https://github.com/SoumyodiptaNath/Drone-Pole-using-LQR/assets/122808862/e8b15db6-382e-4c86-80f0-470737219906">
<br><br>

## Training

<br>
<img width="484" alt="train_ss" src="https://github.com/SoumyodiptaNath/Drone-Pole-using-LQR/assets/122808862/d72d3cf9-b295-4f12-9903-d09e17793e73">
<br><br>

In the GUI:
- ```Choose System Type``` using dropdown menu
- ```Choose Source File``` (of the system) using dropdown menu
- Enter ```Output Filename``` to store new weights & configs
- ```Fetch``` the details from old source file
- Choose ```What to Change``` using dropdown menu
- ```Show``` the contents of the param on the text-box
- Change the values of the parameters in the text-box itself
- CAUTION: Dont alter the names of parameters inappropriately
- ```Change``` the parameters accordingly
- ```Save All``` to save current config
- ```Train``` to intiate training
- While training the GUI will close
- All updates will appear on terminal
- ```Refresh``` to start-over


## System Configurations

Every system (drone-pole / drone / cart-pole / your custom model) should have the following configurations in the given order:

```
SOURCE/DATA/system.bin
(a list of dictionaries)
    ga_config = {
        max_steps: Maximum steps for simulation,
        goal: Desired target coordinate,
        pop_size: Population size per generation,
        num_concur: No. of agents evaluated parallely,
        levels_var: No. of binary levels per design variable,
        num_var: No. of design variables to be optimized
    }

    train_conf = {
        num_gen: Number of generations
        cross_prob: Crossover Probability
        mut_prob: Mutation Probability
    }

    sys_config = {
        system paramters
        like dimensions, mass, dampning factor,
        acceleration due to gravity and so on;
        depends on the system parameters
    }
```


## Contributing

Contributions are always welcome! 

This project is open to contributions, bug reports, and suggestions. If you've found a bug or have a suggestion, please open an issue.
## 🛠 Skills
Linear Control Systems, Numerical Methods, Physics Simulation, Python, PyGame, CustomTkinter


## Acknowledgements

 - [Control Bootcamp, Steve Brunton](https://youtube.com/playlist?list=PLMrJAkhIeNNR20Mz-VpzgfQs5zrYi085m&si=xTh4PWrXEwkV3x2L) is great for beginners!

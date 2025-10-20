# Evolving Stability: Drone-Pole Control with LQR & Genetic Algorithms

This project tackles the classic, notoriously difficult challenge of balancing an inverted pendulum, but with a modern twist: the pendulum is mounted on a quadcopter drone. Control is achieved using a **Linear Quadratic Regulator (LQR)**, whose critical Q and R matrices are intelligently fine-tuned by a **Genetic Algorithm (GA)** to discover the optimal balancing strategy.

The result is a robust, self-tuning control system brought to life in a versatile Python simulation environment.

<p align="center">
<kbd><img src="https://github.com/SoumyodiptaNath/Drone-Pole-using-LQR/assets/122808862/7a3aa22f-4b79-4645-bb67-0531fedd3266"></kbd>
</p>

## 🧠 The Core Concepts

-   **The Challenge: The Inverted Pendulum**
    A classic problem in control theory, balancing a pole is inherently unstable. The drone must make constant, precise adjustments to counteract gravity and disturbances, making it a perfect testbed for advanced control algorithms.

-   **The Controller: Linear Quadratic Regulator (LQR)**
    LQR is an optimal control technique that determines the best possible adjustments by minimizing a cost function. This function penalizes both state deviations (e.g., the pole's angle) and control effort (e.g., the drone's motor thrust). The key is choosing the right penalty matrices, `Q` (for state) and `R` (for effort).

-   **The Optimizer: Genetic Algorithm (GA)**
    How do we find the *best* `Q` and `R` matrices? This is where the GA comes in. By simulating a population of controllers and applying principles of evolution—selection, crossover, and mutation—the algorithm iteratively "evolves" the LQR parameters towards optimal performance, discovering highly effective and sometimes non-obvious balancing strategies.

## ✨ Features

-   **GA-Tuned LQR Controller**: A powerful combination for solving complex control problems.
-   **Multi-System Simulation**: Includes pre-configured models for a **Drone-Pole**, a classic **Cart-Pole**, and a standalone **Drone**.
-   **Interactive GUI**: A user-friendly interface built with `CustomTkinter` for both training new models and testing existing ones.
-   **Modular Configuration**: Easily define and customize your own physical systems and training parameters.
-   **Side-by-Side Comparison**: Load and simulate multiple systems simultaneously to compare their performance visually.

## 🚀 Getting Started

### 1. Prerequisites

-   Python 3.x
-   Git

### 2. Installation

```bash
# Clone the repository
git clone [https://github.com/your-username/Drone-Pole-using-LQR.git](https://github.com/your-username/Drone-Pole-using-LQR.git)

# Navigate to the project directory
cd Drone-Pole-using-LQR

# Install all required dependencies
pip install -r requirements.txt
````

### 3\. Launch the Application

```bash
# On Linux or macOS
python3 run.py

# On Windows
python run.py
```

You will be prompted to choose between **Training (1)** or **Testing (2)** mode.

## 🧪 Testing Mode: Simulating a Pre-Trained Model

The testing interface allows you to load and visualize the performance of different controllers.

<center>
<img width="487" height="282" alt="test_ss_1" src="https://github.com/user-attachments/assets/031a98f9-5812-4178-ae1b-0b3ad40b1527" />
</center>

#### Workflow:

1.  **Select a System** (`Drone-Pole`, `Cart-Pole`, etc.) from the dropdown.
2.  **Choose a Configuration File** containing the pre-trained weights.
3.  **Give it a Name** for the simulation list.
4.  Click **Load Data**. You can load multiple systems to compare.
5.  Click **Simulate** to launch the visualization window.


#### In the Simulation Window:

  - **Select** which loaded system to visualize from the dropdown.
  - Press **Q** to pause and return to the main menu.
  - Press **Z** at the main menu to exit the application.

<center>
<img width="960" height="358" alt="test_ss_2" src="https://github.com/user-attachments/assets/884dd857-cb9e-472e-9a87-a4e8890dd570" />
</center>

<center>
<img width="959" height="328" alt="test_ss_3" src="https://github.com/user-attachments/assets/52aa637a-e6b1-41d0-a6e3-1a5fd8a2740a" />
</center>

## 🧬 Training Mode: Evolving a New Controller

The training interface lets you configure and launch a new Genetic Algorithm training session.

<img width="484" height="359" alt="train_ss" src="https://github.com/user-attachments/assets/a929b20f-3177-4399-8ad8-939d0e33f40d" />

#### Workflow:

1.  **Select System Type** and a **Source File** to use as a template.
2.  Enter an **Output Filename** where the new trained model will be saved.
3.  **Fetch** the template data.
4.  **Choose What to Change** (`GA Config`, `Train Config`, or `System Config`).
5.  **Modify** the parameters directly in the text box.
6.  **Save** your changes and click **Train** to begin.
7.  The GUI will close, and progress will be printed to the terminal.

## ⚙️ System Configuration Structure

Each system is defined by a `.bin` file containing a list of Python dictionaries. This structure allows for easy customization and extension.

```python
# Located in: SOURCE/DATA/your_system.bin

[
    # Genetic Algorithm settings
    ga_config = {
        "max_steps": 1000,      # Max simulation steps per evaluation
        "goal": [0, 0, 0, 0],  # Target state for the system
        "pop_size": 50,         # Number of individuals per generation
        # ... and other GA parameters
    },

    # Training session settings
    train_conf = {
        "num_gen": 100,         # Number of generations to evolve
        "cross_prob": 0.8,      # Crossover probability
        "mut_prob": 0.1,        # Mutation probability
    },

    # Physical properties of the system
    sys_config = {
        "mass_pole": 0.5,
        "length_pole": 1.0,
        "mass_drone": 1.5,
        # ... and other physical constants
    }
]
```

## 🛠️ Tech Stack

  - **Control Theory**: Linear Quadratic Regulator (LQR), State-Space Representation
  - **Optimization**: Genetic Algorithms
  - **Simulation**: PyGame
  - **GUI**: CustomTkinter
  - **Core Language**: Python (NumPy, SciPy)

## 🤝 Contributing

Contributions are always welcome\! This project is open to bug reports, feature requests, and suggestions. Please feel free to open an issue or submit a pull request.

## 🙏 Acknowledgements

  - A huge thanks to Steve Brunton's **[Control Bootcamp](https://youtube.com/playlist?list=PLMrJAkhIeNNR20Mz-VpzgfQs5zrYi085m&si=xTh4PWrXEwkV3x2L)** series on YouTube. It's an incredible resource for anyone new to control theory.


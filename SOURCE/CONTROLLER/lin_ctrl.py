import numpy as np
from control import lqr


#######################################################################################################
#######################################################################################################


def get_sys_matrix(system, step=1.):
    '''
    Linearizing the system numerically
    Obtaining X' = AX + Bu
    '''
    tot_cols = system.num_states + system.num_inputs
    A_B = np.zeros((system.num_states, tot_cols))
    states_inputs = np.identity(tot_cols)

    if system.num_inputs == 1: 
        force = lambda val_arr : val_arr[0] 
    else: 
        force = lambda val_arr : val_arr

    # Taking a step in the direction of every state to get the gradient
    accelerations_0 = system.step_sim(force(np.zeros(system.num_inputs)))
    for i in range(tot_cols):
        system.curr_state = states_inputs[i, :system.num_states]
        accelerations_1 = system.step_sim(force(states_inputs[i,system.num_states:]))
        A_B[:system.num_states//2, i] = np.copy(system.curr_state[system.num_states//2:])/step
        A_B[system.num_states//2:, i] = np.copy(accelerations_1-accelerations_0)/step

    A = A_B[:, :system.num_states]
    B = A_B[:, system.num_states:]    
    return A, B


#######################################################################################################
#######################################################################################################


def get_K_matrix(A, B, Q, R):
    '''
    Generating K matrix using LQR
    Q and R are 1D matrices which
    are turned into diagonal matrices
    X' = AX + Bu; u = -KX (Feedback)
    Using LQR to find K in X' = (A-BK)X
    '''
    K, _, _ = lqr(A, B, np.diag(Q), np.diag(R))
    K = np.squeeze(K)
    return K


#######################################################################################################
#######################################################################################################


def get_force(K, system):
    '''
    Generating the Feedback
    Force = u = -KX
    '''
    err = system.curr_state - system.steady_state
    return -np.dot(K, err), err


#######################################################################################################
#######################################################################################################
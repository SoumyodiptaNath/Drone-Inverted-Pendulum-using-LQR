import numpy as np
from tqdm import tqdm
from .lin_ctrl import *
import concurrent.futures
import matplotlib.pyplot as plt


#######################################################################################################
#######################################################################################################


class genetic_algo():
    def __init__(self, system, max_steps, goal, pop_size,
                 num_concur, levels_var, num_var, **sys_params):
        
        if pop_size % num_concur != 0:
            raise ValueError("Population Size must be divisble by number of concurrent bots")
        
        '''
        num_var: Number of Variables to be trained
        pop_size: Population Size
        num_concur: Number of bots to be evaluated parallelly
        levels_var: Number of binary levels per design variable
        fitness: Array of fitness of current generation
        pop_chrom: Array of chromosomes of the population
        pop_concur: Array of bots to be trained parallelly
        
        Chromosome contain design variables
        Here they contain the diagonal elements of Q & R'''

        goal = np.array(goal)
        self.num_var = num_var
        self.pop_size = pop_size
        self.num_concur = num_concur
        self.levels_var = levels_var
        self.fitness = np.zeros(pop_size)
        self.pop_chrom = np.random.randint(0, 2**levels_var-1, size=(pop_size, num_var))
        self.pop_concur = [system(goal, max_steps, **sys_params) for _ in range(num_concur)]

        
    def restore_elite(self, elite_indices, elite_chrom):
        # Following Elitist Genetic Algorithm
        self.pop_chrom[elite_indices,:] = np.copy(elite_chrom)


    def evaluate_all(self):
        # Spli into batches and go for multiprocessing
        for batch in range(self.pop_size//self.num_concur):
            with concurrent.futures.ProcessPoolExecutor() as executor:
                results = []
                curr_index = batch*self.num_concur
                for i in range(self.num_concur):
                    results.append(executor.submit(self.pop_concur[i].run, self.pop_chrom[curr_index+i], curr_index+i))

                for f in concurrent.futures.as_completed(results):
                    curr_fitness, chrom_index = f.result()
                    self.fitness[chrom_index] = curr_fitness
    

    def reproduce(self):
        # Diminishing the effect of least fit chromosome
        self.fitness[self.fitness<0.] = 0.
        fitness = self.fitness - 0.9*np.min(self.fitness)
        elite_id = np.argmax(fitness)
        prob = fitness/np.sum(fitness)

        # Probability based selection of offsprings
        offspring_indices = np.random.choice(np.arange(self.pop_size), 
                                             size=self.pop_size, 
                                             replace=True, p=prob)

        offspring_indices[elite_id] = elite_id
        offsprings = np.copy(self.pop_chrom[offspring_indices])
        self.pop_chrom = offsprings[offspring_indices]

        # Ensuring elite is carried over
        elite_indices = offspring_indices==elite_id
        elite_chrom = self.pop_chrom[elite_id]
        return elite_indices, elite_chrom


    def crossover(self, cross_prob):
        # Crossover between current and immediately next chromosome
        cross_id = np.random.random((self.pop_size, self.num_var)) < cross_prob
        temp_pop = np.roll(self.pop_chrom, 1, axis=0) 
        self.pop_chrom[cross_id], temp_pop[cross_id] = temp_pop[cross_id], self.pop_chrom[cross_id]
    

    def mutate(self, mut_prob):
        # Random mutation using bitwise XOR
        mutation_indices = np.random.random((self.levels_var, self.num_var*self.pop_size)) < mut_prob
        mutation_vals = (1 << np.arange(self.levels_var)) @ mutation_indices
        mutation_vals = np.reshape(mutation_vals, (self.pop_size, self.num_var))
        self.pop_chrom = np.bitwise_xor(self.pop_chrom, mutation_vals)
    

    def train(self, num_gen, cross_prob, mut_prob):
        '''
        num_gen: Number of generations
        cross_prob: Crossover Probability
        mut_prob: Mutation Probability
        '''
        # Overall training process
        fitness_history = []
        for _ in tqdm(range(num_gen)):
            self.pop_chrom[self.pop_chrom==0] = 1
            
            self.evaluate_all()
            elite_indices, elite_chrom = self.reproduce()
            
            self.crossover(cross_prob)
            self.mutate(mut_prob)

            self.restore_elite(elite_indices, elite_chrom)
            fitness_history.append(np.copy(self.fitness))
        
        max_fitness = np.max(self.fitness)
        plt.imshow(fitness_history)
        plt.show()
        
        return elite_chrom, max_fitness
    

#######################################################################################################
#######################################################################################################


from ga import GA
import numpy as np 
import multiprocessing as mp 
from rbs import RBS

weights1 = {'name': 'w1', 
            'f_vol':0.2,
            'f_connect':0.2,
            'f_discon':0.2,
            'f_cur':0.2,
            'f_cost':-0.2}

weights2 = {'name': 'w2', 
            'f_vol':0.25,
            'f_connect':0.25,
            'f_discon':0.25,
            'f_cur':0,
            'f_cost':-0.25}

weights3 = {'name': 'w3', 
            'f_vol':0,
            'f_connect':0.25,
            'f_discon':0.25,
            'f_cur':0.25,
            'f_cost':-0.25}

# ga_steps = 10000 
ga_steps = 30000 

rbs_names_eva = ['a','b','c','d','f','g','h','i','j']

ga_nums = 150

num_bats_hpar = 3
num_sws_hpar = num_bats_hpar*5

pc_hpar = [ 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
pm_hpar = [0.01, 0.05, 0.1, 0.15, 0.2]

pc_opti  = 0.75
pm_opti  = 0.2

from ga import GA
import numpy as np 
import os
from rbs import RBS
from config import *
import pandas as pd
import random

def setup_seed(seed):
    np.random.seed(seed)
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    return

def optimize(num_bats,num_swtiches,weight,nums,pc,pm,steps):
    # setup_seed(5)
    setup_seed(10)
    Optimer = GA(num_bats,num_swtiches,weight,nums=nums,prob_cross=pc,prob_mutat=pm,steps=steps)
    best_fitness,best_chromosome = Optimer.evolution()
    # res = {'best_fitness':best_fitness,
    #         'best_chromosome':best_chromosome}
    df_res = pd.DataFrame(  {'best_fitness':best_fitness,
                            'best_chromosome':best_chromosome})
    res_path = './results/opti_process_'+str(num_bats)+'_'+str(num_swtiches)+'_'+weight['name']+'_'+str(steps)+'_'+str(nums)+'_'+str(pc)+'_'+str(pm)+'.csv'
    df_res.to_csv(res_path)
    return

def select_best_chro(num_bats,weights,nums,pc,pm,steps):
    fitness, chro = [], []
    for num_sw in range(num_bats*2,num_bats*5+1):
        res_path = './results/opti_process_'+str(num_bats)+'_'+str(num_sw)+'_'+weights['name']+'_'+str(steps)+'_'+str(nums)+'_'+str(pc)+'_'+str(pm)+'.csv'
        data = pd.read_csv(res_path)
        fitness = fitness + [data['best_fitness'].values[-1]]
        chro = chro + [data['best_chromosome'].values[-1]]
    best_fit = min(fitness)
    fit_res, chro_res = [], []
    for i in range(len(fitness)):
        if abs(best_fit - fitness[i]) <= 0.01:
            best_chro = chro[fitness.index(best_fit)]
            best_chro = best_chro.replace('[','')
            best_chro = best_chro.replace(']','')
            best_chro = [int(x) for x in best_chro.split()]
            fit_res.append(fitness[i])
            chro_res.append(best_chro)
    return fit_res, chro_res

def select_best_chro2(num_bats,weights,nums,pc,pm,steps):
    num_sw = num_bats*5
    res_path = './results/opti_process_'+str(num_bats)+'_'+str(num_sw)+'_'+weights['name']+'_'+str(steps)+'_'+str(nums)+'_'+str(pc)+'_'+str(pm)+'.csv'
    data = pd.read_csv(res_path)
    fitness = data['best_fitness'].values[-1]
    chro = data['best_chromosome'].values[-1]
    chro = chro.replace('[','')
    chro = chro.replace(']','')
    chro = [int(x) for x in chro.split()]
    return fitness,chro


####### RBS评估 ###########
def T_eva_rbs(rbs_name,num_bats):
    RBSer = RBS()
    chro, terminal = RBSer.gene(rbs_name,num_bats)
    num_sws = int(len(chro)/2)-num_bats
    Opti = GA(num_bats,num_sws,weights1)
    res_dict = Opti.eva_chro(chro,num_bats,terminal=terminal)
    df_res = pd.DataFrame(res_dict, index=[0])
    df_res.to_csv('./results/indicator_'+rbs_name+'_'+str(num_bats)+'.csv')
    return

####### GA参数敏感性分析 ###
def T_hpar_sns(pc_ind,pm_ind):
    pc = pc_hpar[pc_ind]
    pm = pm_hpar[pm_ind]
    optimize(num_bats_hpar,num_sws_hpar,weights1,ga_nums,pc,pm,ga_steps)
    return

####### RBS优化  ###########
def T_opti(num_bats,num_sws,weight_ind):
    Weights = [weights1,weights2,weights3]
    weight = Weights[weight_ind]
    optimize(num_bats,num_sws,weight,ga_nums,pc_opti,pm_opti,ga_steps)
    return


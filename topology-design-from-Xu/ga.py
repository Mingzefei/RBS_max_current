# -*- coding: UTF-8 -*-
from copyreg import pickle
import numpy as np
import networkx  as nx
import copy
from mdgraph import MdGraph
from rbs import RBS

# 遗传算法
class GA:
    def __init__(self,num_bats,num_swtiches,weights,nums=100,prob_cross=0.8,prob_mutat=0.15,steps=100):
        self.weights = weights              # 多目标对应的权重
        self.num_bats = num_bats            # 电池数量
        self.num_swtiches = num_swtiches    # 开关数量
        self.steps = steps                  # 进化次数
        self.nums = nums                    # 种群数量
        self.prob_cross = prob_cross        # 交叉操作-染色体交叉概率
        self.prob_mutat = prob_mutat        # 变异操作-染色体变异概率
        self.num_edges = self.num_swtiches+ self.num_bats # RBS中边的数量
        self.num_nodes = self.num_edges//2 + 1  # 考虑到电路的连接规律，RBS中最多有n+1个顶点数
        self.ini_gene_dict = {  2:'gene_a',
                                3:'gene_g',
                                4:'gene_i',
                                5:'gene_j'}
            
    def evolution(self):
        # GA主流程
        out_str = 'num_bats--num_sws:--'+str(self.num_bats)+','+ \
                str(self.num_swtiches)+'_'+str(self.nums)+'_'+str(self.prob_cross)+'_'+str(self.prob_mutat)+'--start'
        print(out_str,flush=True)
        population,terminals = self.initialization()
        best_fitness,best_chromosome = [],[]
        fitness_p = self.evaluation(population,terminals=terminals)
        ind_ = fitness_p.index(np.min(fitness_p))
        best_fitness.append(fitness_p[ind_])
        best_chromosome.append(population[ind_])
        for i in range(self.steps):
            offspring = self.crossover(population)
            offspring = self.mutation(offspring)
            fitness_offspring = self.evaluation(offspring)
            population = population+offspring
            fitness = fitness_p+fitness_offspring

            ind_ = fitness.index(np.min(fitness))
            best_fitness.append(fitness[ind_])
            best_chromosome.append(population[ind_])

            population,fitness_p = self.selection(population,fitness)
        return best_fitness,best_chromosome

    def initialization(self,ini_type=1):
        # 初始化种群
        ## 基因编码：[边1-节点1，边1-节点2,……，边i-节点1，边i-节点2，……]
        chromosomes,terminals = [], []
        if ini_type == 0:
            # 方案1：完全随机
            for i in range(self.nums):
                graph_nodes = np.random.randint(0,self.num_nodes,size=self.num_edges*2)
                chromosomes.append(graph_nodes)
                terminals.append(None)
        elif ini_type == 1:
            # 方案2：基于现有RBS拓扑结构
            for i in range(self.nums):
                Rbs = RBS()
                if  2*self.num_bats <= self.num_swtiches <  2*self.num_bats+2:
                    gene,terminal = Rbs.gene_a(self.num_bats)
                elif 2*self.num_bats+2 <= self.num_swtiches <  3*self.num_bats+2:
                    gene,terminal = Rbs.gene_b(self.num_bats)
                elif 3*self.num_bats+2 <= self.num_swtiches <  4*self.num_bats:
                    gene,terminal = Rbs.gene_c(self.num_bats)
                elif 4*self.num_bats <= self.num_swtiches <  5*self.num_bats-1:
                    gene,terminal = Rbs.gene_i(self.num_bats)
                else:
                    gene,terminal = Rbs.gene_j(self.num_bats)

                terminals.append(terminal)
                extra_nodes = np.random.randint(min(gene),max(gene),size=(self.num_edges*2-len(gene)))
                extra_nodes = [node_ for node_ in extra_nodes]
                gene = np.asarray(gene+extra_nodes)
                chromosomes.append(gene)
        return chromosomes, terminals
    
    def crossover(self,population):
        offspring = []
        random_values = np.random.rand(len(population)//2)
        len_chro = len(population[0])
        for i in range(len(random_values)):
            if random_values[i] <= self.prob_cross:
                fa, ma = population[i],population[-1-i]
                # 双点交叉法，随机选择两个交叉点 （fa, ma 上的交叉点的位置相同）
                ind_ = np.random.randint(0,len_chro,size=2)
                ind_ = np.sort(ind_)
                son1 = copy.deepcopy(fa);   son1[ind_[0]:ind_[1]] = ma[ind_[0]:ind_[1]]
                son2 = copy.deepcopy(ma);   son2[ind_[0]:ind_[1]] = fa[ind_[0]:ind_[1]]
                offspring = offspring + [son1] + [son2]
        return offspring 
    
    def mutation(self,population):
        # 多点随机突变
        num_mutat = 4                           # 突变点个数
        prob_mutat = self.prob_mutat            # 每个基因的突变概率
        len_chro = len(population[0])
        offspring = []
        rand_values = np.random.rand(len(population))   # 随机抽样确定待变异个体
        mut_inds = np.where(rand_values < prob_mutat)[0]
        if mut_inds.size > 0:
            for ind in mut_inds:
                gene = copy.deepcopy(population[ind])
                index_mutat = np.random.randint(0,len_chro,size=num_mutat) # 变异点位置
                node = np.random.randint(0,self.num_nodes,size=num_mutat)   # 变异值
                gene[index_mutat] = node
                offspring.append(gene)
        return offspring

    def eva_chro(self,chro,num_bats,terminal=None):
        num_sws = int(len(chro)/2)-num_bats
        GRA = MdGraph(num_bats,num_sws)
        if terminal is None:
            G = GRA.build(chro)
            G,terminal = GRA.select_circuit(G)
            res = GRA.eva_main(G,terminal)
        else:
            G = GRA.build(chro)
            res = GRA.eva_main(G,terminal)
        return res

    def evaluation(self,population,terminals=None):
        fitness = []
        if terminals is None:
            for chro in population:
                res = self.eva_chro(chro,self.num_bats)
                fit = 0 
                for fea in res.keys():
                    fit = fit + res[fea]*self.weights[fea]
                fitness.append(-fit)
        else:
            for i in range(len(population)):
                chro,terminal = population[i],terminals[i]
                res = self.eva_chro(chro,self.num_bats,terminal=terminal)
                fit = 0 
                for fea in res.keys():
                    fit = fit + res[fea]*self.weights[fea]
                fitness.append(-fit)
        
        return fitness

    def selection(self,population,raw_fitness):
        # 精英法 选择
        fitness = np.asarray(copy.deepcopy(raw_fitness))
        sort_inds = np.argsort(fitness)[:self.nums]
        select_pop = [population[ind_] for ind_ in sort_inds]
        fitness_pop = [raw_fitness[ind_] for ind_ in sort_inds]

        return select_pop, fitness_pop

class GA2(GA):
    def __init__(self,num_bats,num_swtiches,weights,nums=100,prob_cross=0.8,prob_mutat=0.15,steps=100) -> None:
        super(GA2,self).__init__(num_bats,num_swtiches,weights,nums=100,prob_cross=0.8,prob_mutat=0.15,steps=100)
        pass

    def crossover(self,population):
        # 基于图的交运算和并运算进行交叉
        offspring = []
        random_values = np.random.rand(len(population)//2)
        len_chro = len(population[0])
        for i in range(len(random_values)):
            if random_values[i] <= self.prob_cross:
                fa, ma = population[i],population[-1-i]
                # 首先构建仅区分有向图

                # 双点交叉法，随机选择两个交叉点 （fa, ma 上的交叉点的位置相同）
                ind_ = np.random.randint(0,len_chro,size=2)
                ind_ = np.sort(ind_)
                son1 = copy.deepcopy(fa);   son1[ind_[0]:ind_[1]] = ma[ind_[0]:ind_[1]]
                son2 = copy.deepcopy(ma);   son2[ind_[0]:ind_[1]] = fa[ind_[0]:ind_[1]]
                offspring = offspring + [son1] + [son2]
        return offspring  


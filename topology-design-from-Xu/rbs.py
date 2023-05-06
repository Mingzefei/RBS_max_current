# -*- coding: UTF-8 -*-
import numpy as np

class RBS():
    def __init__(self):
        pass
    
    def gene_a(self,num_bats):
        terminal = [0,num_bats*2]
        num_edges = num_bats *3
        gene = np.zeros(num_edges*2)
        for i in range(num_bats):
            # 电池
            gene[2*i] = 2*i+1
            gene[2*i+1] = i*2+2
            # 开关-类别1
            gene[num_bats*2+2*i] = 2*i
            gene[num_bats*2+2*i+1] = 2*i+1
            # 开关-类别2
            gene[num_bats*4+2*i] = 2*i
            gene[num_bats*4+2*i+1] = 2*i+2
        gene = [int(node) for node in gene]

        return gene,terminal
    
    def gene_b(self,num_bats):
        num_edges = num_bats*3+2
        terminal = [0,num_bats*2+2]
        gene = np.zeros(num_edges*2)
        for i in range(num_bats):
            # 电池
            gene[2*i] = 2*i+1
            gene[2*i+1] = i*2+2
            # 电池-类别1
            gene[num_bats*2+2*i] = 2*i
            gene[num_bats*2+2*i+1] = 2*i+1
            # 电池-类别2
            gene[num_bats*4+2*i] = 2*i
            gene[num_bats*4+2*i+1] = num_bats*2 + 1
        # 电池-类别3
        gene[num_bats*6] = num_bats*2
        gene[num_bats*6+1] = num_bats*2+2
        gene[num_bats*6+2] = num_bats*2
        gene[num_bats*6+3] = num_bats*2+1

        gene = [int(node) for node in gene]

        return gene, terminal
    
    def gene_c(self,num_bats):
        num_edges = num_bats*4+2
        gene = np.zeros(num_edges*2)
        terminal = [0,num_bats*3+2]
        for i in range(num_bats):
            # 电池
            gene[2*i] = 2*i+1
            gene[2*i+1] = i*2+2
            ## 方向1
            # 开关-类别1
            gene[num_bats*2+2*i] = 2*i
            gene[num_bats*2+2*i+1] = 2*i+1
            # 开关-类别2
            gene[num_bats*4+2*i] = 2*i
            gene[num_bats*4+2*i+1] = num_bats*2+1+i
            # 开关-类别3
            gene[num_bats*6+2*i] = num_bats*2+1+i
            gene[num_bats*6+2*i+1] = num_bats*2+2+i

        # 开关-类别4
        gene[num_bats*8] = num_bats*2
        gene[num_bats*8+1] = num_bats*3+1
        gene[num_bats*8+2] = num_bats*2
        gene[num_bats*8+3] = num_bats*3+2

        gene = [int(node) for node in gene]
        return gene,terminal

    def gene_d(self,num_bats):
        num_edges = num_bats*3+2
        gene = np.zeros(num_edges*2)
        terminal = [0,num_bats+2]
        for i in range(num_bats):
            # 电池
            gene[2*i] = i+1
            gene[2*i+1] = i+2
            # 开关-类别1
            gene[num_bats*2+2*i] = 0
            gene[num_bats*2+2*i+1] = i+1
            # 开关-类别2
            gene[num_bats*4+2*i] = num_bats+2
            gene[num_bats*4+2*i+1] = i+1
        # 开关-类别3
        gene[num_bats*6] = 0
        gene[num_bats*6+1] = num_bats+1
        gene[num_bats*6+2] = num_bats+1
        gene[num_bats*6+3] = num_bats+2

        gene = [int(node) for node in gene]
        return gene, terminal

    def gene_f(self,num_bats):
        num_edges = (num_bats-1)*4+1
        gene = np.zeros(num_edges*2)
        terminal = [1,num_bats*2]
        for i in range(num_bats):
            # 电池
            gene[2*i] = 2*i+1
            gene[2*i+1] = i*2+2
        for i in range(num_bats-1):
            # 开关-类别1
            gene[num_bats*2+2*i] = 2*i+1
            gene[num_bats*2+2*i+1] = 2*i+3
            # 开关-类别2
            gene[num_bats*4-2+2*i] = 2*i+2
            gene[num_bats*4-2+2*i+1] = 2*i+3
            # 开关-类别3
            gene[num_bats*6-4+2*i] = 2*i+2
            gene[num_bats*6-4+2*i+1] = 2*i+4
        gene = [int(node) for node in gene]
        return gene,terminal 

    def gene_h(self,num_bats):
        num_edges = (num_bats-1)*4+3
        gene = np.zeros(num_edges*2)
        terminal = [0,num_bats*2+1]
        for i in range(num_bats):
            # 电池
            gene[2*i] = 2*i+1
            gene[2*i+1] = i*2+2
            # 开关-类别1
            gene[num_bats*2+2*i] = 0
            gene[num_bats*2+2*i+1] = 2*i+1

        for i in range(num_bats-1):
             # 开关-类别2
            gene[num_bats*4+2*i] = 2*i+2
            gene[num_bats*4+2*i+1] = 2*i+3
             # 开关-类别3
            gene[num_bats*6-2+2*i] = num_bats*2
            gene[num_bats*6-2+2*i+1] = 2*i+2
        # 开关-类别4
        gene[-2] = num_bats*2
        gene[-1] = num_bats*2+1

        gene = [int(node) for node in gene]
        return gene, terminal

    def gene_j(self,num_bats):
        num_edges = (num_bats-1)*6+5
        gene = np.zeros(num_edges*2)
        terminal = [num_bats*2+2,num_bats*2+3]
        for i in range(num_bats):
             # 电池
            gene[2*i] = 2*i+1
            gene[2*i+1] = i*2+2
            # 开关-类别1
            gene[num_bats*2+2*i] = 0
            gene[num_bats*2+2*i+1] = 2*i+1
            # 开关-类别2
            gene[num_bats*4+2*i] = num_bats*2+1
            gene[num_bats*4+2*i+1] = 2*i+2
        for i in range(num_bats-1):
            # 开关-类别3
            gene[num_bats*6+2*i] = 2*i+2
            gene[num_bats*6+2*i+1] = 2*i+3
            # 开关-类别4
            gene[num_bats*8-2+2*i] = 2*i+1
            gene[num_bats*8-2+2*i + 1] = 2*i+3
            # 开关-类别5
            gene[num_bats*10-4+2*i] = 2*i+2
            gene[num_bats*10-4+2*i+1] = 2*i+4
        # 开关-类别6
        gene[num_edges*2-4] = 0
        gene[num_edges*2-3] = num_bats*2+2
        gene[num_edges*2-2] = num_bats*2+1
        gene[num_edges*2-1] = num_bats*2+3

        gene = [int(node) for node in gene]
        return gene,terminal
    
    def gene_g(self,num_bats):
        num_edges = (num_bats-1)*4+2
        gene = np.zeros(num_edges*2)
        terminal = [0,num_bats*2]
        for i in range(num_bats):
            # 电池
            gene[2*i] = 2*i+1
            gene[2*i+1] = i*2+2
            # 开关-类别1
            gene[num_bats*2+2*i] = 0
            gene[num_bats*2+2*i+1] = 2*i+1
        for i in range(num_bats-1):
            # 开关-类别2
            gene[num_bats*4+2*i] = 2*i +2
            gene[num_bats*4+2*i+1] = 2*i +3
            # 开关-类别3
            gene[num_bats*6-2+2*i] = 2*i +2
            gene[num_bats*6-2+2*i+1] = 2*i +4

        gene = [int(node) for node in gene]

        return gene,terminal

    def gene_i(self,num_bats):
        num_edges = num_bats*5
        gene = np.zeros(num_edges*2)
        terminal = [num_bats*2+2,num_bats*2+3]
        for i in range(num_bats):
            # 电池
            gene[2*i] = 2*i+1
            gene[2*i+1] = i*2+2
            # 开关-类别1
            gene[num_bats*2+2*i] = 0
            gene[num_bats*2+2*i+1] = 2*i+1
            # 开关-类别2
            gene[num_bats*4+2*i] = 2*num_bats+1
            gene[num_bats*4+2*i+1] = 2*i+2
        for i in range(num_bats-1):
            # 开关-类别3
            gene[num_bats*6+2*i] = 2*i+2
            gene[num_bats*6+2*i+1] = 2*i+3
            # 开关-类别4
            gene[num_bats*8-2+2*i] = 2*i+2
            gene[num_bats*8-2+2*i+1] = 2*i+4
        # 开关-类别5
        gene[num_edges*2-4] = 0
        gene[num_edges*2-3] = num_bats*2+2
        gene[num_edges*2-2] = num_bats*2+1
        gene[num_edges*2-1] = num_bats*2+3
        
        gene = [int(node) for node in gene]
        return gene,terminal

    def gene(self,rbs_name,num_bats):
        lc = locals()
        exec('gene,terminal = self.gene_'+rbs_name+'(num_bats)')
        gene,terminal = lc['gene'], lc['terminal']
        return gene,terminal


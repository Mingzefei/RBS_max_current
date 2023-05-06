# TopologyDesign

#### Description
python3 implementation of "Topology design for RBS"

#### TODO
· 计算重构灵活性时，考虑每条通路可能导致其他电池短路的情况，并排除该通路，相应地，更新输出调节能力的计算程序   
· 添加电池短路故障容忍率 ？

#### Framework  
- rbs.py   
    构造现有拓扑结构对应的gene  
- mdgraph.py  
    根据gene构造有向图，并对其各项指标进行计算
- ga2.py  
    遗传算法
- optimize.py  
    进行优化计算  
- evaluate_rbs.py  
    评价现有拓扑结构的各项指标  
- results  
    - figs  
        结果图  
    - opti  
        不同电池数量-不同开关数量-不同超参数下的优化结果  
    - ts_rbs  
        不同拓扑结构的评价结果

#### Run  
1. evaluate_rbs.py : 计算现有拓扑结构的各项指标  
2. 获取现有拓扑结构各项指标的最大值  
3. optimize.py : 参数敏感性分析  
4. optimize.py : 对各种电池数量-开关数量下的拓扑进行优化 
5. figs.ipynb  : 画图 

#### Requirements 

#### Liscense

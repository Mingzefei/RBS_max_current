# -*- coding: UTF-8 -*-

import networkx as nx 
import numpy as np
from itertools import combinations


class MdGraph:
    def __init__(self,num_bats,num_sws) :
        self.num_bats = num_bats
        self.num_sws = num_sws
        self.num_edges = num_bats + num_sws
        self.max_nodes = self.num_edges + 1
        pass

    def build(self,gene):
        # 根据gene构建图
        # 基因编码：[边1-节点1，边1-节点2,……，边i-节点1，边i-节点2，……]

        G = nx.MultiDiGraph()
        for j in range(len(gene)):  #添加节点
            G.add_node(gene[j],name=gene[j])

        for j in range(self.num_edges): # 添加有向边
            if j < self.num_bats:
                G.add_edge(gene[2*j],gene[2*j+1],key=j,edge_name=j,edge_label=j)
            else :  # 代表开关的边，要加上另一方向
                G.add_edge(gene[2*j],gene[2*j+1],key=j,edge_name=j,edge_label=j)
                G.add_edge(gene[2*j+1],gene[2*j],key=self.num_edges+j,edge_name=j,
                        edge_label=self.num_edges+j)
        return G

    def select_circuit(self,G):
        # 从图中选择连通图代表RBS并指定正负极, 以最大连通度的连通图作为电路图
        largest_cc = max(nx.weakly_connected_components(G), key=len)
        g_cc = G.subgraph(largest_cc)
        ## 以图中的编号最小、最大的点分别为电路的正负极
        nodes = list(g_cc.nodes)
        terminal = [min(nodes), max(nodes)]
        return g_cc, terminal

    def eva_main(self,G,terminal):
        f_cost = self.eva_cost(G)
        subG,paths_by_edge, bats_in_circuit, edge_terminal_dict, suc_edge_of_node = self.remove_extra_edge(G,terminal)
        valid_path_by_edge,bats_in_valid_circuit,nodes_of_series_bats_in_graph = self.get_valid_path(paths_by_edge,bats_in_circuit,edge_terminal_dict,suc_edge_of_node)
        paths_in_group = self.group_path( valid_path_by_edge)
        f_conn = self.eva_single_connect(bats_in_valid_circuit,paths_in_group)
        f_disc = self.eva_single_disconnect(valid_path_by_edge,bats_in_valid_circuit,paths_in_group)
        f_vol = self.eva_vol_range(bats_in_valid_circuit,paths_in_group)
        f_cur = self.eva_max_cur(subG,terminal,valid_path_by_edge,bats_in_valid_circuit,nodes_of_series_bats_in_graph)
        res = {'f_vol':f_vol,'f_connect':f_conn,'f_discon':f_disc,
                'f_cur':f_cur,'f_cost':f_cost}
        return res

    def eva_cost(self,G):
        # 计算连通图中的开关总数，作为成本
        edge_name = G.edges.data('edge_name')
        sws = [edge[-1] for edge in edge_name if edge[-1]>=self.num_bats]
        sws = set(sws)
        return len(sws)/(5*self.num_bats-1)

    def collect_info(self,G):
        edge_terminal_dict, bats_in_G,suc_edge_of_node,pre_edge_of_node = {}, [], {},{}
        for source,target,attr in G.edges(data=True):
            edge_terminal_dict[attr['edge_label']] = [source,target]
            if attr['edge_label'] < self.num_bats:
                bats_in_G = bats_in_G + [attr['edge_label']]

            if source not in suc_edge_of_node.keys():
                suc_edge_of_node[source] = [attr['edge_label']]
            else:
                suc_edge_of_node[source] = suc_edge_of_node[source] + [attr['edge_label']]
            if target not in pre_edge_of_node.keys():
                pre_edge_of_node[target] = [attr['edge_label']]
            else:
                pre_edge_of_node[target] = pre_edge_of_node[target] + [attr['edge_label']]
        return edge_terminal_dict, bats_in_G,suc_edge_of_node,pre_edge_of_node

    def build_subG(self,G,edges_in_subG):
        # 根据给出的边，从原图中构建子图
        edges_in_graph_ = [(source,target,attr) for edge in edges_in_subG for source,target,attr in G.edges(data=True) if attr['edge_label']==edge]
        edges_in_graph = []
        circuit_G = nx.MultiDiGraph()
        for (source,target,attr) in edges_in_graph_:
            if attr['edge_label'] > self.num_edges:
                edge_name_ = attr['edge_label']-self.num_edges
            else:
                edge_name_ = attr['edge_label']
            circuit_G.add_edge(source,target,key=attr['edge_label'],edge_label=attr['edge_label'],edge_name=edge_name_)

        edge_terminal_dict, bats_in_circuit,suc_edge_of_node,pre_edge_of_node = self.collect_info(circuit_G)
        return circuit_G, edge_terminal_dict,bats_in_circuit,suc_edge_of_node,pre_edge_of_node

    def remove_extra_edge(self,G,terminal):
        # 只保留在通路中的边,构成电路图
        paths_by_edge = []
        edges_in_circuit = []
        for path in nx.all_simple_edge_paths(G,*terminal):
            _path_by_edge = [edge_label for source, target, edge_label in path]
            paths_by_edge = paths_by_edge + [_path_by_edge]
            edges_in_circuit = edges_in_circuit + _path_by_edge 
        edges_in_circuit = set(edges_in_circuit)
        # 构建子图
        circuit_G, edge_terminal_dict,bats_in_circuit,suc_edge_of_node,pre_edge_of_node = self.build_subG(G,edges_in_circuit)
        return circuit_G, paths_by_edge, bats_in_circuit, edge_terminal_dict, suc_edge_of_node
    
    def get_node_of_series_bats(self,edge_terminal_dict,suc_edge_of_node,bat):
        '''
        采用深度优先搜索，找出该电池及其后继边中所有与该电池无开关直接串联电池所组成的端点
        '''
        stack = []
        stack.append(bat)
        seen = []
        seen.append(bat)
        nodes_of_series_bats = [edge_terminal_dict[bat]]
        while stack:
            bat_ = stack.pop()
            end_node = edge_terminal_dict[bat_][-1]
            if end_node in suc_edge_of_node:
                # bat_的终点不是系统终点的情况
                suc_bats = [edge_ for edge_ in suc_edge_of_node[end_node] if edge_<self.num_bats ]
                for suc_bat in suc_bats:
                    if suc_bat not in seen:
                        stack.append(suc_bat)
                        seen.append(suc_bat)
                nodes_of_series_bats = nodes_of_series_bats + [[edge_terminal_dict[bat][0],edge_terminal_dict[bat_][-1]]]
        return nodes_of_series_bats

    def sc_judge(self,path_by_edge,nodes_of_series_bats_in_graph,edge_terminal_dict):
        # 判断一条通路是否会造成其他电池短路
        path_by_node = [edge_terminal_dict[edge_][0] for edge_ in path_by_edge]
        path_by_node.append(edge_terminal_dict[path_by_edge[-1]][-1])
        res = False
        for node_pair in nodes_of_series_bats_in_graph:
            if all(node in path_by_node for node in node_pair):
                # 通路中存在两个端点，使得该2个端点之间有一条全是串联电池的其他通路
                ind1,ind2 = path_by_node.index(node_pair[0]),path_by_node.index(node_pair[1])
                suspicious_path_by_edge = path_by_edge[min(ind1,ind2):max(ind1,ind2)]
                if all(edge_>=self.num_bats for edge_ in suspicious_path_by_edge):
                    # 两端点间全为开关，则将导致短路
                    res = True
                    break
        return res 

    def get_valid_path(self,paths_by_edge,bats_in_circuit,edge_terminal_dict,suc_edge_of_node):
        # 获取从负极到正极的所有有效通路
        # 即：剔除可能导致其他电池短路的通路、没有电池的通路后的所有通路
        valid_path_by_edge = []
        nodes_of_series_bats_in_graph = [node_pair for bat in bats_in_circuit \
                    for node_pair in self.get_node_of_series_bats(edge_terminal_dict,suc_edge_of_node,bat)]
        bats_in_valid_circuit = []
        for path in paths_by_edge:
            if any(edge < self.num_bats for edge in path):
                # 通路中包含电池
                if not self.sc_judge(path,nodes_of_series_bats_in_graph,edge_terminal_dict):
                    # 该通路不会造成其他电池短路
                    bats_in_valid_circuit =  bats_in_valid_circuit + [edge_ for edge_ in path if edge_<self.num_bats]  
                    # 更新通路中的电池，排除仅存在于无效通路的电池
                    valid_path_by_edge.append(path)
        bats_in_valid_circuit = list(set(bats_in_valid_circuit))
        return valid_path_by_edge,bats_in_valid_circuit,nodes_of_series_bats_in_graph

    def group_path(self,paths_by_edge):
        ''' 
        每条通路都有一个以自身为最高层次的group,即该条通路连通，将直接导致其他通路也连通
        利用通路中除电池外的开关集合的包含、被包含关系进行分组
        对于全是电池的通路，其属于所有其他的分组
        '''
        sw_of_path = [[edge for edge in path if edge >= self.num_bats] for path in paths_by_edge]
        swSet_of_path = [set(sws) for sws in sw_of_path]
        paths_in_group = []
        for i in range(len(paths_by_edge)):
            group_inds = []
            for j in range(len(paths_by_edge)):
                if swSet_of_path[j].issubset(swSet_of_path[i]):
                    group_inds.append(j)
            paths_in_group = paths_in_group + [[paths_by_edge[ind] for ind in group_inds]]
        # print('paths_in_group',paths_in_group)
        # sw_path_dict = {}
        # paths_no_sw = []
        # for path in paths_by_edge:
        #     sw_in_path = [edge for edge in path if edge >= self.num_bats]
        #     if len(sw_in_path) == 0:
        #         # 该通路全是电池（固有连通）
        #         paths_no_sw = paths_no_sw + [path]
        #     else:
        #         sw_in_path = [sw if sw < self.num_edges else sw-self.num_edges for sw in sw_in_path]
        #         sw_in_path.sort()
        #         if str(sw_in_path) not in sw_path_dict.keys():
        #             sw_path_dict[str(sw_in_path)] = [path]
        #         else:
        #             sw_path_dict[str(sw_in_path)] = sw_path_dict[str(sw_in_path)] + [path]
        # paths_in_group = list(sw_path_dict.values())
        # # 将全是电池的固有通路添加到所有通路分组中
        # paths_in_group = [group+paths_no_sw for group in paths_in_group]
        
        return paths_in_group

    def eva_single_connect(self,bats_in_circuit,paths_in_group):
        ''' 
        其他电池可被完全断开且单个电池可被连通于电路,即：存在只包含该电池的通路组
        '''

        if any(bat_i not in bats_in_circuit for bat_i in range(self.num_bats)):
            # 存在电池不在有效通路中
            res = -1
        else:
            # 所有电池均在有效通路中
            res = []
            for i in range(self.num_bats):
                f_bat = 0
                for group in paths_in_group:
                    # TO DO:考虑一个group只有一条通路的情况
                    bat_in_group = [edge for path in group  for edge in path if edge < self.num_bats]
                    if i in bat_in_group and len(bat_in_group)==1:
                        f_bat = 1
                        break
                res.append(f_bat)
            res = sum(res)/len(res)
        return res

    def eva_single_disconnect(self,path_by_edge,bats_in_circuit,paths_by_group):
        '''
        单个电池可被断开且其他电池全部可被连通于电路
        即：该电池所在的所有通路均存在开关，且删除该电池所在所有同组通路后，其他所有的电池还可以被连通
        '''

        if any(bat_i not in bats_in_circuit for bat_i in range(self.num_bats)):
            # 存在电池不在有效通路中
            res = -1
        else:
            # 所有电池均在有效通路中
            res = []
            for bat in range(self.num_bats):
                path_contain_bat = [path for path in path_by_edge if bat in path]
                flag_path_contain_sw = [1 if any(edge>=self.num_bats for edge in path) else 0 for path in path_contain_bat]
                # 只要该group有包含该电池的通路，则group内的所有通路均应该断开
                group_to_discon = [group for group in paths_by_group if any(bat in path for path in group)]
                path_to_discon = []
                for group in group_to_discon:
                    path_to_discon = path_to_discon + group 
                path_exist = [path for path in path_by_edge if path not in path_to_discon]
                bats_exist = list(set([edge for path in path_exist for edge in path if edge <self.num_bats]))
                if all(flag for flag in flag_path_contain_sw) and len(bats_exist) == self.num_bats-1:
                    f_bat = 1
                    # print('path_exist:',path_exist)
                else:
                    f_bat = 0
                res.append(f_bat)
 
                # group_no_bat = [group for group in paths_by_group if all(bat not in path for path in group)]
                # bats_in_exist_group = [edge for group in group_no_bat for path in group for edge in path if edge<self.num_bats]
                # bats_in_exist_group = list(set(bats_in_exist_group))
                # if all(flag for flag in flag_path_contain_sw) and len(bats_in_exist_group) == self.num_bats-1:
                #     f_bat = 1
                # else:
                #     f_bat = 0
                # res.append(f_bat)
            res = sum(res)/len(res)
        return res

    def eva_vol_range(self,bats_in_circuit,paths_by_group):
        '''
        系统可主动调节的输出电压范围
        即：不同通路组的输出电压的档位数
        '''
        if any(bat_i not in bats_in_circuit for bat_i in range(self.num_bats)):
            # 存在电池不在有效通路中
            res = -1
        else:
            # 所有电池均在有效通路中
            # print(paths_by_group)
            vols = set([min([len([edge for edge in path if edge<self.num_bats]) for path in group]) for group in paths_by_group])
            # 对于同属一组的通路，取包含电池最少的通路电压为该组的输出电压
            res = len(vols)/self.num_bats
        return res

    def eva_max_cur(self,G,terminal,path_by_edge,bats_in_circuit,nodes_of_series_bats_in_graph):
        '''
        计算系统允许的最大电流(假设电池单体最大允许电流为1)
        贪心策略，近似计算，二分查找：
        对于每个电池，取该电池所在的最短通路作为参与并联的通路;
        贪心：认为由所有电池所在最短通路并联形成的系统电路，所允许的外部电池最大
        二分查找：从所有电池均并联参与起始，利用二分查找快速找到能够形成有效的系统并联电路的最大电池数和对应的系统电路
        '''

        def get_bat_shortest_path_dict(path_by_edge,bats_in_circuit):
            # 获取所有电池对应的最短路径
            shortest_path_dict = {}
            for bat in bats_in_circuit:
                path_contain_bat = [path for path in path_by_edge if bat in path]
                bats_in_paths = [len([edge for edge in path if edge<self.num_bats]) for path in path_contain_bat]
                score_of_path = [bats_in_paths[i]*100+len(path_contain_bat[i])-bats_in_paths[i] for i in range(len(path_contain_bat))]
                shortest_path_dict[bat] = path_contain_bat[score_of_path.index(min(score_of_path))]
            return shortest_path_dict

        def calculate_cur_of_paths(G,path_selected,terminal,num_bats):
            '''
            计算由选中的所有通路并联形成的系统电路所允许的最大电流
            首先，根据所选通路构造新的系统电路图(所有开关均为闭合状态)
            其次，判断系统电路中是否存在导致电池被短路以及全是开关的通路
                注意:多个有效通路并联可能会重新导致某些电池短路或全是开关的通路
            最后,将系统电路图中的每条边通过的电流作为待求解量,构造矩阵求解
                每个非系统端点的顶点，其流入电流和=流出电流和
                根据每条通路计算得到的系统两端电压应相等
                假设其中一条边上的电流为1
                按照电池最大允许电流为1, 对电流计算结果进行缩放
            '''
            # 重新构建系统电路图
            edges_selected = [edge for path in path_selected for edge in path]
            edges_selected = set(edges_selected)
            circuit_G, edge_terminal_dict_,bats_in_circuit_,suc_edge_of_node_,pre_edge_of_node_ = self.build_subG(G,edges_selected)
            # 判断系统电路中是否存在导致电池被短路以及全是开关的通路(认为：所有开关均为闭合状态)
            # 以原系统电路的nodes_of_series_bats_in_graph作为短路电路判断参考

            paths_by_edge = []
            for path in nx.all_simple_edge_paths(circuit_G,*terminal):
                path_by_edge_ = [edge_label for source, target, edge_label in path]
                if all(edge_ >= num_bats for edge_ in path_by_edge_):
                    # 存在全是开关的通路
                    paths_by_edge = []
                    break
                else:
                    if self.sc_judge(path_by_edge_,nodes_of_series_bats_in_graph,edge_terminal_dict_):
                        # 该通路会导致其他电池直接短路
                        paths_by_edge = []
                        break
                    else:
                        paths_by_edge = paths_by_edge + [path_by_edge_]
            # 计算有效系统电路的最大允许电流
            if len(paths_by_edge) == 0:
                cur = -1
            else:
                # 构造矩阵AX=B，求解电流X
                edge_in_circuit = [attr['edge_label'] for source,target,attr in circuit_G.edges(data=True)]
                A = []
                # 基于每个节点的电流出入和为0
                for node in circuit_G.nodes:
                    if node not in terminal:
                        a = [0 for edge in edge_in_circuit]
                        for edge_ in pre_edge_of_node_[node]:
                            a[edge_in_circuit.index(edge_)] = 1
                        for edge_ in suc_edge_of_node_[node]:
                            a[edge_in_circuit.index(edge_)] = -1
                        A.append(a)
                # 基于所有通路两端的电压相等
                for path in paths_by_edge[1:]:
                    a = [0 for edge in edge_in_circuit]
                    for edge in path:
                        if edge < self.num_bats:
                            a[edge_in_circuit.index(edge)] = 1
                    for edge in paths_by_edge[0]:
                        if edge < self.num_bats:
                            a[edge_in_circuit.index(edge)] = a[edge_in_circuit.index(edge)] - 1
                    A.append(a)
                # 假定第一条边的电流为1 
                a = [0 for edge in edge_in_circuit]; a[0] = 1; A.append(a)
                A = np.asarray(A)
                B = np.zeros(A.shape[0]); B[-1] = 1
                cur_of_edge = np.linalg.pinv(A).dot(B)
                cur_of_bat = [cur_of_edge[edge_in_circuit.index(edge_)] for edge_ in edge_in_circuit if edge_<self.num_bats]
                cur_of_edge = cur_of_edge/np.max(cur_of_bat)
                cur4out = [cur_of_edge[edge_in_circuit.index(edge_)] for edge_ in pre_edge_of_node_[terminal[-1]]]
                # print('cur_of_edge---',cur_of_edge)
                # print('cur_of_bat---',cur_of_bat)
                # print('cur4out---',cur4out)
                # print('path_selected---',path_selected)
                cur = sum(cur4out)/self.num_bats
                if cur > 2:
                    cur = -10
            return cur

        def calculate_cur_under_nums(G,terminal,num_bats,num_cur_dict,shortest_paths):
            '''
            计算给定电池数量下构造的系统电路所能允许的最大电流
            简化策略: 以第一次构造出的有效系统电路算出的电流值为结果
            '''
            if num_bats in num_cur_dict:
                return num_cur_dict
            else:
                for path_selected in combinations(shortest_paths,num_bats):
                    cur = calculate_cur_of_paths(G,path_selected,terminal,num_bats)
                    num_cur_dict[num_bats] = cur
                    if cur > 0:
                        break
            return num_cur_dict

        def binary_search(G,terminal,l_num_bats,c_num_bats,r_num_bats,num_cur_dict,shortest_paths):
            num_cur_dict = calculate_cur_under_nums(G,terminal,c_num_bats,num_cur_dict,shortest_paths)
            if num_cur_dict[c_num_bats] > 0:
                # 当前的电池数下存在有效的系统电路
                if r_num_bats - l_num_bats <= 1:
                    # 电池数最大的情况
                    return num_cur_dict[c_num_bats]
                else:
                    # 电池数往变大的方向更新
                    l_num_bats = c_num_bats
                    c_num_bats = int((l_num_bats+r_num_bats)/2)
                    return binary_search(G,terminal,l_num_bats,c_num_bats,r_num_bats,num_cur_dict,shortest_paths)
            else:
                # 当前的电池数下不存在有效的系统电路
                if c_num_bats <= 1:
                    return -1
                else:
                    if c_num_bats-1 in num_cur_dict.keys():
                        # 当x个电池时可行，而x+1个电池时不可行时，直接给出结果，省去一次X个电池时的重复计算
                        return num_cur_dict[c_num_bats-1]
                    else:
                        r_num_bats = c_num_bats
                        c_num_bats = int((l_num_bats+r_num_bats)/2)
                        return binary_search(G,terminal,l_num_bats,c_num_bats,r_num_bats,num_cur_dict,shortest_paths)

        if any(bat_i not in bats_in_circuit for bat_i in range(self.num_bats)):
            # 存在电池不在有效通路中
            res = -1
        else:
            # 所有电池均在有效通路中
            shortest_paths_dict = get_bat_shortest_path_dict(path_by_edge,bats_in_circuit)
            shortest_paths = list(shortest_paths_dict.values())
            min_num_bats,max_num_bats,current_num_bats,num_cur_dict = 1,self.num_bats,self.num_bats,{}
            res = binary_search(G,terminal,min_num_bats,current_num_bats,max_num_bats,num_cur_dict,shortest_paths)
        return res

    def assign_layer(self,G,terminal):
        # 为图的顶点指定layer以自动画图
        G = nx.MultiDiGraph(G)
        nodepaths = list(nx.all_simple_paths(G,source=terminal[0],target=terminal[1]))
        assigned_node = {}
        for path in nodepaths:
            for i in range(len(path)):
                node = path[i]
                if node in assigned_node.keys():
                    if assigned_node[node] > i+1:
                        assigned_node[node] = i
                        G.nodes[node]['layer'] = i+1
                else:
                    assigned_node[node] = i
                    G.nodes[node]['layer'] = i+1

        for node_,attr in G.nodes(data=True):
            if node_ not in assigned_node.keys():
                G.nodes[node_]['layer'] = 0
                assigned_node[node_] = 0
        return G,terminal

    def build_pos(self,G,terminal):
        '''
        为图G的顶点自定义位置信息, 以便画出与硬件结构相似的图形
        具体规则: 以顶点在不同通路中的顺序值的最大值作为其X坐标
                对于具有相同X的顶点, 按顺序给出其Y坐标

        '''
        subG,paths_by_edge, bats_in_circuit, edge_terminal_dict, suc_edge_of_node = self.remove_extra_edge(G,terminal)
        G = subG
        pos = {}
        nodepaths = list(nx.all_simple_paths(subG,*terminal))
        X = {}
        for path in nodepaths:
            for i in range(len(path)):
                node = path[i]
                if node not in X.keys() or X[node] > i:
                    X[node] = i
        X[terminal[-1]] = max(X.values())+1
        Y = {}
        for i in range(max(X.values())+2):
            nodes = [node for node in X if X[node]==i]
            for i in range(len(nodes)):
                Y[nodes[i]] = i
        for node in X:
            pos[node] = [X[node],Y[node]]
        return subG, pos
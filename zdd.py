#!/usr/bin/env python
# -*- coding: utf-8 -*-

from graphviz import Digraph
import copy
import time

start = time.time()

class Node(object):
    def __init__(self, l, f, parents_pattern=''): #初期化　コンストラクタ
        self.index = str((l,len(levelset[l])))
        self.frontier = f
        self.child = [0]*6 #各パターンへの子ノードへの枝
        self.parents = [parents_pattern] #親への枝(親ノード,パターン)

    def insert(self, l):
        temp_frontier = self.frontier
        if place == 1: #行が１つ上になって左端の場合
            temp_frontier[0] = 0 #左は未処理
        patterns = pattern_dic[(temp_frontier[0], temp_frontier[place])] #左と下の状態から
        for i in patterns[0]: #無しパターン
            # print(i, "なし", end =' ')
            # for parent in self.parents:
                # parent[1].child　枝が伸びてるのが自分だけならparentsを消去
            self.child[i] = falseend.index #o終端に関しては親への枝を書き足さない

        for i in patterns[1]: #有りパターン
            # print(i, "あり", end =' ')
            temp_frontier[0] = direction_dic[i][0] #フロンティアを更新
            temp_frontier[place] = direction_dic[i][1]
            new_frontier = copy.deepcopy(temp_frontier)

            if l == 0: #最後の段
                self.child[i] = trueend.index
                trueend.parents.append((self.index, i))

            else:
                for node in levelset[l]:
                    if Nodes[node].frontier == new_frontier: #同じ条件のものがあれば
                        # print("node有", end =' ')
                        self.child[i] = node.index
                        Nodes[node].parents.append((self.index, i)) #親への枝を追加
                        break
                else: #同じ条件のものがなくbreakしなかった場合
                    new_node = Node(l, new_frontier, (self.index, i))
                    levelset[l].append(new_node.index)
                    Nodes[new_node.index] =  new_node
                    # print("node無", end =' ')
                    self.child[i] = new_node.index

            # print(Nodes)
            # print(levelset)

    def output(self):
        print(self.frontier, self.child, self.parents)

pattern_dic = {( 0, 0): {1:[0,1,2,3,4,5], 0:[]}, #制限無し
               ( 1, 0): {1:[0,2,4], 0:[1,3,5]},  #左が正
               (-1, 0): {1:[1,3,5], 0:[0,2,4]},  #左が負
               ( 0, 1): {1:[0,3,5], 0:[1,2,4]},  #下が正
               ( 0,-1): {1:[1,2,4], 0:[0,3,5]},  #下が負
               ( 1, 1): {1:[0], 0:[1,2,3,4,5]},  #左が正、下が正
               (-1,-1): {1:[1], 0:[0,2,3,4,5]},  #左が負、下が負
               (-1, 1): {1:[3,5], 0:[0,1,2,4]},  #左が負、下が正
               ( 1,-1): {1:[2,4], 0:[0,1,3,5]}}  #左が正、下が負

direction_dic = {0:[ 1, 1], #各配置パターンにおける[左, 上]の正負
                 1:[-1,-1],
                 2:[ 1,-1],
                 3:[-1, 1],
                 4:[-1, 1],
                 5:[ 1,-1]}

energy_dic={0:1, #各配置におけるエネルギー
            1:2,
            2:3,
            3:4,
            4:5,
            5:6}

input =  4 #考えたいgridの一辺の長さ
nodesum = input**2 #node総数

Nodes = {} #indexをキーとしたNodeインスタンスのディクショナリ
levelset = {} #各高さにおけるnode集合
for level in range(nodesum, -2, -1): #-1~nodesumまで
    levelset[level]=[]

root = Node(nodesum, [0]*(input+1))
levelset[nodesum].append(root.index)
Nodes[root.index] =  root

falseend = Node(-1, [0]*(input+1))
levelset[-1].append(falseend.index) #0終端
Nodes[falseend.index] =  falseend

trueend = Node(0, [0]*(input+1))
levelset[0].append(trueend.index) #0終端
Nodes[trueend.index] =  trueend

for level in range(nodesum, 0, -1): #1~nodesumまでの各レベルについて
    # print("レベル",level)
    place = (nodesum - level + 1) % input #左から数えたnode位置
    if place == 0: #右端は割り切れて0になるのでinputに書き換え
        place = input

    for node_index in levelset[level]: #各レベルにあるnodeについて
        # print('\n', node_index)
        node = Nodes[node_index]
        node.insert(level-1)
    # print(levelset,'\n')

del Nodes['(-1, 0)'] #0終端にはparentsを格納していないので除く
del Nodes[str((nodesum, 0))] #根にはparentsを格納していないので除く
Nodes['(0, 0)'].parents.pop(0) #空白が格納されているので除く

Nodes_Energy = {} #Nodes_Energy[node.index][エネルギー合計]=場合の数
Nodes_Energy['(0, 0)'] = {} #初期化
Nodes_Energy['(0, 0)'][0] = 1

for level in range(0, nodesum): #0~nodesumまでの各レベルについて下からエネルギー計算
    for node_index in levelset[level+1]: #次のレベルのノードのNodes_Energyを作成
        Nodes_Energy[node_index] = {}
    for node_index in levelset[level]: #そのレベルに存在するノードについて
        for parent in Nodes[node_index].parents: #各parentについて
            for energysum in Nodes_Energy[node_index]: #各energysumについて
                new_energysum = energysum + energy_dic[parent[1]]
                if new_energysum in Nodes_Energy[parent[0]]: #new_energysumがparentsに存在したら
                    Nodes_Energy[parent[0]][new_energysum] += Nodes_Energy[node_index][energysum]
                else:
                    Nodes_Energy[parent[0]][new_energysum] = Nodes_Energy[node_index][energysum]
    for node_index in levelset[level]:
        del Nodes_Energy[node_index]
    # print("えなじー",Nodes_Energy)
sum = 0
for energysum in Nodes_Energy[root.index]:
    print(energysum, Nodes_Energy[root.index][energysum])
    sum += Nodes_Energy[root.index][energysum]
print("配置総数は", sum)

elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

# G = Digraph(format='png') #Graphviz
# G.attr('node', shape='circle')
#
# for node_index in Nodes:
#     G.node(node_index)
#     temp_parents = Nodes[node_index].parents
#     for parent in temp_parents:
#         G.edge(parent[0], node_index, label = str(parent[1]))
#
# # print(G)# print()するとdot形式で出力される
# G.render('tree') #tree.pngで保存
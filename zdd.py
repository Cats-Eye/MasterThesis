##!/usr/bin/env python
# -*- coding: utf-8 -*-

from graphviz import Digraph
import copy
import time
import sys

start = time.time()

class Node(object):
    count = 0
    def __init__(self, l, fl, parents_pattern=''): #初期化　コンストラクタ
        self.index = str((l,len(levelset[l])))
        self.flabel = fl
        self.child = [0]*6 #各パターンへの子ノードへの枝
        self.parents = [parents_pattern] #親への枝(親ノード,パターン)

    def insert(self, l):
        temp_frontier = frontier_generate(self.flabel)
        if place == 1: #行が１つ上になって左端の場合
            temp_frontier[0] = 0 #左は未処理
        if l >= nodesum-input: #最下段の場合
            temp_frontier[place] = 0 #下は未処理
            print(self.index)
        patterns = pattern_dic[(temp_frontier[0], temp_frontier[place])] #左と下の状態から
        for i in patterns[0]: #無しパターン
            # print(i, "なし", end =' ')
            # for parent in self.parents:
                # parent[1].child　枝が伸びてるのが自分だけならparentsを消去
            self.child[i] = falseend.index #o終端に関しては親への枝を書き足さない

        for i in patterns[1]: #有りパターン
            Node.count += 1
            temp_frontier[0] = direction_dic[i][0] #フロンティアを更新
            temp_frontier[place] = direction_dic[i][1]
            # new_frontier = copy.deepcopy(temp_frontier)
            label = label_generate(temp_frontier)

            if l == 0: #最後の段
                self.child[i] = trueend.index #1終端につなぐ
                trueend.parents.append((self.index, i))

            else:
                if label in frontierset:
                    same_node = Nodes[frontierset[label]]
                    self.child[i] = frontierset[label]
                    same_node.parents.append((self.index, i)) #親への枝を追加
                else: #同じfrontierをもつnodeがない
                    new_node = Node(l, label, (self.index, i))
                    levelset[l].append(new_node.index)
                    frontierset[label] = new_node.index
                    Nodes[new_node.index] =  new_node
                    self.child[i] = new_node.index

def label_generate(frontier_g):#2進数によるラベル生成関数
    label_g = 0
    for i in range(0,input+1):#frontierについてラベル付け
        if frontier_g[i] == 1:
            label_g += (2**i)*1#ただし逆順で計算しているので注意
        else:
            label_g += (2**i)*0
    return(label_g)

def frontier_generate(label_g):#frontier生成関数
    frontier_g = [0]*(input+1)
    for i in range(0,input+1):
        if label_g % 2 == 0: # [0, 1]が[-1, 1]に対応
            frontier_g[i] = -1
        else:
            frontier_g[i] = 1
        label_g = label_g // 2
    return(frontier_g)

# 対象ノードの(左, 下)の状態からみて可能なパターン
# 0は方向未処理、1は正方向、-1は負方向
pattern_dic = {( 0, 0): {1:[0,1,2,3,4,5], 0:[]}, #制限無し
               ( 1, 0): {1:[0,2,4], 0:[1,3,5]},  #左が正
               (-1, 0): {1:[1,3,5], 0:[0,2,4]},  #左が負
               ( 0, 1): {1:[0,3,5], 0:[1,2,4]},  #下が正
               ( 0,-1): {1:[1,2,4], 0:[0,3,5]},  #下が負
               ( 1, 1): {1:[0], 0:[1,2,3,4,5]},  #左が正、下が正
               (-1,-1): {1:[1], 0:[0,2,3,4,5]},  #左が負、下が負
               (-1, 1): {1:[3,5], 0:[0,1,2,4]},  #左が負、下が正
               ( 1,-1): {1:[2,4], 0:[0,1,3,5]}}  #左が正、下が負

direction_dic = {0:[ 1, 1], #0~5の配置パターンにおける[右, 上]の正負
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

input = 2 #考えたいgridの一辺の長さ
nodesum = input**2 #node総数

Nodes = {} #indexをキーとしたNodeインスタンスのディクショナリ
levelset = {} #各高さにおけるnode集合
for level in range(nodesum, -2, -1): #-1~nodesumまで
    levelset[level]=[]

root = Node(nodesum, 0) #根頂点
levelset[nodesum].append(root.index)
Nodes[root.index] =  root

falseend = Node(-1, 0) #0終端
levelset[-1].append(falseend.index)
Nodes[falseend.index] =  falseend

trueend = Node(0, 0) #1終端
levelset[0].append(trueend.index)
Nodes[trueend.index] =  trueend

for level in range(nodesum, 0, -1): #1~nodesumまでの各レベルについて
    place = (nodesum - level + 1) % input #左から数えたnode位置
    frontierset = {} #各frontierにおけるnode集合
    if place == 0: #右端は割り切れて0になるのでinputに書き換え
        place = input

    for node_index in levelset[level]: #各レベルにあるnodeについて
        node = Nodes[node_index]
        node.insert(level-1) #１つ下のレベルにnodeを作成

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

sum = 0
f = open('result.txt', 'w')

for energysum in Nodes_Energy[root.index]: #配置パターン総数を求める
    # f.write(str(energysum) + " " +str(Nodes_Energy[root.index][energysum]) + "\n")
    sum += Nodes_Energy[root.index][energysum]

elapsed_time = time.time() - start

f.write("input" + str(input) + "の配置総数は" + str(sum) + "\n")
f.write("ノード総数は" + str(len(Nodes)) + "\n")
f.write("ループは" + str(Node.count) + "\n" + "ラベル生成は" + str(Node.count*(input+1)) + "\n")
f.write("elapsed_time:{0}".format(elapsed_time) + "[sec]")
f.close()

G = Digraph(format='png') #Graphviz
G.attr('node', shape='circle')

for node_index in Nodes:
    G.node(node_index)
    temp_parents = Nodes[node_index].parents
    for parent in temp_parents:
        G.edge(parent[0], node_index, label = str(parent[1]))

# print(G) #dot形式で出力
G.render('tree') #tree.pngで保存

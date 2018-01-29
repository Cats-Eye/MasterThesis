##!/usr/bin/env python
# -*- coding: utf-8 -*-

# from graphviz import Digraph
import copy
import time

start = time.time()

input = 14 #考えたいgridの一辺の長さ

class Node(object):
    # count = 0
    def __init__(self, l, fl, parents_pattern=''): #初期化　コンストラクタ
        self.flabel = fl #ビット化したfrontier
        self.child = [0]*6 #各パターンへの子ノードへの枝
        self.parents = [parents_pattern] #親への枝(親ノード,パターン)

    def insert(self, l):
        temp_label = self.flabel #次に渡すラベル準備
        temp_label = temp_label & musk[0] #0(nodeの左)をマスク
        temp_label = temp_label & musk[place] #place(nodeの下)をマスク

        if l >= nodesum-input: #最下段の場合、place(nodeの下)は未処理(-1)
            if place == 1: #行が１つ上になって左端の場合、0(nodeの左)は未処理(-1)
                patterns = pattern_dic[(-1,-1)]
            else:
                patterns = pattern_dic[(self.flabel & 1,-1)]
        else:
            if place == 1: #行が１つ上になって左端の場合、0(nodeの左)は未処理(-1)
                patterns = pattern_dic[(-1, (self.flabel >> place) & 1)]
            else:
                patterns = pattern_dic[(self.flabel & 1, (self.flabel >> place) & 1)]

        # for i in patterns[0]: #無しパターン
            # self.child[i] = falseend #o終端に関しては親への枝を書き足さない

        for i in patterns[1]: #有りパターン
            # Node.count += 1
            new_label = temp_label
            if direction_dic[i][0] == 1: #ラベルを更新
                new_label += 1
            if direction_dic[i][1] == 1:
                new_label += (1 << place)

            if l == 0: #最後の段
                self.child[i] = trueend #1終端につなぐ
                trueend.parents.append((self, i))

            else:
                if new_label in frontierset: #同じfrontierのnodeがあれば
                    same_node = frontierset[new_label]
                    self.child[i] = frontierset[new_label] #そのnodeに子供の枝を追加
                    same_node.parents.append((self, i)) #そのnodeの親への枝を追加
                else: #同じfrontierをもつnodeがない
                    new_node = Node(l, new_label, (self, i)) #新しくnodeを作る
                    levelset[l].append(new_node)
                    frontierset[new_label] = new_node
                    self.child[i] = new_node

# 対象ノードの(左, 下)の状態からみて可能なパターン
# -1は方向未処理、0は負方向、1は正方向
pattern_dic = {(-1,-1): {1:[0,1,2,3,4,5], 0:[]}, #制限無し
               ( 1,-1): {1:[0,2,4], 0:[1,3,5]},  #左が正
               ( 0,-1): {1:[1,3,5], 0:[0,2,4]},  #左が負
               (-1, 1): {1:[0,3,5], 0:[1,2,4]},  #下が正
               (-1, 0): {1:[1,2,4], 0:[0,3,5]},  #下が負
               ( 1, 1): {1:[0], 0:[1,2,3,4,5]},  #左が正、下が正
               ( 0, 0): {1:[1], 0:[0,2,3,4,5]},  #左が負、下が負
               ( 0, 1): {1:[3,5], 0:[0,1,2,4]},  #左が負、下が正
               ( 1, 0): {1:[2,4], 0:[0,1,3,5]}}  #左が正、下が負

direction_dic = {0:[ 1, 1], #0~5の配置パターンにおける[右, 上]の正負
                 1:[ 0, 0],
                 2:[ 1, 0],
                 3:[ 0, 1],
                 4:[ 0, 1],
                 5:[ 1, 0]}

energy_dic={0:1, #各配置におけるエネルギー
            1:2,
            2:3,
            3:4,
            4:5,
            5:6}

nodesum = input**2 #node総数
bit = 0
for i in range(input+1):
    bit = bit | (1 << i)
musk = [] #ビット演算マスク用
for i in range(input+1):
    musk.append(bit - (1 << i))

levelset = {} #各高さにおけるnode集合
for level in range(nodesum, -2, -1): #-1~nodesumまで
    levelset[level]=[]

root = Node(nodesum, 0) #根頂点
levelset[nodesum].append(root)

falseend = Node(-1, 0) #0終端
levelset[-1].append(falseend)

trueend = Node(0, 0) #1終端
levelset[0].append(trueend)

for level in range(nodesum, 0, -1): #1~nodesumまでの各レベルについて
    place = (nodesum - level + 1) % input #左から数えたnode位置
    frontierset = {} #各frontierにおけるnode集合
    if place == 0: #右端は割り切れて0になるのでinputに書き換え
        place = input

    for node in levelset[level]: #各レベルにあるnodeについて
        node.insert(level-1) #１つ下のレベルにnodeを作成

end1 = time.time()
zdd_time = end1 - start

trueend.parents.pop(0) #空白が格納されているので除く

Nodes_Energy = {} #Nodes_Energy[node][エネルギー合計]=場合の数
Nodes_Energy[trueend] = {} #初期化
Nodes_Energy[trueend][0] = 1

for level in range(0, nodesum): #0~nodesumまでの各レベルについて下からエネルギー計算
    for node in levelset[level+1]: #次のレベルのノードのNodes_Energyを作成
        Nodes_Energy[node] = {}
    for node in levelset[level]: #そのレベルに存在するノードについて
        for parent in node.parents: #各parentについて
            for energysum in Nodes_Energy[node]: #各energysumについて
                new_energysum = energysum + energy_dic[parent[1]]
                if new_energysum in Nodes_Energy[parent[0]]: #new_energysumがparentsに存在したら
                    Nodes_Energy[parent[0]][new_energysum] += Nodes_Energy[node][energysum]
                else:
                    Nodes_Energy[parent[0]][new_energysum] = Nodes_Energy[node][energysum]
    for node in levelset[level]:
        del Nodes_Energy[node]

dp_time = time.time() - end1

znodesum = 0 #zddのノード総数
for level in range(0, nodesum):
    for node in levelset[level]: #そのレベルに存在するノードについて
        znodesum += 1

sum = 0
f = open('newzddresult.txt', 'w')

for energysum in Nodes_Energy[root]: #配置パターン総数を求める
    sum += Nodes_Energy[root][energysum]

elapsed_time = time.time() - start

f.write("input" + str(input) + "の配置総数は" + str(sum) + "\n")
f.write("ノード総数は" + str(znodesum) + "\n")
# f.write("ループは" + str(Node.count) + "\n" + "ラベル生成は" + str(Node.count*(input+1)) + "\n")
f.write("zdd_time {0}".format(zdd_time) + "[sec]" + "\n")
f.write("dp_time {0}".format(dp_time) + "[sec]")

for energysum in Nodes_Energy[root]: #配置パターン総数を求める
    f.write(str(energysum) + " " +str(Nodes_Energy[root][energysum]) + "\n")

f.close()

# G = Digraph(format='png') #Graphviz
# G.attr('node', shape='circle')
#
# for node in Nodes:
#     G.node(node_index)
#     temp_parents = Nodes[node_index].parents
#     for parent in temp_parents:
#         G.edge(parent[0], node_index, label = str(parent[1]))
#
# # print(G) #dot形式で出力
# G.render('tree') #tree.pngで保存

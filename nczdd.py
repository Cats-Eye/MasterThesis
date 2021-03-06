##!/usr/bin/env python
# -*- coding: utf-8 -*-

# from graphviz import Digraph
import copy
import time

start = time.time()

input = 22 #考えたいgridの一辺の長さ

class Node(object):
    # count = 0
    def __init__(self, l, fl, parents_pattern=''): #初期化　コンストラクタ
        self.index = str((l,len(levelset[l]))) #(level,level内ラベリング)というnode固有インデックス
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

        for i in patterns[0]: #無しパターン
            # print(i, "なし", end =' ')
            # for parent in self.parents:
                # parent[1].child　枝が伸びてるのが自分だけならparentsを消去
            self.child[i] = falseend.index #o終端に関しては親への枝を書き足さない

        for i in patterns[1]: #有りパターン
            # Node.count += 1
            new_label = temp_label
            if direction_dic[i][0] == 1: #ラベルを更新
                new_label += 1
            if direction_dic[i][1] == 1:
                new_label += (1 << place)

            if l == 0: #最後の段
                self.child[i] = trueend.index #1終端につなぐ
                trueend.parents.append((self.index, i))

            else:
                if new_label in frontierset: #同じfrontierのnodeがあれば
                    same_node = Nodes[frontierset[new_label]]
                    self.child[i] = frontierset[new_label] #そのnodeに子供の枝を追加
                    same_node.parents.append((self.index, i)) #そのnodeの親への枝を追加
                else: #同じfrontierをもつnodeがない
                    new_node = Node(l, new_label, (self.index, i)) #新しくnodeを作る
                    levelset[l].append(new_node.index)
                    frontierset[new_label] = new_node.index
                    Nodes[new_node.index] =  new_node
                    self.child[i] = new_node.index

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

energy_dic={0:0, #各配置におけるエネルギー
            1:0,
            2:0,
            3:0,
            4:0,
            5:0}

nodesum = input**2 #node総数
bit = 0
for i in range(input+1):
    bit = bit | (1 << i)
musk = [] #ビット演算マスク用
for i in range(input+1):
    musk.append(bit - (1 << i))

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

end1 = time.time()
zdd_time = end1 - start

del Nodes[falseend.index] #0終端にはparentsを格納していないので除く
del Nodes[root.index] #根にはparentsを格納していないので除く
Nodes[trueend.index].parents.pop(0) #空白が格納されているので除く

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

dp_time = time.time() - end1

sum = 0
f = open('zddresult.txt', 'w')

for energysum in Nodes_Energy[root.index]: #配置パターン総数を求める
    f.write(str(energysum) + " " +str(Nodes_Energy[root.index][energysum]) + "\n")
    sum += Nodes_Energy[root.index][energysum]

f.write("input" + str(input) + "の配置総数は" + str(sum) + "\n")
f.write("ノード総数は" + str(len(Nodes)) + "\n")
# f.write("ループは" + str(Node.count) + "\n" + "ラベル生成は" + str(Node.count*(input+1)) + "\n")
f.write("zdd_time {0}".format(zdd_time) + "[sec]" + "\n")
f.write("dp_time {0}".format(dp_time) + "[sec]")
f.write("dp時間計測方法変更")
f.close()

# G = Digraph(format='png') #Graphviz
# G.attr('node', shape='circle')
#
# for node_index in Nodes:
#     G.node(node_index)
#     temp_parents = Nodes[node_index].parents
#     for parent in temp_parents:
#         G.edge(parent[0], node_index, label = str(parent[1]))
#
# # print(G) #dot形式で出力
# G.render('tree') #tree.pngで保存

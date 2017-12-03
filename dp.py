import copy

def org_grid_2d_graph(nodesum, periodic=False, create_using=None): #重み付き二次元格子グラフの生成関数
    G=nx.Graph()
    G.name="grid_2d_graph"
    G.add_nodes_from(i for i in range(nodesum+1))
    return G

def label_generate(temp_edge_g, input_g):#ラベル生成関数
    label_g = 0
    for i in range(0,input_g+1):#フロンティアについてラベル付け
        if temp_edge_g[i] == 1:
            label_g = label_g + (2**i)*1#ただし逆順で計算しているので注意
        else:
            label_g = label_g + (2**i)*0
    return(label_g)

def newfrontier_generate(label_g, temp_energysum_g, temp_edge_g, newfrontier_g, frontier_g):#フロンティア生成関数
    if label_g in newfrontier_g:
        if temp_energysum_g in newfrontier_g[label_g]:
            newfrontier_g[label_g][temp_energysum_g]['count'] = newfrontier_g[label_g][temp_energysum_g]['count'] + frontier_g[key1][key]['count']
        else:
            newfrontier_g.setdefault(label_g, {}).setdefault(temp_energysum_g, {}).setdefault('edge', copy.deepcopy(temp_edge))#フロンティアの辺の向き
            newfrontier_g.setdefault(label_g, {}).setdefault(temp_energysum_g, {}).setdefault('count', frontier_g[key1][key]['count'])#場合の数
    else:
        newfrontier_g.setdefault(label_g, {}).setdefault(temp_energysum_g, {}).setdefault('edge', copy.deepcopy(temp_edge))#フロンティアの辺の向き
        newfrontier_g.setdefault(label_g, {}).setdefault(temp_energysum_g, {}).setdefault('count', frontier_g[key1][key]['count'])#場合の数
    return(0)

class Frontier(object):
    def __init__(self, l, f, n, e, np): #初期化　コンストラクタ
        self.index = l #フロンティアのラベル
        self.frontier = f
        self.number = n #個数
        self.energysum = e #エネルギー合計
        self.nodepattern = np #各パターンの個数

    def output(self):
        print(self.index, self.frontier, self.number, self.energysum, self.nodepattern)

    def insert(self, l):
        temp_frontier = self.frontier
        if place == 1: #行が１つ上になって左端の場合
            temp_frontier[0] = 0 #左は未処理
        patterns = pattern_dic[(temp_frontier[0], temp_frontier[place])] #左と下の状態から
        for i in patterns[0]: #無しパターン
            print(i, "なし", end =' ')
            # for parent in self.parents:
                # parent[1].child　枝が伸びてるのが自分だけならparentsを消去
            self.child[i] = falseend.index #o終端に関しては親への枝を書き足さない

        for i in patterns[1]: #有りパターン
            print(i, "あり", end =' ')
            temp_frontier[0] = direction_dic[i][0] #フロンティアを更新
            temp_frontier[place] = direction_dic[i][1]
            new_frontier = copy.deepcopy(temp_frontier)

            if l == 0: #最後の段
                self.child[i] = trueend.index
                trueend.parents.append((self.index, i))

            else:
                for node in levelset[l]:
                    if Nodes[node].frontier == new_frontier: #同じ条件のものがあれば
                        print("node有", end =' ')
                        self.child[i] = node.index
                        Nodes[node].parents.append((self.index, i)) #親への枝を追加
                        break
                else: #同じ条件のものがなくbreakしなかった場合
                    new_node = Node(l, new_frontier, (self.index, i))
                    levelset[l].append(new_node.index)
                    Nodes[new_node.index] =  new_node
                    print("node無", end =' ')
                    self.child[i] = new_node.index

input =  3 #考えたいgridの一辺の長さ
nodesum = input**2 #node総数

Frontiers={} #indexをキーとしたFrontierインスタンスのディクショナリ
NewFrontiers={} #indexをキーとしたFrontierインスタンスの新しいディクショナリ

pattern_dic = {( 0, 0): [0,1,2,3,4,5]}, #制限無し
               ( 1, 0): [0,2,4]},  #左が正
               (-1, 0): [1,3,5]},  #左が負
               ( 0, 1): {1:[0,3,5], 0:[1,2,4]},  #下が正
               ( 0,-1): {1:[1,2,4], 0:[0,3,5]},  #下が負
               ( 1, 1): {1:[0], 0:[1,2,3,4,5]},  #左が正、下が正
               (-1,-1): {1:[1], 0:[0,2,3,4,5]},  #左が負、下が負
               (-1, 1): {1:[3,5], 0:[0,1,2,4]},  #左が負、下が正
               ( 1,-1): {1:[2,5], 0:[0,1,3,4]}}  #左が正、下が負

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

first_frontier = Frontier(0, 1, 0, [0]*(input+1))
Frontiers[first_frontier.index] =  first_frontier

# print(Frontiers)
# first_frontier.output()




for j in range(1,input+1):#1~n-2まですべての行
    for i in range(1,input+1):#すべての列
        print((i,j))
        print(frontier)
        for key1 in frontier:#すべてのフロンティアについて
            for key in frontier[key1]:
                temp_edge = frontier[key1][key]['edge']#１つのフロンティアについてedgeを取り出す
                temp_edge_energy=[temp_edge[0],temp_edge[i]]
                temp_energysum = key
                weightsum = 0
                if temp_edge[0] == 1:#まず処理済の左と下のweighttsumを求める
                    weightsum += 1
                if temp_edge[i] == 1:
                    weightsum += 1

                if G.edge[(i,j)][(i,j+1)]['weight'] != 0 and G.edge[(i,j)][(i+1,j)]['weight'] != 0: #右も上も処理済
                    print(key,frontier[key1][key]['count'],temp_edge,"右も上も処理済")
                    if G.edge[(i,j)][(i,j+1)]['weight'] == -1:#上は入る矢印
                        weightsum += 1
                    if G.edge[(i,j)][(i+1,j)]['weight'] == -1:#右は入る矢印
                        weightsum += 1
                    if weightsum == 2:#このパターンのみ有
                        temp_edge[i] = G.edge[(i,j)][(i,j+1)]['weight']
                        temp_edge[0] = G.edge[(i,j)][(i+1,j)]['weight']
                        temp_edge_energy.append(temp_edge[0])
                        temp_edge_energy.append(temp_edge[i])
                        energy_label = label_generate(temp_edge_energy,3)
                        temp_energysum = temp_energysum + energy_dic[energy_label]
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_edge, newfrontier, frontier)

                elif G.edge[(i,j)][(i+1,j)]['weight'] != 0: #右が処理済
                    print(key,frontier[key1][key]['count'],temp_edge,"右が処理済")
                    if G.edge[(i,j)][(i+1,j)]['weight'] == -1: #右は入る矢印
                        weightsum += 1
                    if weightsum == 1: #入るのが１本なら
                        temp_edge[i] = -1#上は入る矢印
                        temp_edge[0] = G.edge[(i,j)][(i+1,j)]['weight']
                        temp_edge_energy.append(temp_edge[0])
                        temp_edge_energy.append(temp_edge[i])
                        energy_label = label_generate(temp_edge_energy,3)
                        temp_energysum = temp_energysum + energy_dic[energy_label]
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_edge, newfrontier, frontier)

                    if weightsum == 2: #入るのが2本なら
                        temp_edge[i] = 1#上は出る矢印
                        temp_edge[0] = G.edge[(i,j)][(i+1,j)]['weight']
                        temp_edge_energy.append(temp_edge[0])
                        temp_edge_energy.append(temp_edge[i])
                        energy_label = label_generate(temp_edge_energy,3)
                        temp_energysum = temp_energysum + energy_dic[energy_label]
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_edge, newfrontier, frontier)

                elif G.edge[(i,j)][(i,j+1)]['weight'] != 0: #上が処理済
                    print(key,frontier[key1][key]['count'],temp_edge,"上が処理済")
                    if G.edge[(i,j)][(i,j+1)]['weight'] == -1: #上は入る矢印
                        weightsum += 1

                    if weightsum == 1: #入るのが１本なら
                        temp_edge[i] = G.edge[(i,j)][(i,j+1)]['weight']
                        temp_edge[0] = -1
                        temp_edge_energy.append(temp_edge[0])
                        temp_edge_energy.append(temp_edge[i])
                        energy_label = label_generate(temp_edge_energy,3)
                        temp_energysum = temp_energysum + energy_dic[energy_label]
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_edge, newfrontier, frontier)

                    if weightsum == 2: #入るのが2本なら
                        temp_edge[i] = G.edge[(i,j)][(i,j+1)]['weight']
                        temp_edge[0] = 1#右は出る矢印
                        temp_edge_energy.append(temp_edge[0])
                        temp_edge_energy.append(temp_edge[i])
                        energy_label = label_generate(temp_edge_energy,3)
                        temp_energysum = temp_energysum + energy_dic[energy_label]
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_edge, newfrontier, frontier)

                else: #右も上も未処理
                    if weightsum == 0: #出るのが2本なら
                        print(key,frontier[key1][key]['count'],temp_edge,"右も上も未処理","出るのが２本")
                        temp_edge[i] = -1#上は入る矢印
                        temp_edge[0] = -1#右も入る矢印
                        temp_edge_energy.append(temp_edge[0])
                        temp_edge_energy.append(temp_edge[i])
                        energy_label = label_generate(temp_edge_energy,3)
                        temp_energysum += energy_dic[energy_label]
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_edge, newfrontier, frontier)

                    elif weightsum == 1: #入るのが１本なら２パターン
                        print(key,frontier[key1][key]['count'],temp_edge,"右も上も未処理","入るのが１本で２パターン")
                        temp_edge[i] = -1 #上は入る矢印
                        temp_edge[0] = 1 #右は出る矢印
                        temp_edge_energy.append(temp_edge[0])
                        temp_edge_energy.append(temp_edge[i])
                        energy_label = label_generate(temp_edge_energy,3)
                        temp_energysum += energy_dic[energy_label]
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_edge, newfrontier, frontier)
                        temp_energysum -= energy_dic[energy_label] #初期化
                        temp_edge_energy.pop() #初期化
                        temp_edge_energy.pop() #初期化

                        temp_edge[i] = 1 #上は出る矢印
                        temp_edge[0] = -1 #右は入る矢印
                        temp_edge_energy.append(temp_edge[0])
                        temp_edge_energy.append(temp_edge[i])
                        energy_label = label_generate(temp_edge_energy,3)
                        temp_energysum += energy_dic[energy_label]
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_edge, newfrontier, frontier)

                    else: #weightsum == 2で入るのが2本なら
                        print(key,frontier[key1][key]['count'],temp_edge,"右も上も未処理","入るのが２本")
                        temp_edge[i] = 1 #上は出る矢印
                        temp_edge[0] = 1 #右も出る矢印
                        temp_edge_energy.append(temp_edge[0])
                        temp_edge_energy.append(temp_edge[i])
                        energy_label = label_generate(temp_edge_energy,3)
                        temp_energysum = temp_energysum + energy_dic[energy_label]
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_edge, newfrontier, frontier)

        if i == input:#右端
            print("右端",newfrontier)
            newfrontier2 = {}
            if G.edge[(0,j+1)][(1,j+1)]['weight'] == 0:#次の行の左端が自由端
                print("左端自由端")
                for key1 in newfrontier:#１つのフロンティアにつき２パターン
                    for key in newfrontier[key1]:
                        temp_edge=newfrontier[key1][key]['edge']
                        temp_energysum = key
                        temp_edge[0] = -1
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_edge, newfrontier2, newfrontier)

                        temp_edge[0] = 1
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_edge, newfrontier2, newfrontier)
            else:#処理済
                print("左端処理済")
                for key1 in newfrontier:#１つのフロンティアにつき２パターン
                    for key in newfrontier[key1]:
                        temp_edge=newfrontier[key1][key]['edge']
                        temp_energysum = key
                        temp_edge[0] = G.edge[(0,j+1)][(1,j+1)]['weight']
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_edge, newfrontier2, newfrontier)
            frontier = newfrontier2
        else:
            frontier = newfrontier

        newfrontier={}
        print(" ")
#
# tempcount=0
# count=0
# for key1 in frontier:
#     for key in frontier[key1]:
#         tempcount += frontier[key1][key]['count']
#     count += tempcount
#     tempcount = 0
# print("配置パターン総数は",count)

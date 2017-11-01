import networkx as nx
import matplotlib.pyplot as plt
import copy

def org_grid_2d_graph(m, n, periodic=False, create_using=None): #重み付き二次元格子グラフの生成関数
    G=nx.Graph()
    G.name="grid_2d_graph"
    rows=range(m)
    columns=range(n)
    G.add_nodes_from( (i,j) for i in rows for j in columns )
    G.add_weighted_edges_from( [(i-1,j),(i,j),0] for i in rows for j in columns if i>0 )
    G.add_weighted_edges_from( [(i,j-1),(i,j),0] for i in rows for j in columns if j>0 )
    return G

def label_generate(temp_edge_g, input_g):#ラベル生成関数
    label_g = 0
    for i in range(0,input_g+1):#フロンティアについてラベル付け
        if temp_edge_g[i] == 1:
            label_g = label_g + (2**i)*1#ただし逆順で計算しているので注意
        else:
            label_g = label_g + (2**i)*0
    return(label_g)

def newfrontier_generate(label_g, temp_energysum_g, temp_vertexcount_g, temp_edge_g, newfrontier_g, frontier_g):#フロンティア生成関数
    if label_g in newfrontier_g:
        if temp_energysum_g in newfrontier_g[label_g]:
            if temp_vertexcount_g == newfrontier_g[label_g][temp_energysum_g]['vertexcount']:
                newfrontier_g[label_g][temp_energysum_g]['count'] += frontier_g[key1][key]['count']
            else:
                newfrontier_g.setdefault(label_g, {}).setdefault(temp_energysum_g, {}).setdefault('edge', copy.deepcopy(temp_edge))#フロンティアの辺の向き
                newfrontier_g.setdefault(label_g, {}).setdefault(temp_energysum_g, {}).setdefault('count', frontier_g[key1][key]['count'])#場合の数
                newfrontier_g.setdefault(label_g, {}).setdefault(temp_energysum_g, {}).setdefault('vertexcount', copy.deepcopy(temp_vertexcount))
        else:
            newfrontier_g.setdefault(label_g, {}).setdefault(temp_energysum_g, {}).setdefault('edge', copy.deepcopy(temp_edge))#フロンティアの辺の向き
            newfrontier_g.setdefault(label_g, {}).setdefault(temp_energysum_g, {}).setdefault('count', frontier_g[key1][key]['count'])#場合の数
            newfrontier_g.setdefault(label_g, {}).setdefault(temp_energysum_g, {}).setdefault('vertexcount', copy.deepcopy(temp_vertexcount))
    else:
        newfrontier_g.setdefault(label_g, {}).setdefault(temp_energysum_g, {}).setdefault('edge', copy.deepcopy(temp_edge))#フロンティアの辺の向き
        newfrontier_g.setdefault(label_g, {}).setdefault(temp_energysum_g, {}).setdefault('count', frontier_g[key1][key]['count'])#場合の数
        newfrontier_g.setdefault(label_g, {}).setdefault(temp_energysum_g, {}).setdefault('vertexcount', copy.deepcopy(temp_vertexcount))

input =  3 #考えたいgridの一辺の長さ
n = input + 2 #それに２を足す
G = org_grid_2d_graph(n, n)

pos= dict((n, n) for n in G.nodes()) #ノード名を座標に指定し描画位置を固定

edge_labels = {} #処理済判定可視化ラベル

for (s,t) in G.nodes_iter(): #端のノードを赤に
    if s == 0 or s == n-1 or t == 0 or t == n-1:
        G.node[(s, t)]['color'] = 'r'
    else:
        G.node[(s, t)]['color'] = 'yellow' #他は黄に

for ((s,t),(p,q)) in G.edges_iter(): #端のノードに隣接するエッジのweightを１にしてとりあえずデフォの方向に
    if s == 0 or t == 0 or p == n-1 or q == n-1:
        G.edge[(s,t)][(p,q)]['weight'] = 1
    else: #他のedgeは0で未設定で
        G.edge[(s,t)][(p,q)]['weight'] = 0


G.edge[(0,3)][(1,3)]['weight'] = -1 #3*3グリッド
G.edge[(0,2)][(1,2)]['weight'] = -1
G.edge[(0,1)][(1,1)]['weight'] = 0

G.edge[(1,0)][(1,1)]['weight'] = -1
G.edge[(2,0)][(2,1)]['weight'] = -1
G.edge[(3,0)][(3,1)]['weight'] = 0

G.edge[(3,1)][(4,1)]['weight'] = 0
G.edge[(3,2)][(4,2)]['weight'] = -1
G.edge[(3,3)][(4,3)]['weight'] = 0

G.edge[(3,3)][(3,4)]['weight'] = -1
G.edge[(2,3)][(2,4)]['weight'] = -1
G.edge[(1,3)][(1,4)]['weight'] = -1

vertexcount={15:0,0:0,5:0,10:0,9:0,6:0}

energy_dic={15:1, #パターン１[1 1 1 1] #格子点におけるエネルギー
             0:2, #パターン２[0 0 0 0]
             5:3, #パターン３[1 0 1 0]
            10:4, #パターン４[0 1 0 1]
             9:5, #パターン５[1 0 0 1]
             6:6} #パターン６[0 1 1 0]

temp_edge=[]
temp_energysum=0
temp_vertexcount=[]
temp_edge_energy=[]
label=0
weightsum = 0
energy_label = 0
frontier={}
newfrontier={}

if G.edge[(0,1)][(1,1)]['weight'] != 0: #左端が決まっている
    temp_edge.append(G.edge[(0,1)][(1,1)]['weight'])
    label=G.edge[(0,1)][(1,1)]['weight']
    frontier.setdefault(label, {}).setdefault(0, {}).setdefault('edge', copy.deepcopy(temp_edge))
else:#決まってない
    temp_edge.append(1)
    frontier.setdefault(1, {}).setdefault(0, {}).setdefault('edge', copy.deepcopy(temp_edge))
    temp_edge[0]=-1
    frontier.setdefault(0, {}).setdefault(0, {}).setdefault('edge', copy.deepcopy(temp_edge))

for i in range(1,input+1):
    for key in frontier:
        temp_edge=frontier[key][0]['edge']
        if G.edge[(i,0)][(i,1)]['weight'] != 0:
            temp_edge.append(G.edge[(i,0)][(i,1)]['weight'])
            label=label_generate(temp_edge,i)
            newfrontier.setdefault(label, {}).setdefault(0, {}).setdefault('edge', copy.deepcopy(temp_edge))
        else:
            temp_edge.append(1)
            label=label_generate(temp_edge,i)
            newfrontier.setdefault(label, {}).setdefault(0, {}).setdefault('edge', copy.deepcopy(temp_edge))
            temp_edge[i]=-1
            label=label_generate(temp_edge,i)
            newfrontier.setdefault(label, {}).setdefault(0, {}).setdefault('edge', copy.deepcopy(temp_edge))
    frontier = newfrontier
    newfrontier = {}

for key in frontier:
    frontier.setdefault(key, {}).setdefault(0, {}).setdefault('count', 1)#場合の数
    frontier.setdefault(key, {}).setdefault(0, {}).setdefault('vertexcount', copy.deepcopy(vertexcount))#場合の数
print(frontier)

for j in range(1,input+1):#1~n-2まですべての行
    for i in range(1,input+1):#すべての列
        print((i,j))
        # print(frontier)
        for key1 in frontier:#すべてのフロンティアについて
            for key in frontier[key1]:
                temp_edge = frontier[key1][key]['edge']#１つのフロンティアについてedgeを取り出す
                temp_vertexcount = frontier[key1][key]['vertexcount']
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
                        temp_vertexcount[energy_label] += 1
                        temp_energysum += energy_dic[energy_label]
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_vertexcount, temp_edge, newfrontier, frontier)

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
                        temp_vertexcount[energy_label] += 1
                        temp_energysum += energy_dic[energy_label]
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_vertexcount, temp_edge, newfrontier, frontier)

                    if weightsum == 2: #入るのが2本なら
                        temp_edge[i] = 1#上は出る矢印
                        temp_edge[0] = G.edge[(i,j)][(i+1,j)]['weight']
                        temp_edge_energy.append(temp_edge[0])
                        temp_edge_energy.append(temp_edge[i])
                        energy_label = label_generate(temp_edge_energy,3)
                        temp_vertexcount[energy_label] += 1
                        temp_energysum += energy_dic[energy_label]
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_vertexcount, temp_edge, newfrontier, frontier)

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
                        temp_vertexcount[energy_label] += 1
                        temp_energysum += energy_dic[energy_label]
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_vertexcount, temp_edge, newfrontier, frontier)

                    if weightsum == 2: #入るのが2本なら
                        temp_edge[i] = G.edge[(i,j)][(i,j+1)]['weight']
                        temp_edge[0] = 1#右は出る矢印
                        temp_edge_energy.append(temp_edge[0])
                        temp_edge_energy.append(temp_edge[i])
                        energy_label = label_generate(temp_edge_energy,3)
                        temp_vertexcount[energy_label] += 1
                        temp_energysum += energy_dic[energy_label]
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_vertexcount, temp_edge, newfrontier, frontier)

                else: #右も上も未処理
                    if weightsum == 0: #出るのが2本なら
                        print(key,frontier[key1][key]['count'],temp_edge,"右も上も未処理","出るのが２本")
                        temp_edge[i] = -1#上は入る矢印
                        temp_edge[0] = -1#右も入る矢印
                        temp_edge_energy.append(temp_edge[0])
                        temp_edge_energy.append(temp_edge[i])
                        energy_label = label_generate(temp_edge_energy,3)
                        temp_vertexcount[energy_label] += 1
                        temp_energysum += energy_dic[energy_label]
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_vertexcount, temp_edge, newfrontier, frontier)

                    elif weightsum == 1: #入るのが１本なら２パターン
                        print(key,frontier[key1][key]['count'],temp_edge,"右も上も未処理","入るのが１本で２パターン")
                        temp_edge[i] = -1 #上は入る矢印
                        temp_edge[0] = 1 #右は出る矢印
                        temp_edge_energy.append(temp_edge[0])
                        temp_edge_energy.append(temp_edge[i])
                        energy_label = label_generate(temp_edge_energy,3)
                        temp_vertexcount[energy_label] += 1
                        temp_energysum += energy_dic[energy_label]
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_vertexcount, temp_edge, newfrontier, frontier)
                        temp_vertexcount[energy_label] -= 1 #初期化
                        temp_energysum -= energy_dic[energy_label] #初期化
                        temp_edge_energy.pop() #初期化
                        temp_edge_energy.pop() #初期化

                        temp_edge[i] = 1 #上は出る矢印
                        temp_edge[0] = -1 #右は入る矢印
                        temp_edge_energy.append(temp_edge[0])
                        temp_edge_energy.append(temp_edge[i])
                        energy_label = label_generate(temp_edge_energy,3)
                        temp_vertexcount[energy_label] += 1
                        temp_energysum += energy_dic[energy_label]
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_vertexcount, temp_edge, newfrontier, frontier)

                    else: #weightsum == 2で入るのが2本なら
                        print(key,frontier[key1][key]['count'],temp_edge,"右も上も未処理","入るのが２本")
                        temp_edge[i] = 1 #上は出る矢印
                        temp_edge[0] = 1 #右も出る矢印
                        temp_edge_energy.append(temp_edge[0])
                        temp_edge_energy.append(temp_edge[i])
                        energy_label = label_generate(temp_edge_energy,3)
                        temp_vertexcount[energy_label] += 1
                        temp_energysum += energy_dic[energy_label]
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_vertexcount, temp_edge, newfrontier, frontier)

        if i == input:#右端
            print("右端",newfrontier)
            newfrontier2 = {}
            if G.edge[(0,j+1)][(1,j+1)]['weight'] == 0:#次の行の左端が自由端
                print("左端自由端")
                for key1 in newfrontier:#１つのフロンティアにつき２パターン
                    for key in newfrontier[key1]:
                        temp_edge=newfrontier[key1][key]['edge']
                        temp_vertexcount = newfrontier[key1][key]['vertexcount']
                        temp_energysum = key
                        temp_edge[0] = -1
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_vertexcount, temp_edge, newfrontier2, newfrontier)

                        temp_edge[0] = 1
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_vertexcount, temp_edge, newfrontier2, newfrontier)
            else:#処理済
                print("左端処理済")
                for key1 in newfrontier:#１つのフロンティアにつき２パターン
                    for key in newfrontier[key1]:
                        temp_edge=newfrontier[key1][key]['edge']
                        temp_vertexcount = newfrontier[key1][key]['vertexcount']
                        temp_energysum = key
                        temp_edge[0] = G.edge[(0,j+1)][(1,j+1)]['weight']
                        label=label_generate(temp_edge,input)
                        newfrontier_generate(label, temp_energysum, temp_vertexcount, temp_edge, newfrontier2, newfrontier)
            frontier = newfrontier2
        else:
            frontier = newfrontier

        newfrontier={}
        print(" ")

for key in frontier:
    tempcount = {15:0,0:0,5:0,10:0,9:0,6:0}
    for key1 in frontier[key]:
        for key2 in frontier[key][key1]['vertexcount']:
            tempcount[key2] += frontier[key][key1]['vertexcount'][key2] * frontier[key][key1]['count']
    for key3 in tempcount:
        vertexcount[key3] += tempcount[key3]
print("配置パターン総数は",vertexcount)

count=0
for key1 in frontier:
    tempcount2 = 0
    for key in frontier[key1]:
        tempcount2 += frontier[key1][key]['count']
        print(key,tempcount2)
    count += tempcount2
print("配置パターン総数は",count)

for s,t in G.edges_iter(): #描画用処理判定可視化
    edge_labels[s,t] = G.edge[s][t]['weight']

for (s,t) in G.edges_iter(): #処理済は青、未処理は黒
    if G.edge[s][t]['weight'] == 1:
         G.edge[s][t]['color'] = 'blue'
    else:
        G.edge[s][t]['color'] = 'black'

nx.draw_networkx(G, pos, node_color=[G.node[n]['color'] for n in G.nodes_iter()]) #描画
nx.draw_networkx_edge_labels(G, pos, edge_labels)
nx.draw_networkx_edges(G,pos,edge_color= [G.edge[s][t]['color'] for (s,t) in G.edges_iter()])
plt.axis('equal') #x,yの座標値の増分を同量に調整
plt.gca().xaxis.set_visible(False)
plt.gca().yaxis.set_visible(False)
plt.show()

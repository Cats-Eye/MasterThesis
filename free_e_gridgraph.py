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
        # print(i)
        # print(label,"=",label,"+","2^",i,"*",temp_edge[i])
    return(label_g)

def newfrontier_generate(label_g, temp_edge_g, newfrontier_g, frontier_g):#フロンティア生成関数
    if label_g in newfrontier_g:
        newfrontier_g[label_g]['count'] = newfrontier_g[label_g]['count'] + frontier_g[key]['count']
    else:
        newfrontier_g.setdefault(label_g, {})['edge'] = copy.deepcopy(temp_edge_g)#フロンティアの辺の向き
        newfrontier_g.setdefault(label_g, {})['count'] = frontier_g[key]['count']#場合の数
    return(0)

input = 4 #考えたいgridの一辺の長さ
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

# for ((s,t),(p,q)) in G.edges_iter(): #テスト
#     if  p == n-1 or q == n-1:
#         G.edge[(s,t)][(p,q)]['weight'] = 0

# G.edge[(1,0)][(1,1)]['weight'] = -1 #解が２になる小池さんグリッド
# G.edge[(2,0)][(2,1)]['weight'] = -1
# G.edge[(2,1)][(3,1)]['weight'] = -1
# G.edge[(2,2)][(3,2)]['weight'] = -1

# G.edge[(2,0)][(2,1)]['weight'] = -1 #パワポの4*4グリッド
# G.edge[(0,1)][(1,1)]['weight'] = -1
# G.edge[(0,3)][(1,3)]['weight'] = -1
# G.edge[(0,4)][(1,4)]['weight'] = -1
# G.edge[(1,4)][(1,5)]['weight'] = -1
# G.edge[(4,4)][(4,5)]['weight'] = -1
# G.edge[(1,4)][(1,5)]['weight'] = -1
# G.edge[(4,1)][(5,1)]['weight'] = -1
# G.edge[(4,2)][(5,2)]['weight'] = -1

G.edge[(0,4)][(1,4)]['weight'] = 0 #4*4グリッド
G.edge[(0,3)][(1,3)]['weight'] = 0
G.edge[(0,2)][(1,2)]['weight'] = -1
G.edge[(0,1)][(1,1)]['weight'] = -1

# G.edge[(1,0)][(1,1)]['weight'] = 0
G.edge[(2,0)][(2,1)]['weight'] = 0
# G.edge[(3,0)][(3,1)]['weight'] = 0
G.edge[(4,0)][(4,1)]['weight'] = 0

G.edge[(4,1)][(5,1)]['weight'] = -1
G.edge[(4,2)][(5,2)]['weight'] = -1
G.edge[(4,3)][(5,3)]['weight'] = 0
G.edge[(4,4)][(5,4)]['weight'] = -1

G.edge[(4,4)][(4,5)]['weight'] = -1
# G.edge[(3,4)][(3,5)]['weight'] = 0
G.edge[(2,4)][(2,5)]['weight'] = 0
G.edge[(1,4)][(1,5)]['weight'] = 0

# G.edge[(0,3)][(1,3)]['weight'] = -1 #3*3グリッド
# G.edge[(0,2)][(1,2)]['weight'] = -1
# G.edge[(0,1)][(1,1)]['weight'] = -1
#
# G.edge[(1,0)][(1,1)]['weight'] = -1
# G.edge[(2,0)][(2,1)]['weight'] = -1
# G.edge[(3,0)][(3,1)]['weight'] = 0
#
# G.edge[(3,1)][(4,1)]['weight'] = 0
# G.edge[(3,2)][(4,2)]['weight'] = -1
# G.edge[(3,3)][(4,3)]['weight'] = 0
#
# G.edge[(3,3)][(3,4)]['weight'] = -1
# G.edge[(2,3)][(2,4)]['weight'] = -1
# G.edge[(1,3)][(1,4)]['weight'] = -1

temp_edge=[]
label=0
weightsum = 0
frontier={}
newfrontier={}

if G.edge[(0,1)][(1,1)]['weight'] != 0: #右端が決まっている
    temp_edge.append(G.edge[(0,1)][(1,1)]['weight'])
    label=G.edge[(0,1)][(1,1)]['weight']
    frontier.setdefault(label, {})['edge'] = copy.deepcopy(temp_edge)
else:#決まってない
    temp_edge.append(1)
    frontier.setdefault(1, {})['edge'] = copy.deepcopy(temp_edge)
    temp_edge[0]=-1
    frontier.setdefault(0, {})['edge'] = copy.deepcopy(temp_edge)

for i in range(1,input+1):
    for key in frontier:
        temp_edge=frontier[key]['edge']
        if G.edge[(i,0)][(i,1)]['weight'] != 0:
            temp_edge.append(G.edge[(i,0)][(i,1)]['weight'])
            label=label_generate(temp_edge,i)
            newfrontier.setdefault(label, {})['edge'] = copy.deepcopy(temp_edge)
        else:
            temp_edge.append(1)
            label=label_generate(temp_edge,i)
            newfrontier.setdefault(label, {})['edge'] = copy.deepcopy(temp_edge)
            temp_edge[i]=-1
            label=label_generate(temp_edge,i)
            newfrontier.setdefault(label, {})['edge'] = copy.deepcopy(temp_edge)
    frontier = newfrontier
    newfrontier = {}

for key in frontier:
    frontier.setdefault(key, {})['count'] = 1

for j in range(1,input+1):#1~n-2まですべての行
    for i in range(1,input+1):#すべての列
        print((i,j))
        print(frontier)
        for key in frontier:#すべてのフロンティアについて
            temp_edge=frontier[key]['edge']#１つのフロンティアについてedgeを取り出す
            weightsum = 0
            if temp_edge[0] == 1:#まず処理済の左と下のweighttsumを求める
                weightsum += 1
            if temp_edge[i] == 1:
                weightsum += 1

            if G.edge[(i,j)][(i,j+1)]['weight'] != 0 and G.edge[(i,j)][(i+1,j)]['weight'] != 0: #右も上も処理済
                print(temp_edge,"右も上も処理済")
                if G.edge[(i,j)][(i,j+1)]['weight'] == -1:#上は入る矢印
                    weightsum += 1
                if G.edge[(i,j)][(i+1,j)]['weight'] == -1:#右は入る矢印
                    weightsum += 1
                if weightsum == 2:#このパターンのみ有
                    temp_edge[i] = G.edge[(i,j)][(i,j+1)]['weight']
                    temp_edge[0] = G.edge[(i,j)][(i+1,j)]['weight']
                    label=label_generate(temp_edge,input)
                    newfrontier_generate(label, temp_edge, newfrontier, frontier)

            elif G.edge[(i,j)][(i+1,j)]['weight'] != 0: #右が処理済
                print(temp_edge,"右が処理済")
                if G.edge[(i,j)][(i+1,j)]['weight'] == -1: #右は入る矢印
                    weightsum += 1
                if weightsum == 1: #入るのが１本なら
                    temp_edge[i] = -1#上は入る矢印
                    temp_edge[0] = G.edge[(i,j)][(i+1,j)]['weight']
                    label=label_generate(temp_edge,input)
                    newfrontier_generate(label, temp_edge, newfrontier, frontier)

                if weightsum == 2: #入るのが2本なら
                    temp_edge[i] = 1#上は出る矢印
                    temp_edge[0] = G.edge[(i,j)][(i+1,j)]['weight']
                    label=label_generate(temp_edge,input)
                    newfrontier_generate(label, temp_edge, newfrontier, frontier)

            elif G.edge[(i,j)][(i,j+1)]['weight'] != 0: #上が処理済
                print(temp_edge,"上が処理済")
                if G.edge[(i,j)][(i,j+1)]['weight'] == -1: #上は入る矢印
                    weightsum += 1

                if weightsum == 1: #入るのが１本なら
                    temp_edge[i] = G.edge[(i,j)][(i,j+1)]['weight']
                    temp_edge[0] = -1
                    label=label_generate(temp_edge,input)
                    newfrontier_generate(label, temp_edge, newfrontier, frontier)

                if weightsum == 2: #入るのが2本なら
                    temp_edge[i] = G.edge[(i,j)][(i,j+1)]['weight']
                    temp_edge[0] = 1#右は出る矢印
                    label=label_generate(temp_edge,input)
                    newfrontier_generate(label, temp_edge, newfrontier, frontier)

            else: #右も上も未処理
                if weightsum == 0: #出るのが2本なら
                    print(temp_edge,"右も上も未処理","出るのが２本")
                    temp_edge[i] = -1#上は入る矢印
                    temp_edge[0] = -1#右も入る矢印
                    label=label_generate(temp_edge,input)
                    newfrontier_generate(label, temp_edge, newfrontier, frontier)

                elif weightsum == 1: #入るのが１本なら２パターン
                    print(temp_edge,"右も上も未処理","入るのが１本で２パターン")
                    temp_edge[i] = -1 #上は入る矢印
                    temp_edge[0] = 1 #右は出る矢印
                    label=label_generate(temp_edge,input)
                    newfrontier_generate(label, temp_edge, newfrontier, frontier)

                    temp_edge[i] = 1 #上は出る矢印
                    temp_edge[0] = -1 #右は入る矢印
                    label=label_generate(temp_edge,input)
                    newfrontier_generate(label, temp_edge, newfrontier, frontier)

                else: #weightsum == 2で入るのが2本なら
                    print(temp_edge,"右も上も未処理","入るのが２本")
                    temp_edge[i] = 1 #上は出る矢印
                    temp_edge[0] = 1 #右も出る矢印
                    label=label_generate(temp_edge,input)
                    newfrontier_generate(label, temp_edge, newfrontier, frontier)

        if i == input:#右端
            print("右端",newfrontier)
            newfrontier2 = {}
            if G.edge[(0,j+1)][(1,j+1)]['weight'] == 0:#次の行の左端が自由端
                print("左端自由端")
                for key in newfrontier:#１つのフロンティアにつき２パターン
                    temp_edge=newfrontier[key]['edge']
                    temp_edge[0] = -1
                    label=label_generate(temp_edge,input)
                    newfrontier_generate(label, temp_edge, newfrontier2, newfrontier)

                    temp_edge[0] = 1
                    label=label_generate(temp_edge,input)
                    newfrontier_generate(label, temp_edge, newfrontier2, newfrontier)
            else:#処理済
                print("左端処理済")
                for key in newfrontier:
                    temp_edge=newfrontier[key]['edge']#１つのフロンティアについてedgeを取り出す
                    temp_edge[0] = G.edge[(0,j+1)][(1,j+1)]['weight']
                    label=label_generate(temp_edge,input)
                    newfrontier_generate(label, temp_edge, newfrontier2, newfrontier)
            frontier = newfrontier2
        else:
            frontier = newfrontier

        newfrontier={}
        print(" ")

count=0
for key in frontier:
    count = count + frontier[key]['count']
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

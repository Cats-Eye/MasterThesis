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
        label_g = label_g + (2**i)*temp_edge_g[i]#ただし逆順で計算しているので注意
        # print(i)
        # print(label,"=",label,"+","2^",i,"*",temp_edge[i])
    return(label_g)

def newfrontier_generate(label_g, temp_edge_g, newfrontier_g, frontier_g):#フロンティア生成関数
    if label_g in newfrontier_g:
        newfrontier_g[label_g]['count'] = newfrontier_g[label_g]['count'] + frontier_g[key]['count']
    else:
        newfrontier_g.setdefault(label_g, {})['edge'] = copy.deepcopy(temp_edge_g)#フロンティアの辺の向き
        newfrontier.setdefault(label_g, {})['count'] = frontier_g[key]['count']#場合の数
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
    if s == 0 or s == n-1 or t == 0 or t == n-1 or p == 0 or p == n-1 or q == 0 or q == n-1:
        G.edge[(s,t)][(p,q)]['weight'] = 1

# for ((s,t),(p,q)) in G.edges_iter(): #テスト
#     if t == 0 or q == n-1:
#         G.edge[(s,t)][(p,q)]['weight'] = 0

# G.edge[(1,0)][(1,1)]['weight'] = 0 #解が２になる小池さんグリッド
# G.edge[(2,0)][(2,1)]['weight'] = 0
# G.edge[(2,1)][(3,1)]['weight'] = 0
# G.edge[(2,2)][(3,2)]['weight'] = 0

G.edge[(2,0)][(2,1)]['weight'] = 0 #パワポの4*4グリッド
G.edge[(0,1)][(1,1)]['weight'] = 0
G.edge[(0,3)][(1,3)]['weight'] = 0
G.edge[(0,4)][(1,4)]['weight'] = 0
G.edge[(1,4)][(1,5)]['weight'] = 0
G.edge[(4,4)][(4,5)]['weight'] = 0
G.edge[(1,4)][(1,5)]['weight'] = 0
G.edge[(4,1)][(5,1)]['weight'] = 0
G.edge[(4,2)][(5,2)]['weight'] = 0

temp_edge=[]
label=0

temp_edge.append(G.edge[(0,1)][(1,1)]['weight'])#横向き辺を最初に追加
for i in range(1,input+1):#最下段のフロンティアを入力
    temp_edge.append(G.edge[(i,0)][(i,1)]['weight'])
label=label_generate(temp_edge,input)

# energy=0
# energy_dic={15:1, #パターン１[1 1 1 1]
#         0:2,  #パターン２[0 0 0 0]
#         5:3,  #パターン３[1 0 1 0]
#         10:4, #パターン４[0 1 0 1]
#         9:5,  #パターン５[1 0 0 1]
#         6:6}  #パターン６[0 1 1 0]

weightsum = 0
frontier={}
newfrontier={}
frontier.setdefault(label, {})['edge'] = copy.deepcopy(temp_edge)#フロンティアの辺の向き
frontier.setdefault(label, {})['count'] = 1#場合の数

for j in range(1,input+1):#1~n-2まですべての行
    for i in range(1,input+1):#すべての列
        for key in frontier:#すべてのフロンティアについて
            temp_edge=frontier[key]['edge']#１つのフロンティアについてedgeを取り出す
            weightsum = temp_edge[0] + temp_edge[i]#まず処理済の左と下のweighttsumを求める
            print((i,j))
            print(frontier)
            print(temp_edge,"について計算開始")

            if i == input and j == input: #右上端
                print("一番右上端")
                if G.edge[(i,j)][(i,j+1)]['weight'] == 0:#上は入る矢印
                    weightsum += 1
                if G.edge[(i,j)][(i+1,j)]['weight'] == 0:#右は入る矢印
                    weightsum += 1
                if weightsum == 2:#このパターンのみ有
                    temp_edge[i] = G.edge[(i,j)][(i,j+1)]['weight']
                    temp_edge[0] = G.edge[(i,j)][(i+1,j)]['weight']
                    label=label_generate(temp_edge,input)
                    newfrontier_generate(label, temp_edge, newfrontier, frontier)
                    # if label in newfrontier:
                    #     newfrontier[label]['count'] = newfrontier[label]['count'] + frontier[key]['count']
                    # else:
                    #     newfrontier.setdefault(label, {})['edge'] = copy.deepcopy(temp_edge)#フロンティアの辺の向き
                    #     newfrontier.setdefault(label, {})['count'] = frontier[key]['count']#場合の数

            elif i == input: #一番右端の行で右が処理済
                print("一番右端")
                if G.edge[(i,j)][(i+1,j)]['weight'] == 0: #右は入る矢印
                    weightsum += 1
                if weightsum == 1: #入るのが１本なら
                    temp_edge[i] = 0#上は入る矢印
                    temp_edge[0] = G.edge[(0,j+1)][(1,j+1)]['weight']
                    label=label_generate(temp_edge,input)
                    newfrontier_generate(label, temp_edge, newfrontier, frontier)

                if weightsum == 2: #入るのが2本なら
                    temp_edge[i] = 1#上は出る矢印
                    temp_edge[0] = G.edge[(0,j+1)][(1,j+1)]['weight']
                    label=label_generate(temp_edge,input)
                    newfrontier_generate(label, temp_edge, newfrontier, frontier)

            elif j == input: #一番上端の行で上が処理済
                print("一番上端")
                if G.edge[(i,j)][(i,j+1)]['weight'] == 0: #上は入る矢印
                    weightsum += 1

                if weightsum == 1: #入るのが１本なら
                    temp_edge[i] = G.edge[(i,j)][(i,j+1)]['weight']
                    temp_edge[0] = 0
                    label=label_generate(temp_edge,input)
                    newfrontier_generate(label, temp_edge, newfrontier, frontier)

                if weightsum == 2: #入るのが2本なら
                    temp_edge[i] = G.edge[(i,j)][(i,j+1)]['weight']
                    temp_edge[0] = 1#右は出る矢印
                    label=label_generate(temp_edge,input)
                    newfrontier_generate(label, temp_edge, newfrontier, frontier)

            else: #右も上も未処理
                print("右も上も未処理")
                if weightsum == 0: #出るのが2本なら
                    print("出るのが２本")
                    temp_edge[i] = 0#上は入る矢印
                    temp_edge[0] = 0#右も入る矢印
                    label=label_generate(temp_edge,input)
                    newfrontier_generate(label, temp_edge, newfrontier, frontier)

                elif weightsum == 1: #入るのが１本なら２パターン
                    print("入るのが１本で２パターン")
                    temp_edge[i] = 0 #上は入る矢印
                    temp_edge[0] = 1 #右は出る矢印
                    label=label_generate(temp_edge,input)
                    newfrontier_generate(label, temp_edge, newfrontier, frontier)

                    temp_edge[i] = 1 #上は出る矢印
                    temp_edge[0] = 0 #右は入る矢印
                    label=label_generate(temp_edge,input)
                    newfrontier_generate(label, temp_edge, newfrontier, frontier)

                else: #weightsum == 2で入るのが2本なら
                    print("入るのが２本")
                    temp_edge[i] = 1 #上は出る矢印
                    temp_edge[0] = 1 #右も出る矢印
                    label=label_generate(temp_edge,input)
                    newfrontier_generate(label, temp_edge, newfrontier, frontier)

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

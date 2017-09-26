import networkx as nx
import matplotlib.pyplot as plt

def org_grid_2d_graph(m,n,periodic=False,create_using=None): #重み付き二次元格子グラフの生成関数
    G=nx.DiGraph()
    G.name="grid_2d_graph"
    rows=range(m)
    columns=range(n)
    G.add_nodes_from( (i,j) for i in rows for j in columns )
    G.add_weighted_edges_from( [(i-1,j),(i,j),0] for i in rows for j in columns if i>0 )
    G.add_weighted_edges_from( [(i,j-1),(i,j),0] for i in rows for j in columns if j>0 )
    return G

input = 2 #考えたいgridの一辺の長さ
n = input + 2 #それに２を足す
G = org_grid_2d_graph(n, n)

pos= dict((n, n) for n in G.nodes()) #ノード名を座標に指定し描画位置を固定

edge_labels = {} #処理済判定可視化ラベル

for (s,t) in G.nodes_iter(): #端のノードを赤に
    if s == 0 or s == n-1 or t == 0 or t == n-1:
        G.node[(s, t)]['color'] = 'r'
    else:
        G.node[(s, t)]['color'] = 'yellow' #他は黄に

for ((s,t),(p,q)) in G.edges_iter(): #端のノードに隣接するエッジのweightを１にして処理済とする
    if s == 0 or s == n-1 or t == 0 or t == n-1 or p == 0 or p == n-1 or q == 0 or q == n-1:
        G.edge[(s,t)][(p,q)]['weight'] = 1

# for s in range(n):
#     G.edge[(0,s)][(1,s)]['weight'] = 0
#     G.edge[(n-1,s)][(n,s)]['weight'] = 0

G.edge[(1,0)][(1,1)]['weight'] = 0
G.edge[(2,0)][(2,1)]['weight'] = 0
G.edge[(2,1)][(3,1)]['weight'] = 0
G.edge[(2,2)][(3,2)]['weight'] = 0

temp_edge=[]
label=0

temp_edge.append(G.edge[(0,1)][(1,1)]['weight'])#横向き辺を最初に追加
for i in range(1,n-1):#最下段のフロンティアを入力
    temp_edge.append(G.edge[(i,0)][(i,1)]['weight'])

for i in range(0,n-1):#フロンティアについてラベル付け
    label = label + (2**i)*temp_edge[i]#ただし逆順で計算しているので注意

energysum=0
# energy={1:[1 1 1 1],
#         2:[0 0 0 0],
#         3:[0 1 0 1],
#         4:[1 0 1 0],
#         5:[1 0 0 1],
#         6:[0 1 1 0]}
frontier={}
newfrontier={}
frontier.setdefault(1, {})['edge'] = temp_edge#フロンティアの辺の向き
frontier.setdefault(1, {})['count'] = 1#場合の数

for j in range(1,n-1):#1~n-2まですべての行
    for i in range(1,n-1):#すべての列
        for key in frontier:#すべてのフロンティアについて
            temp_edge=frontier[key]['edge']#１つのフロンティアについてedgeを取り出す
            print((i,j),frontier,"1")

            weightsum = 0
            weightsum = weightsum + temp_edge[0] + temp_edge[i]
            print((i,j),frontier,"2") #まず処理済の左と下のweighttsumを求める

            if i == n-2 and j == n-2: #右上端
                if G.edge[(i,j)][(i,j+1)]['weight'] == 0:#上は入る矢印
                    weightsum = weightsum + 1
                    print((i,j),frontier,"3")
                if G.edge[(i,j)][(i+1,j)]['weight'] == 0:#右は入る矢印
                    weightsum = weightsum + 1
                    print((i,j),frontier,"4")

                if weightsum == 2:#このパターンは有
                    temp_edge[i] = G.edge[(i,j)][(i,j+1)]['weight']
                    temp_edge[0] = G.edge[(i,j)][(i+1,j)]['weight']
                    print((i,j),frontier,"5")
                    label=0
                    for s in range(0,n-2):#ラベル生成
                        label = label + (2**s)*temp_edge[s]
                        print((i,j),frontier,"6")
                    if label in newfrontier:
                        newfrontier[label]['count'] = newfrontier[label]['count'] + frontier[key]['count']
                        print((i,j),frontier,"7")
                    else:
                        newfrontier.setdefault(label, {})['edge'] = temp_edge#フロンティアの辺の向き
                        newfrontier.setdefault(label, {})['count'] = frontier[key]['count']#場合の数
                        print((i,j),frontier,"8")

            elif i == n-2: #一番右端の行で右が処理済
                if G.edge[(i,j)][(i+1,j)]['weight'] == 0: #右は入る矢印
                    weightsum == weightsum + 1#入るのが0か3本なら不可
                    print((i,j),frontier,"9")

                if weightsum == 1: #入るのが１本なら
                    temp_edge[i] = 0#上は入る矢印
                    temp_edge[0] = G.edge[(0,j+1)][(1,j+1)]['weight']
                    print((i,j),frontier,"10")
                    label=0
                    for s in range(0,n-2):#ラベル生成
                        label = label + (2**s)*temp_edge[s]
                        print((i,j),frontier,"11")
                    if label in newfrontier:
                        newfrontier[label]['count'] = newfrontier[label]['count'] + frontier[key]['count']
                        print((i,j),frontier,"12")
                    else:
                        newfrontier.setdefault(label, {})['edge'] = temp_edge#フロンティアの辺の向き
                        newfrontier.setdefault(label, {})['count'] = frontier[key]['count']#場合の数
                        print((i,j),frontier,"13")

                else: # weightsum == 2で入るのが2本なら
                    temp_edge[i] = 1#上は出る矢印
                    temp_edge[0] = G.edge[(0,j+1)][(1,j+1)]['weight']
                    print((i,j),frontier,"14")
                    label=0
                    for s in range(0,n-2):#ラベル生成
                        label = label + (2**s)*temp_edge[s]
                        print((i,j),frontier,"15")
                    if label in newfrontier:
                        newfrontier[label]['count'] = newfrontier[label]['count'] + frontier[key]['count']
                        print((i,j),frontier,"16")
                    else:
                        newfrontier.setdefault(label, {})['edge'] = temp_edge#フロンティアの辺の向き
                        newfrontier.setdefault(label, {})['count'] = frontier[key]['count']#場合の数
                        print((i,j),frontier,"17")

            elif j == n-2: #一番上端の行で上が処理済
                if G.edge[(i,j)][(i,j+1)]['weight'] == 0: #上は入る矢印
                    weightsum == weightsum + 1#入るのが0か3本なら不可
                    print((i,j),frontier,"18")

                if weightsum == 1: #入るのが１本なら
                    temp_edge[i] = G.edge[(i,j)][(i,j+1)]['weight']
                    temp_edge[0] = 0
                    print((i,j),frontier,"19")
                    label=0
                    for s in range(0,n-2):#ラベル生成
                        label = label + (2**s)*temp_edge[s]
                        print((i,j),frontier,"20")
                    if label in newfrontier:
                        newfrontier[label]['count'] = newfrontier[label]['count'] + frontier[key]['count']
                        print((i,j),frontier,"21")
                    else:
                        newfrontier.setdefault(label, {})['edge'] = temp_edge#フロンティアの辺の向き
                        newfrontier.setdefault(label, {})['count'] = frontier[key]['count']#場合の数
                        print((i,j),frontier,"22")

                else: # weightsum == 2で入るのが2本なら
                    temp_edge[i] = G.edge[(i,j)][(i,j+1)]['weight']
                    temp_edge[0] = 1#右は出る矢印
                    print((i,j),frontier,"23")
                    label=0
                    for s in range(0,n-2):#ラベル生成
                        label = label + (2**s)*temp_edge[s]
                        print(label,"=",label,"+","2^",s,"*",temp_edge[s])
                        print((i,j),frontier,"24")
                    if label in newfrontier:
                        newfrontier[label]['count'] = newfrontier[label]['count'] + frontier[key]['count']
                        print((i,j),frontier,"25")
                    else:
                        newfrontier.setdefault(label, {})['edge'] = temp_edge#フロンティアの辺の向き
                        newfrontier.setdefault(label, {})['count'] = frontier[key]['count']#場合の数
                        print((i,j),frontier,"26")

            else: #右も上も未処理
                if weightsum == 0: #出るのが2本なら
                    temp_edge[i] = 0#上は入る矢印
                    temp_edge[0] = 0#右も入る矢印
                    print((i,j),frontier,"27")
                    label=0
                    for s in range(0,n-2):#ラベル生成
                        label = label + (2**s)*temp_edge[s]
                        print((i,j),frontier,"28")
                    if label in newfrontier:
                        newfrontier[label]['count'] = newfrontier[label]['count'] + frontier[key]['count']
                        print((i,j),frontier,"29")
                    else:
                        newfrontier.setdefault(label, {})['edge'] = temp_edge#フロンティアの辺の向き
                        newfrontier.setdefault(label, {})['count'] = frontier[key]['count']#場合の数
                        print((i,j),frontier,"30")

                elif weightsum == 1: #入るのが１本なら２パターン
                    temp_edge[i] = 0 #上は入る矢印
                    temp_edge[0] = 1 #右は出る矢印
                    print((i,j),frontier,"31")
                    label=0
                    for s in range(0,n-2):#ラベル生成
                        label = label + (2**s)*temp_edge[s]
                        print((i,j),frontier,"32")
                    if label in newfrontier:
                        newfrontier[label]['count'] = newfrontier[label]['count'] + frontier[key]['count']
                        print((i,j),frontier,"33")
                    else:
                        newfrontier.setdefault(label, {})['edge'] = temp_edge#フロンティアの辺の向き
                        newfrontier.setdefault(label, {})['count'] = frontier[key]['count']#場合の数
                        print((i,j),frontier,"34")

                    temp_edge[i] = 1 #上は出る矢印
                    temp_edge[0] = 0 #右は入る矢印
                    print((i,j),frontier,"35",temp_edge)
                    label=0
                    for s in range(0,n-2):#ラベル生成
                        label = label + (2**s)*temp_edge[s]
                        print((i,j),frontier,"36")
                    if label in newfrontier:
                        newfrontier[label]['count'] = newfrontier[label]['count'] + frontier[key]['count']
                        print((i,j),frontier,"37")
                    else:
                        newfrontier.setdefault(label, {})['edge'] = temp_edge#フロンティアの辺の向き
                        newfrontier.setdefault(label, {})['count'] = frontier[key]['count']#場合の数
                        print((i,j),frontier,"38")

                else: #weightsum == 2で入るのが2本なら
                    temp_edge[i] = 1 #上は出る矢印
                    temp_edge[0] = 1 #右も出る矢印
                    print((i,j),frontier,"39")
                    label=0
                    for s in range(0,n-2):#ラベル生成
                        label = label + (2**s)*temp_edge[s]
                        print(label,"=",label,"+","2^",s,"*",temp_edge[s])
                        print((i,j),frontier,"40")
                    if label in newfrontier:
                        newfrontier[label]['count'] = newfrontier[label]['count'] + frontier[key]['count']
                        print((i,j),frontier,"41")
                    else:
                        newfrontier.setdefault(label, {})['edge'] = temp_edge#フロンティアの辺の向き
                        newfrontier.setdefault(label, {})['count'] = frontier[key]['count']#場合の数
                        print((i,j),frontier,"42")

        frontier = newfrontier
        newfrontier={}
        print((i,j),frontier,"new")

count=0
for key in frontier:
    count = count + frontier[key]['count']
print(count)

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

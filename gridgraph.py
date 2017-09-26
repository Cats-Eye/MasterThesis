import networkx as nx
import matplotlib.pyplot as plt

def org_grid_2d_graph(m,n,periodic=False,create_using=None): #重み付き二次元格子グラフの生成関数
    G=nx.empty_graph(0,create_using)
    G.name="grid_2d_graph"
    rows=range(m)
    columns=range(n)
    G.add_nodes_from( (i,j) for i in rows for j in columns )
    G.add_weighted_edges_from( [(i,j),(i-1,j),1] for i in rows for j in columns if i>0 )
    G.add_weighted_edges_from( [(i,j),(i,j-1),1] for i in rows for j in columns if j>0 )
    return G

n = 10
G = org_grid_2d_graph(n, n)

pos= dict((n, n) for n in G.nodes()) #ノード名を座標に指定し描画位置を固定

edge_labels = {} #可視化のためにエッジのweightとラベルの紐付け
visited = {} #エッジの処理済判定ラベル

for s,t in G.edges_iter():
    edge_labels[s,t] = G.edge[s][t]['weight']
    G.edge[s][t]['fixed'] = False

for (s,t) in G.nodes_iter(): #端のノードを赤に
    if s == 0 or s == n-1 or t == 0 or t == n-1:
        G.node[(s, t)]['color'] = 'r'
    else:
        G.node[(s, t)]['color'] = 'yellow'

for ((s,t),(p,q)) in G.edges_iter(): #端のノードに隣接するエッジを処理済ラベルに
    if s == 0 or s == n-1 or t == 0 or t == n-1 or p == 0 or p == n-1 or q == 0 or q == n-1:
        G.edge[(s,t)][(p,q)]['fixed'] = True

# frontier = {} #フロンティアのノードを格納
# for j in range(1,2):
#     for i in range(1,n-2):
#         frontier = {}
#         entersum = 0
#         entersum = entersum + G.edge[(i-1,j)][(i,j)]['weight'] + G[(i,j-1)][(i,j)]['weight'] #まず処理済の左と下のentersumを求める
#
#         if entersum == 2: #入ってくる矢印が2本の場合自動的に上と右が決まる
#             if G.edge[(i,j)][(i+1,j)]['weight'] == 0: #右が既に反転して決定している場合、3本入ってくるので不可
#                 消去
#             G.edge[(i,j)][(i+1,j)]['weight'] == 1
#             G.edge[(i,j)][(i,j+1)]['weight'] == 1
#             G.edge[(i,j)][(i+1,j)]['fixed'] == True
#             G.edge[(i,j)][(i,j+1)]['fixed'] == True
#         elif entersum == 0: #入ってくる矢印が0本の場合自動的に上と右が決まる
#             if G.edge[(i,j)][(i+1,j)]['weight'] == 1: #右が既に決定している場合、出て行くので不可
#                 消去
#             G.edge[(i,j)][(i+1,j)]['weight'] == 0
#             G.edge[(i,j)][(i,j+1)]['weight'] == 0
#             G.edge[(i,j)][(i+1,j)]['fixed'] == True
#             G.edge[(i,j)][(i,j+1)]['fixed'] == True
#         else: #entersumが１の場合
#             G.edge[(i,j)][(i+1,j)]['weight'] == 1


for (s,t) in G.edges_iter(): #処理済は青、未処理は黒
    if G.edge[s][t]['fixed'] == True:
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

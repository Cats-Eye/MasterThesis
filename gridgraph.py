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
visited = {} #エッジの処理済ラベル
for s,t in G.edges_iter():
    edge_labels[s,t] = G.edge[s][t]['weight']
    visited[s,t] = False

for (s,t) in G.nodes_iter(): #端のノードを赤に
    if s == 0 or s == n-1 or t == 0 or t == n-1:
        G.node[(s, t)]['color'] = 'r'

for (s,t),(p,q) in G.edges_iter(): #端のノードに隣接するエッジを処理済ラベルに
    if s == 0 or s == n-1 or t == 0 or t == n-1 or p == 0 or p == n-1 or q == 0 or q == n-1:
        visited[(s,t),(p,q)] = True

nx.draw_networkx(G, pos, #描画
        node_color=[G.node[n].get('color', 'yellow') for n in G.nodes_iter()]) #全ノードを黄に
nx.draw_networkx_edge_labels(G, pos, edge_labels)
plt.axis('equal') #x,yの座標値の増分を同量に調整
plt.gca().xaxis.set_visible(False)
plt.gca().yaxis.set_visible(False)
plt.show()

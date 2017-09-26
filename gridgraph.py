import sys
sys.path.append("D:\Python34\lib\site-packages")
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

n = 9
G = org_grid_2d_graph(n, n)
pos= dict((n, n) for n in G.nodes()) #ノード名は座標に等しいことを利用しノードの描画位置を固定

for i in range(n): #端の部分を赤に
    if i == 0 or i ==n-1:
        for j in range(n):
            G.node[(i, j)]['color'] = 'r'
            G.node[(j, i)]['color'] = 'r'

edge_labels={}

for i in range(1,n):
    for j in range(n):
        edge_labels[(i,j),(i-1,j)] = G[(i,j)][(i-1,j)]['weight']

for j in range(1,n):
    for i in range(n):
        edge_labels[(i,j),(i,j-1)] = G[(i,j)][(i,j-1)]['weight']

nx.draw_networkx(G, pos, #描画
        node_color=[G.node[n].get('color', 'w') for n in G.nodes_iter()]) #ノードを白に
nx.draw_networkx_edge_labels(G, pos, edge_labels)
plt.axis('equal') #x,yの座標値の増分を同量に調整
plt.gca().xaxis.set_visible(False)
plt.gca().yaxis.set_visible(False)
plt.show()

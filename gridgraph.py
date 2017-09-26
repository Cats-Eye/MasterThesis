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

edge_labels = {} #可視化のために辺のweightとラベルの紐付け
visited = {} #処理済ラベル
for s,t in G.edges_iter():
    edge_labels[s,t] = G.edge[s][t]['weight']
    visited[s,t] = False

for s in G.nodes_iter(): #全ノードを黄に
    G.node[s]['color'] = 'yellow'

for i in range(n): #端の部分を赤に
    if i == 0 or i ==n-1:
        for j in range(n):
            G.node[(i, j)]['color'] = 'r'
            G.node[(j, i)]['color'] = 'r'



#for s,t in G.edges_iter():
#visited[()]

#for j in range(1,n-1):
#    weightsum=0
#    for n in G.edges((j,i)):
#        if fixed[n]=true
#        weightsum=G[(j,i)][(j-1,i)]['weight']+G[(j,i)][(j+1,i)]['weight']+G[(j,i)][(j,i-1)]['weight']+G[(j,i)][(j,i+1)]['weight']
#        G.node[(j,i)]['color'] = 'yellow'

#print(G.nodes('color'='r'))

nx.draw_networkx(G, pos, #描画
        node_color=[G.node[n].get('color', 'w') for n in G.nodes_iter()]) #ノードを白に
nx.draw_networkx_edge_labels(G, pos, edge_labels)
plt.axis('equal') #x,yの座標値の増分を同量に調整
plt.gca().xaxis.set_visible(False)
plt.gca().yaxis.set_visible(False)
plt.show()

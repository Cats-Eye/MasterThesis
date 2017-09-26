# coding:utf-8
import networkx as nx
import matplotlib.pyplot as plt

n = 9
G = nx.grid_2d_graph(n, n)
pos= dict((n, n) for n in G.nodes()) #ノード名は座標に等しいことを利用しノードの描画位置を固定

for i in range(n): #端の部分を赤に
    if i == 0 or i ==n-1:
        for j in range(n):
            G.node[(i, j)]['color'] = 'r'
            G.node[(j, i)]['color'] = 'r'

nx.draw_networkx(G, pos, #描画
        node_color=[G.node[n].get('color', 'w') for n in G.nodes_iter()]) #ノードを白に
plt.axis('equal') #x,yの座標値の増分を同量に調整
plt.gca().xaxis.set_visible(False)
plt.gca().yaxis.set_visible(False)
plt.show()

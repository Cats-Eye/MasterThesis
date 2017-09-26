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

n = 10
G = org_grid_2d_graph(n, n)

pos= dict((n, n) for n in G.nodes()) #ノード名を座標に指定し描画位置を固定

edge_labels = {} #処理済判定可視化ラベル

for (s,t) in G.nodes_iter(): #端のノードを赤に
    if s == 0 or s == n-1 or t == 0 or t == n-1:
        G.node[(s, t)]['color'] = 'r'
    else:
        G.node[(s, t)]['color'] = 'yellow'

for ((s,t),(p,q)) in G.edges_iter(): #端のノードに隣接するエッジのweightを１にして処理済とする
    if s == 0 or s == n-1 or t == 0 or t == n-1 or p == 0 or p == n-1 or q == 0 or q == n-1:
        G.edge[(s,t)][(p,q)]['weight'] = 1

# for i in range(1,2):
#     for j in range(1,n-1):
#         weightsum = 0
#         weightsum = weightsum + G[(i-1,j)][(i,j)]['weight'] + G[(i,j-1)][(i,j)]['weight'] #まず処理済の左と下のweighttsumを求める
#         if G.edge[(i,j)][(i+1,j)]['visited'] == True: #右は処理済の可能性有
#             weightsum = weightsum + G[(i,j)][(i+1,j)]['weight']
#         else:
#             G.edge[(i,j)][(i+1,j)]['visited'] = True
#
#             weightsum = weightsum + G[(i,j)][(i+1,j)]['weight'] #こっからは右が1の場合
#             if weightsum == 3 or weightsum == 1:
#                 G[(i,j)][(i,j+1)]['weight']=1
#             elif weightsum == 2 or weightsum == 0:
#                 G[(i,j)][(i,j+1)]['weight']=0

        # print(weightsum)
        # if G.edge[(i-1,j)][(i,j)]['visited'] == True:
        #     weightsum = weightsum + G[(i-1,j)][(i,j)]['weight']

        # if G.edge[(i,j-1)][(i,j)]['visited'] == True:
        #     weightsum = weightsum + G[(i,j-1)][(i,j)]['weight']
        # if G.edge[(i,j)][(i,j+1)]['visited'] == True:
        #     weightsum = weightsum + G[(i,j)][(i,j+1)]['weight']

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

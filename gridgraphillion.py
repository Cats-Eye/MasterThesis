from graphillion import GraphSet
import graphillion.tutorial as tl  # チュートリアルのためのヘルパー・モジュール
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
    for ((s,t),(p,q)) in G.edges_iter(): #端のノードに隣接するエッジのweightを１にしてとりあえずデフォの方向に
        if s == 0 or t == 0 or p == n-1 or q == n-1:
            G.edge[(s,t)][(p,q)]['weight'] = 1
        else: #他のedgeは0で未設定で
            G.edge[(s,t)][(p,q)]['weight'] = 0
    return G

def draw(g, universe=None):
    if not isinstance(g, nx.Graph):#gがnx.Graphじゃなかったら
        g = nx.Graph(list(g))
    if universe is None:
        universe = GraphSet.universe()
    if not isinstance(universe, nx.Graph):#universeがnx.Graphじゃなかったら
        universe = nx.Graph(list(universe))
    g.add_nodes_from(universe.nodes())
    pos= dict((n, n) for n in universe.nodes()) #ノード名を座標に指定し描画位置を固定
    for (s,t) in G.nodes_iter(): #端のノードを赤に
        if s == 0 or s == n-1 or t == 0 or t == n-1:
            g.node[(s, t)]['color'] = 'r'
        else:
            g.node[(s, t)]['color'] = 'yellow' #他は黄に
    # edge_labels = {} #処理済判定可視化ラベル
    # for s,t in g.edges_iter(): #描画用処理判定可視化
    #     edge_labels[s,t] = g.edge[s][t]['weight']
    # nx.draw(g, pos, node_color=[g.node[n]['color'] for n in g.nodes_iter()])
    nx.draw(g, pos)
    # nx.draw_networkx_edge_labels(g, pos, edge_labels)
    # nx.draw_networkx_edges(g,pos,edge_color= [g.edge[s][t]['color'] for (s,t) in g.edges_iter()])
    plt.axis('equal') #x,yの座標値の増分を同量に調整
    plt.show()

input = 4 #考えたいgridの一辺の長さ
n = input + 2 #それに２を足す
G = org_grid_2d_graph(n, n)
preuniverse = G.edges()
universe = []
for (s,t) in preuniverse:
    universe.append((s, t, G.edge[s][t]['weight']))
GraphSet.set_universe(universe)
draw(universe)



#
# edge_labels = {} #処理済判定可視化ラベル
#
# for (s,t) in G.nodes_iter(): #端のノードを赤に
#     if s == 0 or s == n-1 or t == 0 or t == n-1:
#         G.node[(s, t)]['color'] = 'r'
#     else:
#         G.node[(s, t)]['color'] = 'yellow' #他は黄に
#
# G.remove_edge((1,0), (1,1)) #解が２になる小池さんグリッド
# G.remove_edge((2,0), (2,1))
# G.remove_edge((2,1), (3,1))
# G.remove_edge((2,2), (3,2))
#
# universe = G
# for (s,t) in G.edges_iter():
#     universe.append((s,t))
# GraphSet.set_universe(universe)
#
# tl.draw(universe)
#
# weightsum = 0
# gs={}#端っこだけ投入
# new_gs={}
#
# for j in range(1,input+1):#1~n-2まですべての行
#     for i in range(1,input+1):#すべての列
#         if ((i,j),(i+1,j)) in gs:
#             weightsum = weightsum + 1

# nx.draw_networkx(G, pos, node_color=[G.node[n]['color'] for n in G.nodes_iter()]) #描画
# nx.draw_networkx_edge_labels(G, pos, edge_labels)
# nx.draw_networkx_edges(G,pos,edge_color= [G.edge[s][t]['color'] for (s,t) in G.edges_iter()])
# plt.axis('equal') #x,yの座標値の増分を同量に調整
# plt.gca().xaxis.set_visible(False)
# plt.gca().yaxis.set_visible(False)
# plt.show()

#
# start = 1
# goal = 81
# paths = GraphSet.paths(start, goal)
# # print(len(paths))  # 結果が大規模のときは paths.len() を使う
# # for path in paths: #これでイテレーションできる
# # tl.draw(paths.choice())
#
# key = 64
# treasure = 18
# paths_to_key = GraphSet.paths(start, key).excluding(treasure)  # 宝箱を通らずに鍵にたどり着くパス
# treasure_paths = paths.including(paths_to_key).including(treasure)  # 鍵と宝箱を通ってゴールにたどり着くパス
# len(treasure_paths)
# tl.draw(treasure_paths.choice())  # パスのひとつを表示する
#
# treasure_paths < paths  # Graphillion において "<" は "subset-of" の意味

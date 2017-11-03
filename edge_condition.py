# for ((s,t),(p,q)) in G.edges_iter(): #テスト
#     if  p == n-1 or q == n-1:
#         G.edge[(s,t)][(p,q)]['weight'] = 0

# G.edge[(1,0)][(1,1)]['weight'] = -1 #解が２になる小池さんグリッド
# G.edge[(2,0)][(2,1)]['weight'] = -1
# G.edge[(2,1)][(3,1)]['weight'] = -1
# G.edge[(2,2)][(3,2)]['weight'] = -1

G.edge[(1,2)][(1,3)]['weight'] = -1 #解が２になる小池さんグリッド +90
G.edge[(2,2)][(2,3)]['weight'] = -1
G.edge[(0,1)][(1,1)]['weight'] = -1
G.edge[(0,2)][(1,2)]['weight'] = -1

G.edge[(2,1)][(3,1)]['weight'] = -1 #解が２になる小池さんグリッド +180
G.edge[(2,2)][(3,2)]['weight'] = -1
G.edge[(0,1)][(1,1)]['weight'] = -1
G.edge[(0,2)][(1,2)]['weight'] = -1

G.edge[(1,2)][(1,3)]['weight'] = -1 #解が２になる小池さんグリッド +270
G.edge[(2,2)][(2,3)]['weight'] = -1
G.edge[(0,1)][(1,1)]['weight'] = -1
G.edge[(0,2)][(1,2)]['weight'] = -1

G.edge[(2,0)][(2,1)]['weight'] = -1 #パワポの4*4グリッド
G.edge[(0,1)][(1,1)]['weight'] = -1
G.edge[(0,3)][(1,3)]['weight'] = -1
G.edge[(0,4)][(1,4)]['weight'] = -1
G.edge[(1,4)][(1,5)]['weight'] = -1
G.edge[(4,4)][(4,5)]['weight'] = -1
G.edge[(1,4)][(1,5)]['weight'] = -1
G.edge[(4,1)][(5,1)]['weight'] = -1
G.edge[(4,2)][(5,2)]['weight'] = -1

# G.edge[(0,4)][(1,4)]['weight'] = 0 #4*4グリッド初期
G.edge[(0,3)][(1,3)]['weight'] = 0
# G.edge[(0,2)][(1,2)]['weight'] = 0
G.edge[(0,1)][(1,1)]['weight'] = 0

# G.edge[(1,0)][(1,1)]['weight'] = 0
# G.edge[(2,0)][(2,1)]['weight'] = 0
G.edge[(3,0)][(3,1)]['weight'] = 0
# G.edge[(4,0)][(4,1)]['weight'] = 0

G.edge[(4,1)][(5,1)]['weight'] = -1
# G.edge[(4,2)][(5,2)]['weight'] = 0
G.edge[(4,3)][(5,3)]['weight'] = 0
G.edge[(4,4)][(5,4)]['weight'] = 0

G.edge[(4,4)][(4,5)]['weight'] = 0
G.edge[(3,4)][(3,5)]['weight'] = 0
# G.edge[(2,4)][(2,5)]['weight'] = 0
# G.edge[(1,4)][(1,5)]['weight'] = 0

G.edge[(0,4)][(1,4)]['weight'] = 0 #4*4グリッド -90回転
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

# G.edge[(0,4)][(1,4)]['weight'] = 0 #4*4グリッド -180回転
G.edge[(0,3)][(1,3)]['weight'] = -1
G.edge[(0,2)][(1,2)]['weight'] = 0
G.edge[(0,1)][(1,1)]['weight'] = 0

G.edge[(1,0)][(1,1)]['weight'] = 0
G.edge[(2,0)][(2,1)]['weight'] = 0
G.edge[(3,0)][(3,1)]['weight'] = -1
G.edge[(4,0)][(4,1)]['weight'] = -1

G.edge[(4,1)][(5,1)]['weight'] = -1
G.edge[(4,2)][(5,2)]['weight'] = 0
G.edge[(4,3)][(5,3)]['weight'] = -1
G.edge[(4,4)][(5,4)]['weight'] = 0

G.edge[(4,4)][(4,5)]['weight'] = -1
G.edge[(3,4)][(3,5)]['weight'] = -1
G.edge[(2,4)][(2,5)]['weight'] = 0
G.edge[(1,4)][(1,5)]['weight'] = -1

# G.edge[(0,4)][(1,4)]['weight'] = 0 #4*4グリッド -270回転
# G.edge[(0,3)][(1,3)]['weight'] = 0
G.edge[(0,2)][(1,2)]['weight'] = 0
# G.edge[(0,1)][(1,1)]['weight'] = 0

# G.edge[(1,0)][(1,1)]['weight'] = 0
G.edge[(2,0)][(2,1)]['weight'] = -1
G.edge[(3,0)][(3,1)]['weight'] = 0
G.edge[(4,0)][(4,1)]['weight'] = 0

G.edge[(4,1)][(5,1)]['weight'] = 0
G.edge[(4,2)][(5,2)]['weight'] = 0
G.edge[(4,3)][(5,3)]['weight'] = 1
G.edge[(4,4)][(5,4)]['weight'] = 1

G.edge[(4,4)][(4,5)]['weight'] = -1
G.edge[(3,4)][(3,5)]['weight'] = 0
G.edge[(2,4)][(2,5)]['weight'] = -1
G.edge[(1,4)][(1,5)]['weight'] = 0

# G.edge[(0,4)][(1,4)]['weight'] = 0 #4*4グリッド初期
G.edge[(0,3)][(1,3)]['weight'] = 0
# G.edge[(0,2)][(1,2)]['weight'] = 0
G.edge[(0,1)][(1,1)]['weight'] = 0

# G.edge[(1,0)][(1,1)]['weight'] = 0
# G.edge[(2,0)][(2,1)]['weight'] = 0
G.edge[(3,0)][(3,1)]['weight'] = 0
# G.edge[(4,0)][(4,1)]['weight'] = 0

G.edge[(4,1)][(5,1)]['weight'] = -1
# G.edge[(4,2)][(5,2)]['weight'] = 0
G.edge[(4,3)][(5,3)]['weight'] = 0
G.edge[(4,4)][(5,4)]['weight'] = 0

G.edge[(4,4)][(4,5)]['weight'] = 0
G.edge[(3,4)][(3,5)]['weight'] = 0
# G.edge[(2,4)][(2,5)]['weight'] = 0
# G.edge[(1,4)][(1,5)]['weight'] = 0

# G.edge[(0,3)][(1,3)]['weight'] = -1 #3*3グリッド
# G.edge[(0,2)][(1,2)]['weight'] = -1
# G.edge[(0,1)][(1,1)]['weight'] = 0
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

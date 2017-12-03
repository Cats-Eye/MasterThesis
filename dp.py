import copy
import time

start = time.time()

def label_generate(temp_edge_g, input_g):#ラベル生成関数
    label_g = 0
    for i in range(0,input_g+1):#フロンティアについてラベル付け
        if temp_edge_g[i] == 1:
            label_g = label_g + (2**i)*1#ただし逆順で計算しているので注意
        else:
            label_g = label_g + (2**i)*0
    return(label_g)

class Front(object):
    def __init__(self, l, f, n, e, np): #初期化　コンストラクタ
        self.index = l #フロンティアのラベル
        self.frontier = f #フロンティア
        self.count = n #個数
        self.energysum = e #エネルギー合計
        self.nodepattern = np #各パターンの個数

    def output(self):
        print(sself.energysum, self.count)

    def insert(self):
        temp_frontier = self.frontier
        # print(temp_frontier, "\n")
        if place == 1: #行が１つ上になって左端の場合
            temp_frontier[0] = 0 #左は未処理
        patterns = pattern_dic[(temp_frontier[0], temp_frontier[place])] #左と下の状態から
        temp_energysum = self.energysum
        temp_nodepattern = self.nodepattern

        for i in patterns: #有りパターン
            # print(i, "あり", end =' ')
            temp_frontier[0] = direction_dic[i][0] #フロンティアを更新
            temp_frontier[place] = direction_dic[i][1]
            new_frontier = copy.deepcopy(temp_frontier)
            new_energysum = self.energysum + energy_dic[i]
            temp_nodepattern[i] += 1
            new_nodepattern = copy.deepcopy(temp_nodepattern)

            for front in NewFronts:
                if front.frontier == new_frontier and front.energysum == new_energysum and front.nodepattern == new_nodepattern: #同じ条件のものがあれば
                    # print("front有", end =' ')
                    front.count += self.count  #個数を追加
                    break
            else: #同じ条件のものがなくbreakしなかった場合
                # print("front無", end =' ')
                label=label_generate(new_frontier,input)
                new_front = Front(label, new_frontier, self.count, new_energysum, new_nodepattern)
                NewFronts.append(new_front)

pattern_dic = {( 0, 0): [0,1,2,3,4,5], #制限無し
               ( 1, 0): [0,2,4],  #左が正
               (-1, 0): [1,3,5],  #左が負
               ( 0, 1): [0,3,5],  #下が正
               ( 0,-1): [1,2,4],  #下が負
               ( 1, 1): [0],  #左が正、下が正
               (-1,-1): [1],  #左が負、下が負
               (-1, 1): [3,5],  #左が負、下が正
               ( 1,-1): [2,4]}  #左が正、下が負

direction_dic = {0:[ 1, 1], #各配置パターンにおける[左, 上]の正負
                 1:[-1,-1],
                 2:[ 1,-1],
                 3:[-1, 1],
                 4:[-1, 1],
                 5:[ 1,-1]}

energy_dic={0:1, #各配置におけるエネルギー
            1:2,
            2:3,
            3:4,
            4:5,
            5:6}

input =  4 #考えたいgridの一辺の長さ
nodesum = input**2 #node総数

OldFronts=[] #各ノードにおける古いfront集合
NewFronts=[] #各ノードにおける新しいfront集合

first_front = Front(0, [0]*(input+1), 1, 0, [0]*6)
OldFronts.append(first_front)

for node in range(nodesum, 0, -1): #各nodeについて
    # print("のーど",node,"\n", OldFronts)
    place = (nodesum - node + 1) % input #左から数えたnode位置
    if place == 0: #右端は割り切れて0になるのでinputに書き換え
        place = input

    for front in OldFronts:
        front.insert()

    OldFronts = NewFronts
    NewFronts = []

Energy = {}
sum = 0
for front in OldFronts:
    sum += front.count
    if front.energysum in Energy:
        Energy[front.energysum] += front.count
    else:
        Energy[front.energysum] = front.count
print("配置総数は", sum)

for k, v in sorted(Energy.items()):
    print(str(k), str(v))

elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

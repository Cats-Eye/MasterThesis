import copy
import time

start = time.time()

class Front(object):
    def __init__(self, f, n, e): #初期化　コンストラクタ
        self.frontier = f #フロンティア
        self.count = n #個数
        self.energysum = e #エネルギー合計

    def insert(self):
        temp_frontier = self.frontier
        if place == 1: #行が１つ上になって左端の場合
            temp_frontier[0] = 0 #左は未処理
        patterns = pattern_dic[(temp_frontier[0], temp_frontier[place])] #左と下の状態から
        temp_energysum = self.energysum #更新前のフロンティア

        for i in patterns: #有りパターン
            temp_frontier[0] = direction_dic[i][0] #フロンティアを更新
            temp_frontier[place] = direction_dic[i][1]
            new_frontier = copy.deepcopy(temp_frontier)
            new_energysum = self.energysum + energy_dic[i] #エネルギー合計を更新

            for front in NewFronts:
                if front.frontier == new_frontier and front.energysum == new_energysum: #同じ条件のものがあれば
                    front.count += self.count  #個数を追加
                    break
            else: #同じ条件のものがなくbreakしなかった場合
                new_front = Front(new_frontier, self.count, new_energysum) #新しくfrontを作る
                NewFronts.append(new_front)

# 対象ノードの(左, 下)の状態からみて可能なパターン
# 0は方向未処理、1は正方向、-1は負方向
pattern_dic = {( 0, 0): [0,1,2,3,4,5], #制限無し
               ( 1, 0): [0,2,4],  #左が正
               (-1, 0): [1,3,5],  #左が負
               ( 0, 1): [0,3,5],  #下が正
               ( 0,-1): [1,2,4],  #下が負
               ( 1, 1): [0],  #左が正、下が正
               (-1,-1): [1],  #左が負、下が負
               (-1, 1): [3,5],  #左が負、下が正
               ( 1,-1): [2,4]}  #左が正、下が負

direction_dic = {0:[ 1, 1], #0~5の配置パターンにおける[右, 上]の正負
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

input = 7 #考えたいgridの一辺の長さ
nodesum = input**2 #node総数
frontsum = 1

OldFronts=[] #各ノードにおける古いfront集合
NewFronts=[] #各ノードにおける新しいfront集合

first_front = Front([0]*(input+1), 1, 0) #初期front
OldFronts.append(first_front)

for node in range(nodesum, 0, -1): #各nodeについて
    place = (nodesum - node + 1) % input #左から数えたnode位置
    if place == 0: #右端は割り切れて0になるのでinputに書き換え
        place = input

    for front in OldFronts: #各frontについて更新
        front.insert()

    frontsum += len(OldFronts)
    OldFronts = NewFronts
    NewFronts = []

Energy = {}
sum = 0
f = open('result.txt', 'w')

for front in OldFronts:
    sum += front.count #配置パターン総数を求める
    if front.energysum in Energy: #エネルギー総計毎にまとめる
        Energy[front.energysum] += front.count
    else:
        Energy[front.energysum] = front.count

elapsed_time = time.time() - start
f.write("input" + str(input) + "の配置総数は" + str(sum) + "\n")
f.write("elapsed_time:{0}".format(elapsed_time) + "[sec]")

# for k, v in sorted(Energy.items()):
    # f.write(str(k) + " " + str(v) + "\n")

f.close()

print(input, "のフロント総数", frontsum, "最終フロント総数", len(OldFronts))

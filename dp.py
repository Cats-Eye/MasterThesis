import copy
import time

start = time.time()

input = 4 #考えたいgridの一辺の長さ

def frontier_generate(label_g):#frontier生成関数
    frontier_g = [0]*(input+1)
    for i in range(0,input+1):
        if label_g % 2 == 0: # [0, 1]が[-1, 1]に対応
            frontier_g[i] = -1
        else:
            frontier_g[i] = 1
        label_g = label_g // 2
    return(frontier_g)

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

nodesum = input**2 #node総数
frontsum = 1

#energysum, frontierのラベルをキーとする場合の数
OldFronts = {} #各ノードにおける更新前front集合
NewFronts = {} #各ノードにおける更新後front集合

first_frontier = [0]*(input+1) #初期frontier
OldFronts.setdefault(0, {}).setdefault(0, 1)

for node in range(nodesum, 0, -1): #各nodeについて
    place = (nodesum - node + 1) % input #左から数えたnode位置
    if place == 0: #右端は割り切れて0になるのでinputに書き換え
        place = input
    for energysum in OldFronts:
        for label in OldFronts[energysum]:
            new_frontier = frontier_generate(label)

            old_label = label #次に渡すラベル準備
            if new_frontier[0] == 1:
                old_label -= (2**0)*1
            if new_frontier[place] == 1:
                old_label -= (2**place)*1

            if node >= nodesum-input+1: #歳下段の場合
                new_frontier[place] = 0 #下は未処理
            if place == 1: #行が１つ上になって左端の場合
                new_frontier[0] = 0 #左は未処理
            patterns = pattern_dic[(new_frontier[0], new_frontier[place])] #左と下の状態から

            for i in patterns: #有りパターン
                new_frontier[0] = direction_dic[i][0] #フロンティアを更新
                new_frontier[place] = direction_dic[i][1]
                new_label = old_label
                if new_frontier[0] == 1: #ラベルを更新
                    new_label += (2**0)*1
                if new_frontier[place] == 1:
                    new_label += (2**place)*1
                new_energysum = energysum + energy_dic[i] #エネルギー合計を更新

                if (new_energysum in NewFronts) and (new_label in NewFronts[new_energysum]): #同じ条件のものがあれば
                    NewFronts[new_energysum][new_label] += OldFronts[energysum][label] #場合の数を追加
                else: #同じ条件のものがなかった場合
                    NewFronts.setdefault(new_energysum, {}).setdefault(new_label, OldFronts[energysum][label]) #新しくfrontを作る
                    frontsum += 1
    OldFronts = NewFronts
    NewFronts = {}

Energy = {}
sum = 0
for energysum in OldFronts:
    Energy[energysum] = 0
    for label in OldFronts[energysum]:
        sum += OldFronts[energysum][label] #配置パターン総数を求める
        Energy[energysum] += OldFronts[energysum][label] #エネルギー総計毎にまとめる

elapsed_time = time.time() - start
f = open('result.txt', 'w')
f.write("input" + str(input) + "の配置総数は" + str(sum) + "\n")
f.write("elapsed_time:{0}".format(elapsed_time) + "[sec]" + "\n")
f.write("フロント総数" + str(frontsum) +"\n")

# for k, v in sorted(Energy.items()):
#     f.write(str(k) + " " + str(v) + "\n")

f.close()

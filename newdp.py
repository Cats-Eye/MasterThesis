import copy
import time

start = time.time()

input = 3#考えたいgridの一辺の長さ

# 対象ノードの(左, 下)の状態からみて可能なパターン
# -1は方向未処理、0は負方向、1は正方向
pattern_dic = {(-1,-1): [0,1,2,3,4,5], #制限無し
               ( 1,-1): [0,2,4],  #左が正
               ( 0,-1): [1,3,5],  #左が負
               (-1, 1): [0,3,5],  #下が正
               (-1, 0): [1,2,4],  #下が負
               ( 1, 1): [0],  #左が正、下が正
               ( 0, 0): [1],  #左が負、下が負
               ( 0, 1): [3,5],  #左が負、下が正
               ( 1, 0): [2,4]}  #左が正、下が負

direction_dic = {0:[ 1, 1], #0~5の配置パターンにおける[右, 上]の正負
                 1:[ 0, 0],
                 2:[ 1, 0],
                 3:[ 0, 1],
                 4:[ 0, 1],
                 5:[ 1, 0]}

energy_dic={0:1, #各配置におけるエネルギー
            1:2,
            2:3,
            3:4,
            4:5,
            5:6}

nodesum = input**2 #node総数
frontsum = 1 #カウント用

bit = 0
for i in range(input+1):
    bit = bit | (1 << i)
musk = [] #ビット演算マスク用
for i in range(input+1):
    musk.append(bit - (1 << i))

#energysum, frontierのラベルをキーとする場合の数
OldFronts = {} #各ノードにおける更新前front集合
NewFronts = {} #各ノードにおける更新後front集合

OldFronts.setdefault(0, {}).setdefault(0, 1)

for node in range(nodesum, 0, -1): #各nodeについて
    place = (nodesum - node + 1) % input #左から数えたnode位置
    if place == 0: #右端は割り切れて0になるのでinputに書き換え
        place = input
    for energysum in OldFronts:
        for label in OldFronts[energysum]:
            temp_label = label #次に渡すラベル準備
            temp_label = temp_label & musk[0] #0(nodeの左)をマスク
            temp_label = temp_label & musk[place] #place(nodeの下)をマスク

            if node >= nodesum-input+1: #最下段の場合、place(nodeの下)は未処理(-1)
                if place == 1: #行が１つ上になって左端の場合、0(nodeの左)は未処理(-1)
                    patterns = pattern_dic[(-1,-1)]
                else:
                    patterns = pattern_dic[(label & 1,-1)]
            else:
                if place == 1: #行が１つ上になって左端の場合、0(nodeの左)は未処理
                    patterns = pattern_dic[(-1, (label >> place) & 1)]
                else:
                    patterns = pattern_dic[(label & 1, (label >> place) & 1)]

            for i in patterns: #有りパターン
                new_label = temp_label
                if direction_dic[i][0] == 1: #ラベルを更新
                    new_label += 1
                if direction_dic[i][1] == 1:
                    new_label += (1 << place)
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
f.write("elapsed_time:{0}".format(elapsed_time) + "\n")
f.write("フロント総数" + str(frontsum) +"\n")

# for k, v in sorted(Energy.items()):
#     f.write(str(k) + " " + str(v) + "\n")

f.close()

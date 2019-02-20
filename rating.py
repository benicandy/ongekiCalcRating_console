import database
import math
from bs4 import BeautifulSoup
#import requests
#from urllib.parse import urljoin

# 各枠のレートなどを算出する
# 評価値：スコアと譜面定数から算出される一曲あたりのレート値を"評価値"と呼ぶことにする


html = "rating.html"  # 保存したhtmlファイルを指定
with open(html, encoding="utf-8") as fp:
    res = fp.read()


soup = BeautifulSoup(res, "lxml")  # lxmlをinstallしておく
elems_label = soup.select('.music_label')      # 曲名を抽出
elems_level = soup.select('.score_level.t_c')  # 曲のレベルを抽出
elems_score = soup.select('.f_14.l_h_12')      # 曲のスコアを抽出


# 1譜面の評価値を算出
def calc_m_eval(score, m_const):
    # score  : スコア
    # m_const: 譜面定数
    # return : 評価値 m_eval

    m_eval = 0  # 初期化
    if (score >= 1007500):  # SSS+ -
        m_eval = 2.0 + m_const
    if (score >= 1000000 and score < 1007500):  # SSS -
        m_eval = 1.5 + m_const + 0.5 * (score - 1000000) / 7500
    elif (score >= 990000 and score < 1000000):  # SS -
        m_eval = 1.0 + m_const + 0.5 * (score - 990000) / 10000
    elif (score >= 970000 and score < 990000):  # S -
        m_eval =       m_const + 0.5 * (score - 970000) / 20000
    elif (score >= 940000 and score < 970000):  # AAA -
        # 知らない
        pass
    elif (score >= 900000 and score < 940000):  # AA -
        # 知らない
        pass
    else:
        # しらない
        pass

    return m_eval


sum_new    = 0  # 初期化
sum_new_const = 0
sum_best   = 0
sum_recent = 0
eval_list = []
for i in range(55):
    #  0-14 : 新曲枠
    # 16-44 : ベスト枠
    # 46-54 : リーセント枠
    # 56-64 : ベスト枠外

    label   = elems_label[i].getText()     # 曲名
    level   = elems_level[i].getText()     # レベル
    score   = elems_score[i].getText()     # スコア
    m_const = database.const_dict[label]   # 譜面定数

    score = int(score.replace(",", ""))  # 数値変換処理
    m_const = float(m_const)  # 数値変換処理

    m_eval  = calc_m_eval(score, m_const)  # 評価値

    if   (i <= 14):
        sum_new += m_eval
        sum_new_const += m_const + 2
        eval_list.append([label, math.floor(m_eval*100)/100])
    elif (i <= 44):
        sum_best += m_eval
        eval_list.append([label, math.floor(m_eval*100)/100])
    elif (i <= 54):
        sum_recent += m_eval
        eval_list.append([label, math.floor(m_eval*100)/100])
    else:
        #eval_list.append([label, m_eval])
        pass

ave_new = sum_new / 15        # 新曲枠平均レート
ave_best = sum_best / 30      # best枠平均レート
ave_recent = sum_recent / 10  # recent枠平均レート
disp = (sum_new + sum_best + sum_recent) / 55  # 表示レート
max_new = sum_new_const / 15  # 新曲枠最大レート
disp_new_max = (sum_new_const + sum_best + sum_recent) / 55  # 新曲枠最大レート時の表示レート


print("オンゲキレーティング対象曲 評価値一覧")
for i in range(55):
    if (i <= 14):
        if (i == 0):
            print("******新曲枠*********************************")
        print(eval_list[i][0], ":", eval_list[i][1])
    elif (i <= 44):
        if (i == 15):
            print("******best枠********************************")
        print(eval_list[i][0], ":", eval_list[i][1])
    elif (i <= 54):
        if (i == 45):
            print("******recent枠******************************")
        print(eval_list[i][0], ":", eval_list[i][1])

print("*********************************************")
print("new     ：", math.floor(ave_new*1000)/1000)
print("best    ：", math.floor(ave_best*1000)/1000)
print("recent  ：", math.floor(ave_recent*1000)/1000)
print("rating  ：", math.floor(disp*1000)/1000)
print("new max ：", math.floor(max_new*1000)/1000)
print("rating(new max)：", math.floor(disp_new_max*1000)/1000)

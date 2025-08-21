# ボロノイ図を使うことも可能か？

import random

# import copy
# import time
# import math
# import sys
import cv2
import numpy as np
from scipy import ndimage

is_test = True
margin = 300  # make_final_img用

# np.set_printoptions(threshold=1)


def convert_rgba_to_tf(img: np.array([], dtype=np.uint8)):  # α(不透明度)でtf判定
    img = img[:, :, 3] >= 128
    return img


def convert_bw_to_tf(img: np.array([], dtype=np.uint8), is_white_background=True):
    img = (img <= 128) if is_white_background else (img >= 128)
    return img


def convert_tf_to_bw(img: np.array([], dtype=np.bool)):
    img = img.astype(np.uint8)
    img *= 255
    return img


def show_image(img: np.array([], dtype=np.uint8), title="image"):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return None


def make_final_img(imgs: np.array, hs: int, ws: int):  # 全てリスト
    ret = np.zeros((input_img_H + 600, input_img_W + 600, 4), dtype=np.uint8)
    for img, h, w in zip(imgs, hs, ws):
        H, W, _ = img.shape
        ret[
            h + margin : h + H + margin, w + margin : w + W + margin
        ] += img  # 上下左右にmargin
        if not is_test:
            # 以下がFalseならば桁あふれを起こしている可能性がある
            assert np.all(
                ret[h + margin : h + H + margin, w + margin : w + W + margin] >= img
            )
    ret = ret[margin : input_img_H + margin, margin : input_img_W + margin]
    return ret


def calc_area(img):
    return np.count_nonzero(img)


def calc_score(img: np.array([], dtype=np.bool)):
    global input_img
    img = img.astype(dtype=np.int8)  # -128~127
    local_input_img = input_img.astype(dtype=np.int8)
    # input_imgの内側1点、外側-10点 internal_border上は追加で100点ボーナス
    score = img * (local_input_img * 11 - 10 + input_img_internal_border * 100)
    if is_test:
        assert np.all(-10 <= score) and np.all(score <= 101)
    print(score.dtype)
    return np.sum(score)


input_img_name = "input_img_test.jpeg"
input_img_raw = cv2.imread(input_img_name, cv2.IMREAD_GRAYSCALE)
expansion_rate = 2048 / min(input_img_raw.shape)  # 辺が最低でも2048pixelはあるようにする
input_img_raw = cv2.resize(input_img_raw, None, fx=expansion_rate, fy=expansion_rate)
input_img = convert_bw_to_tf(input_img_raw, is_white_background=True)
input_img_H, input_img_W = input_img.shape
input_img_area = calc_area(input_img)
if is_test:
    input_img_num_of_True = np.count_nonzero(input_img)
    input_img_num_of_False = input_img_H * input_img_W - input_img_num_of_True
    print(f"{input_img_H=},{input_img_W=}")
    print(f"{input_img_num_of_True=}")
    print(f"{input_img_num_of_False=}")
    show_image(convert_tf_to_bw(input_img), title="input_img")


kernel = np.ones((10, 10), np.bool)
input_img_erosion = ndimage.binary_erosion(input_img, structure=kernel)  # 境界内側
# XOR np.boolで境界も管理する
# A and not B   external_borderを除く、内側の境界
input_img_internal_border = input_img ^ input_img_erosion
if is_test:
    print(f"{np.count_nonzero(input_img_internal_border)=}")
# show_image(convert_tf_to_bw(external_border))


component_imgs = [
    cv2.imread(f"{i+1}_trimmed_version3.png", cv2.IMREAD_UNCHANGED) for i in range(47)
]
component_imgs_area = [calc_area(img) for img in component_imgs]
# print(component_imgs_area)

# 米粒猫
number_of_cats = 47

random_coordinates = []
random_coordinates_counter = 0
while True:
    random_coordinate = (
        random.randint(0, input_img_H - 1),
        random.randint(0, input_img_W - 1),
    )
    if input_img[random_coordinate[0]][random_coordinate[1]]:
        random_coordinates.append(random_coordinate)
        random_coordinates_counter += 1
        if random_coordinates_counter == number_of_cats:
            break


print(calc_score(input_img))


imgs = component_imgs  # アフィン変換後の画像群
hs = [random_coordinates[i][0] for i in range(number_of_cats)]  # y軸(左上)
ws = [random_coordinates[i][1] for i in range(number_of_cats)]  # x軸(左上)

final_img = make_final_img(imgs, hs, ws)
show_image(final_img, title="final_img")

# print(img1+img2)
# show_image(img1+img2)

"""
largest_loop_timelimit = 2
step2_timelimit = 0.5
step3_timelimit = 4.8  # 単位はsec

# 関数など


def calc_score(ans: list):
    ret = 0
    for n in range(N):
        a, b, c, d = ans[n][1:]
        r = NXYRs[n][3]
        s = (c-a)*(d-b)
        ret += 1-(1-min(r, s)/max(r, s))**2
    ret *= (10**9/N)
    return round(ret)


def calc_area(a, b, c, d):
    return (c-a)*(d-b)


def is_exceeded(n, a, b, c, d):  # 目標面積(NXYRs[n][3])を超えてしまっているか
    return True if calc_area(a, b, c, d) > NXYRs[n][3] else False


def is_exceeded_three_quarters_area(n, a, b, c, d):  # 目標面積の75%を超えてしまっているか
    return True if calc_area(a, b, c, d) > (NXYRs[n][3]*3 >> 2) else False


def is_overlapping(n, a, b, c, d):  # nabcdは動かした長方形に関するデータ
    for original_nabcd in ans:
        if original_nabcd[0] == n:
            continue
        if a < original_nabcd[3] and c > original_nabcd[1] and\
                b < original_nabcd[4] and d > original_nabcd[2]:
            return True
    else:
        return False


def is_inside_the_frame(coordinate: int):
    return True if 0 <= coordinate < 10000 else False



def append_data_for_visualize(ans):
    global counter_for_visualize
    if time.perf_counter()-start_time >
    deltatime_for_visualize*counter_for_visualize:
        counter_for_visualize += 1
        ans_for_visualize = copy.deepcopy(ans)
        answers_for_visualize.append(ans_for_visualize)
        scores_for_visualize.append(calc_score(ans))


# main
score = 0
number_of_times_largest_loop = 0
while time.perf_counter()-start_time <= largest_loop_timelimit:
    temp_start_time = time.perf_counter()
    ##STEP0 米粒広告##
    ans = [[n, NXYRs[n][1], NXYRs[n][2], NXYRs[n][1]+1, NXYRs[n][2]+1]
           for n in range(N)]

    ##STEP1 拡大もしくは移動 ただし面積の上限は4分の3##
    which_direction_to_extend = 1  # 1なら左に、2なら上に、3なら右に、4なら下に伸ばす
    which_direction_to_move = 1  # 1なら左に 2なら上に 3なら右に 4なら下に動かす
    extend_or_move = True  # Trueはextendを,Falseはmoveを実行することを意味する
    delta = 32
    large_area_NXYRs = sorted(NXYRs, key=lambda x: x[3])[len(NXYRs)//3:]

    step1_number_of_times_loop = 0

    which_direction_to_extend = 1  # 1なら左に、2なら上に、3なら右に、4なら下に伸ばす
    which_direction_to_shorten = 1
    which_direction_to_move = 1  # 1なら左に 2なら上に 3なら右に 4なら下に動かす
    delta = 8
    step2_starttime = step1_endtime
    step2_deltatime = step2_timelimit
    start_temp = 4000
    end_temp = 10
    delta_temp = end_temp-start_temp

    if not is_final:
        step2_number_of_times_loop = 0
        step2_number_of_times_shorten = 0

    while True:
        now = time.perf_counter()-temp_start_time
        if now >= step2_timelimit:
            break

        # 拡大をする
        nabcd = random.choice(ans)
        nabcd[which_direction_to_extend] += (
            delta if which_direction_to_extend >= 3 else -1*delta)
        if is_overlapping(*nabcd) or not(is_inside_the_frame
        (nabcd[which_direction_to_extend])) or is_exceeded(*nabcd):
            nabcd[which_direction_to_extend] -= (
                delta if which_direction_to_extend >= 3 else -1*delta)  # 逆操作
        which_direction_to_extend = (which_direction_to_extend % 4)+1

        # 移動をする
        nabcd = random.choice(ans)
        move_coordinate_1, move_coordinate_2 = (
            (1, 3) if which_direction_to_move & 0b1 == 1 else (2, 4))
        nabcd[move_coordinate_1] += (
            delta if which_direction_to_move >= 3 else -1*delta)
        nabcd[move_coordinate_2] += (
            delta if which_direction_to_move >= 3 else -1*delta)
        if is_overlapping(*nabcd) or\
                not(is_inside_the_frame(nabcd[move_coordinate_1])
                and is_inside_the_frame(nabcd[move_coordinate_2]))\
                or not does_include_the_required_point(*nabcd[1:],
                *NXYRs[nabcd[0]][1:3]):
            # 逆操作
            nabcd[move_coordinate_1] -= (
                delta if which_direction_to_move >= 3 else -1*delta)
            nabcd[move_coordinate_2] -= (
                delta if which_direction_to_move >= 3 else -1*delta)
        which_direction_to_move = (which_direction_to_move % 4)+1

        # 縮小をする
        nabcd = random.choice(ans)
        new_nabcd = copy.copy(nabcd)
        n = new_nabcd[0]
        new_nabcd[which_direction_to_shorten] -= (
            delta if which_direction_to_shorten >= 3 else -1*delta)
        if not does_include_the_required_point(*new_nabcd[1:],
        NXYRs[n][1], NXYRs[n][2]):
            new_nabcd[which_direction_to_shorten] += (
                delta if which_direction_to_shorten >= 3 else -1*delta)  # 逆操作
        which_direction_to_shorten = (which_direction_to_shorten % 4)+1

        new_score = calc_area(*new_nabcd[1:])
        pre_score = calc_area(*nabcd[1:])
        delta_score = new_score-pre_score

        temp = start_temp+delta_temp * \
            (now-step2_starttime)/step2_deltatime  # 温度関数
        prob = math.exp((delta_score)/temp)  # 遷移確率関数

        if prob > random.random():  # 確率probで遷移する
            ans[n] = new_nabcd
            if not is_final and new_score < pre_score:
                step2_number_of_times_shorten += 1

        if not is_final:
            step2_number_of_times_loop += 1
            # if step2_number_of_times_loop%10000==0:
            #  print(f"prob:{prob}")
        if is_for_visualize:
            append_data_for_visualize(ans)

    if not is_final:
        print(f"STEP2_end_time:{time.perf_counter()-start_time}")
        print(f"STEP2_number_of_times_loop:{step2_number_of_times_loop}")
        print(
            f"STEP2_numbere_of_times_shorten:{step2_number_of_times_shorten}")

    # STEP1とSTEP2による結果の内、最良のものを選択
    this_score = calc_score(ans)
    if not is_final:
        print(f"this_score:{this_score}")
    if this_score > score:
        score = this_score
        best_ans = copy.deepcopy(ans)
    number_of_times_largest_loop += 1

if not is_final:
    print(f"number_of_times_largest_loop:{number_of_times_largest_loop}")


if not is_final:
    print(f"STEP3_end_time:{time.perf_counter()-start_time}")

##assertion,及び答えの出力など##
if not is_final:
    assertion()
    print(f"score:{calc_score(ans)}")
    print("-----------------ANSWER------------------")

for n in range(N):
    print(*ans[n][1:])
assert time.perf_counter()-start_time <= 5.0

if is_for_visualize:
    render_images()
"""

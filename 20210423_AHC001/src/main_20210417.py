# ボロノイ図を使うことも可能か？
# dsize=shape

import copy
import datetime
import math
import random
import time

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

is_test = True
is_for_visualize = False
is_debug = True  # 重いassert用
margin = 600  # >=component_imgs_maxhw


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


def calc_area(img):
    return np.count_nonzero(img)


def calc_score(img: np.array([], dtype=np.bool), co_h, co_w):
    # input_imgの内側1点、外側-10点 internal_border上は追加で100点ボーナス
    h, w = img.shape
    assert h != 0 and w != 0
    inner = np.count_nonzero(
        img & input_img_with_margin[co_h : co_h + h, co_w : co_w + w]
    )
    outter = np.count_nonzero(
        img & (~input_img_with_margin[co_h : co_h + h, co_w : co_w + w])
    )
    internal_border = np.count_nonzero(
        img & input_img_internal_border[co_h : co_h + h, co_w : co_w + w]
    )
    assert not (inner == 0 and outter == 0 and internal_border == 0)
    score = inner * 1 + outter * (-10) + internal_border * 100
    return score


def is_overlapping(img, co_h, co_w):
    h, w = img.shape
    try:
        ret = np.any(my_table[co_h : co_h + h, co_w : co_w + w] & img)
        return ret
    except ValueError:
        raise (ValueError(f"{h=},{w=},{co_h=},{co_w=}"))


def make_final_img(answers):  # 全てリスト
    ret = np.zeros(
        (input_img_H + 2 * margin, input_img_W + 2 * margin, 4), dtype=np.uint8
    )
    sum_of_score = 0
    for img, img_num, co_h, co_w, angle, scale, score in answers:
        raw_img = component_imgs_raw[img_num]
        raw_img = cv2.resize(raw_img, None, fx=scale, fy=scale)
        h, w, _ = raw_img.shape
        assert h == w
        affine = cv2.getRotationMatrix2D((w / 2, h / 2), angle=angle, scale=1)
        raw_img = cv2.warpAffine(raw_img, affine, (w, h))
        ret[co_h : co_h + h, co_w : co_w + w] += raw_img
        sum_of_score += score
        if is_test:
            pass
            # 以下がFalseならば桁あふれを起こしている可能性がある
            # assert np.all(ret[co_h:co_h+h, co_w:co_w+w] >= raw_img)
    ret = ret[margin : input_img_H + margin, margin : input_img_W + margin]
    return ret, sum_of_score


def modify_move(img, img_num, co_h, co_w, angle, scale, pre_score, move_delta):
    global my_table  # なぜこれが必要なのかさっぱり分からない
    h, w = img.shape

    if is_debug:
        try:
            assert np.all((my_table[co_h : co_h + h, co_w : co_w + w] & img) == img)
        except AssertionError:
            show_image(convert_tf_to_bw(my_table[co_h : co_h + h, co_w : co_w + w]))
            show_image(convert_tf_to_bw(img))
            raise AssertionError

    # my_tableの移動前の部分を全てFに変換
    my_table[co_h : co_h + h, co_w : co_w + w] = (
        ~img & my_table[co_h : co_h + h, co_w : co_w + w]
    )

    which_direction = random.random()
    if 0.0 <= which_direction < 0.25:
        co_h += move_delta
    elif 0.25 <= which_direction < 0.5:
        co_h -= move_delta
    elif 0.5 <= which_direction < 0.75:
        co_w += move_delta
    else:
        co_w -= move_delta

    if is_overlapping(img, co_h, co_w):
        pass
        co_h = pre_h
        co_w = pre_w
        my_table = pre_my_table
        img = pre_img
        return (None, None)
    else:
        # 衝突が起きない
        my_table[co_h : co_h + h, co_w : co_w + w] = img
        # スコア計算
        new_score = 100
        delta_score = 100  # new_score-pre_score
        return ([img, img_num, co_h, co_w, angle, scale, new_score], delta_score)


# input
input_img_name = "input_img_test.jpeg"
input_img_raw = cv2.imread(input_img_name, cv2.IMREAD_GRAYSCALE)
expansion_rate = 2048 / min(
    input_img_raw.shape
)  # 辺が最低でも2048pixelはあるようにする
input_img_raw = cv2.resize(input_img_raw, None, fx=expansion_rate, fy=expansion_rate)
input_img = convert_bw_to_tf(input_img_raw, is_white_background=True)
input_img_H, input_img_W = input_img.shape
input_img_area = calc_area(input_img)
input_img_with_margin = np.zeros(
    (input_img_H + 2 * margin, input_img_W + 2 * margin), dtype=np.bool
)
input_img_with_margin[margin : input_img_H + margin, margin : input_img_W + margin] = (
    input_img
)
kernel = np.ones((10, 10), np.bool)
input_img_erosion = ndimage.binary_erosion(input_img_with_margin, structure=kernel)
input_img_internal_border = input_img_with_margin ^ input_img_erosion  # XOR
my_table = np.zeros(input_img_with_margin.shape, dtype=np.bool)

# component
component_imgs_raw = [
    cv2.imread(f"{i + 1}_trimmed_version4.png", cv2.IMREAD_UNCHANGED) for i in range(47)
]
# component_imgs_tf = [convert_rgba_to_tf(img) for img in component_imgs_raw]
component_imgs_tf = [
    ndimage.binary_dilation(convert_rgba_to_tf(img), kernel)
    for img in component_imgs_raw
]
component_imgs_bw = [convert_tf_to_bw(img) for img in component_imgs_tf]
component_imgs_area = [calc_area(img) for img in component_imgs_tf]


# answer
answers = []
# answers=[[img,img_num,co_h,co_w,angle,scale,score]]
# co_h,co_wはmargin付きの値
sum_of_components_area = 0
first_step_timelimit = 1
first_step_start_time = time.perf_counter()
while sum_of_components_area < input_img_area * 0.1:
    if time.perf_counter() - first_step_start_time > first_step_timelimit:
        errmsg = "Taking too long time to find first points\n"
        errmsg += "please confirm the input image or so are setup correctly"
        raise AssertionError(errmsg)
    img_num = random.randint(0, len(component_imgs_tf) - 1)
    co_h, co_w = (
        random.randint(margin, margin + input_img_H - 1),
        random.randint(margin, margin + input_img_W - 1),
    )
    angle = 0
    scale = 0.3
    img = convert_bw_to_tf(
        cv2.resize(component_imgs_bw[img_num], None, fx=scale, fy=scale),
        is_white_background=False,
    )
    score = calc_score(img, co_h, co_w)
    if (
        (not input_img_with_margin[co_h, co_w])
        or score <= 0
        or is_overlapping(img, co_h, co_w)
    ):
        continue
    else:
        answer = [img, img_num, co_h, co_w, angle, scale, score]
        answers.append(answer)
        sum_of_components_area += component_imgs_area[img_num]
        h, w = img.shape
        my_table[co_h : co_h + h, co_w : co_w + w] = (
            img | my_table[co_h : co_h + h, co_w : co_w + w]
        )
show_image(convert_tf_to_bw(my_table), title="final_my_table")
final_img, first_score = make_final_img(answers)
show_image(final_img, title="final_img")


# 焼きなまし
start_time = time.perf_counter()
time_limit = 10
start_temp = 10000
end_temp = 10
plt_data_time = []
plt_data_score = []
plt_data_prob = []
time_for_plt = start_time
time_for_movie = start_time
interval_for_plt = 0.01
interval_for_movie = 0.1
answers_for_movie = []
while True:
    now = time.perf_counter()
    if now - time_for_plt > interval_for_plt:
        plt_data_time.append(now - start_time)
        plt_data_score.append(sum([answer[-1] for answer in answers]))
        time_for_plt += interval_for_plt
    if now - time_for_movie > interval_for_movie:
        answer_for_movie = [[None] + answer[1:] for answer in answers]
        answers_for_movie.append(answer_for_movie)
        time_for_movie += interval_for_movie
    if now - start_time >= time_limit:
        break

    answer_num = random.randint(0, len(answers) - 1)
    answer = answers[answer_num]

    which_modify = random.random()
    if 0 <= which_modify < 2:  # 0.5:  # 移動
        move_delta = round(30 * (1 - (now - start_time) / time_limit))
        new_answer, delta_score = modify_move(*answer, move_delta)

    if new_answer is None:
        continue
    else:
        temp = (
            start_temp + (end_temp - start_temp) * (now - start_time) / time_limit
        )  # 温度関数
        if delta_score >= -30:  # 誤差レベルのマイナスまでは無視
            prob = 1
        elif delta_score / temp <= -10:
            prob = 0
        else:
            prob = math.exp((delta_score) / temp)  # 遷移確率関数

        if prob > random.random():  # 確率probで遷移する
            answers[answer_num] = new_answer

final_my_table = ~input_img_with_margin | my_table
show_image(convert_tf_to_bw(final_my_table), title="final_my_table")
if is_test:
    cv2.imwrite("aaa.jpeg", convert_tf_to_bw(my_table))

# 最後
final_img, final_score = make_final_img(answers)
show_image(final_img, title="final_img")
if is_test:
    plt.plot(plt_data_time, plt_data_score)
    plt.title("score graph")
    plt.xlabel("time/s")
    plt.ylabel("score/a.u.")
    plt.show()
if is_for_visualize:
    imgs_for_movie = [make_final_img(answers) for answers in answers_for_movie]
    filename = datetime.datetime.now().strftime("%H%M%S")
    fps = 4.0
    total_frames = round(time_limit / interval_for_movie)
    make_movie(filename=filename, fps=fps, total_frames=total_frames)

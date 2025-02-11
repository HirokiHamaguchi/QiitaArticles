import cv2
import math
import numpy as np


def convert_tf_to_bw(img: np.array([], dtype=bool)):
    img = img.astype(np.uint8)
    img = img[:, :, np.newaxis]
    img = np.tile(img, reps=(1, 1, 3))
    img *= 255
    return img


def convert_png_to_tf(img: np.array([], dtype=np.uint8)):
    img = (img[:, :, 3] == 255)
    return img


def trim(name: int):
    img = cv2.imread(f"{name}_trimmed_version3.png",
                     cv2.IMREAD_UNCHANGED)  # α付きで読み込む
    contours, hierarchy = cv2.findContours(img[:, :, 3], cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)  # 境界抽出
    max_area = 0
    for cnt in contours:  # 手作業での切り出しではゴミが含まれてしまっているので、一番面積の多い部分を選択する。
        x, y, w, h = cv2.boundingRect(cnt)
        if h*w > max_area:
            max_area = h*w
            X, Y, W, H = x, y, w, h
    img = img[Y:Y+H, X:X+W]
    for i, row in enumerate(img):
        for j, pixel in enumerate(row):
            if not pixel[3] in (0, 255):
                img[i][j][3] = 0 if pixel[3] < 128 else 255
            if np.array_equal(pixel, [255, 255, 255, 0]):
                img[i][j] = np.array([0, 0, 0, 0])
    return img


def add_margin(img: np.array([], dtype=np.uint8)):  # 回転しても切れない様に余白追加
    h, w, _ = img.shape
    r = math.ceil(math.sqrt(h**2+w**2))
    ret = np.zeros((r, r, 4), dtype=np.uint8)
    ret[(r-h)//2:(r-h)//2+h, (r-w)//2:(r-w)//2+w] += img
    return ret


for i in range(47):
    print(f"{i/47:.0%}")
    image = trim(i+1)
    image = add_margin(image)
    cv2.imwrite(f"{i+1}_trimmed_version4.png", image)
else:
    print("finished")

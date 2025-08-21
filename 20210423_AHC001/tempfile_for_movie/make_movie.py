import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw


def img_add_msg(img, message, position, color, fontsize=20):
    fontpath = "C:\\Windows\\Fonts\\msmincho.ttc"  # Windowsのフォントファイルへのパス
    font = ImageFont.truetype(fontpath, fontsize)  # PILでフォントを定義
    # cv2(NumPy)型の画像をPIL型に変換
    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)  # 描画用のDraw関数を用意

    # テキストを描画（位置、文章、フォント、文字色（BGR+α）を指定）
    draw.text(position, message, font=font, fill=(color, color, color, 1))
    # PIL型の画像をcv2(NumPy)型に変換
    img = np.array(img)
    return img  # 文字入りの画像をリターン


def make_movie(filename: str(int), fps: float):
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # コーデックを定める
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    shape = cv2.imread(f"{filename}_0.jpeg", cv2.IMREAD_GRAYSCALE).shape
    print(shape)
    video = cv2.VideoWriter("MOVIE_211845.mp4", fourcc, fps, shape)
    for i in range(10):
        img = cv2.imread(f"{filename}_{i}.jpeg")
        if img is None:  # imgが存在しなければNone,つまりFalse
            assert i != 0
            break
        # img = img_add_msg(img, f"{i/fps}s", (50, 50), color=1, fontsize=50)
        video.write(img)
    video.release()
    print("finished")


make_movie(filename=211845, fps=10.0)

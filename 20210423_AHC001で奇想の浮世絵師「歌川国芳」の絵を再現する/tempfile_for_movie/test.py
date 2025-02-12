import cv2
import numpy as np

# 幅
W = 1024
# 高さ
H = 1024
# FPS（Frame Per Second：１秒間に表示するFrame数）
CLIP_FPS = 20.0
# テスト用の背景色
BG_COLOR = (79, 62, 70)

filepath = 'test2.mp4'
codec = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(filepath, codec, CLIP_FPS, (W, H))

for i in range(10):
    # イメージデータの領域確保
    # img = np.zeros((H, W, 3), np.uint8)
    # 背景色で塗りつぶし
    #img = cv2.rectangle(img, (0, 0), (W-1, H-1), BG_COLOR, -1)
    img = cv2.imread(f"211845_{i}.jpeg")
    img = cv2.resize(img, dsize=(1024, 1024))
    print(img.shape)
    video.write(img)

video.release()

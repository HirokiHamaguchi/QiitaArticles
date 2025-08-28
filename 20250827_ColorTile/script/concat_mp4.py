from moviepy import (  # type: ignore
    CompositeVideoClip,
    TextClip,
    VideoFileClip,
    concatenate_videoclips,
)

# 入力リスト
inputs = [
    ("imgs/tmp/gif_0.mp4", "ランダム戦略"),
    ("imgs/tmp/gif_1.mp4", "垂直戦略"),
    ("imgs/tmp/gif_2.mp4", "水平戦略"),
    ("imgs/tmp/gif_3.mp4", "斜め戦略"),
    ("imgs/tmp/gif_4.mp4", "四隅戦略"),
    ("imgs/tmp/gif_5.mp4", "斜め双方向戦略"),
]

percentages = [5.6, 7.7, 9.6, 12.6, 13.9, 18.8]

final_clips = []
video_sizes = []

for i, (video_path, strategy_name) in enumerate(inputs):
    print(f"Processing {strategy_name} from {video_path}")

    video_clip = VideoFileClip(video_path)
    video_sizes.append(video_clip.size)

    w, h = video_clip.size
    strategy_font_size = h // 5  # 戦略名
    percentage_font_size = h // 10  # 達成率
    percentage_text = f"(全消し達成率: {percentages[i]}%)"

    # 戦略名Clip
    strategy_clip = TextClip(
        font="meiryo.ttc",
        text=strategy_name,
        font_size=strategy_font_size,
        color="black",
        method="caption",
        size=(w, int(strategy_font_size * 1.5)),
    )

    # 達成率Clip
    percentage_clip = TextClip(
        font="meiryo.ttc",
        text=percentage_text,
        font_size=percentage_font_size,
        color="black",
        method="caption",
        size=(w, int(percentage_font_size * 1.5)),
    )

    # 上下2段を中央に配置
    total_height = strategy_font_size + percentage_font_size
    strategy_clip = strategy_clip.with_position(
        ("center", (h - total_height) // 2 - percentage_font_size)
    )
    percentage_clip = percentage_clip.with_position(
        ("center", (h - total_height) // 2 + strategy_font_size)
    )

    # 背景白のClip作成
    bg_clip = TextClip(text="", size=(w, h), color="white", duration=2)

    # 合成
    txt_clip = CompositeVideoClip(
        [bg_clip, strategy_clip, percentage_clip],
        bg_color=(255, 255, 255),
    ).with_duration(4)

    final_clips.extend([txt_clip, video_clip])

# 全動画のサイズが同じであることを確認
assert all(size == video_sizes[0] for size in video_sizes), "動画サイズが揃っていません"

# すべてのクリップを結合
final_video = concatenate_videoclips(final_clips)

# 出力
final_video.write_videofile("imgs/strategies.mp4", codec="libx264", fps=24)

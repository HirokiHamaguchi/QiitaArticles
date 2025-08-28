#!/bin/bash

OUTPUT="imgs/strategies.mp4"

WORKDIR="imgs/tmp"
mkdir -p "$WORKDIR"

INPUTS=(
  "imgs/strategy_gifs/Random_AvoidTriple_all_clear.gif:ランダム戦略"
  "imgs/strategy_gifs/Vertical_AvoidTriple_all_clear.gif:垂直戦略"
  "imgs/strategy_gifs/Horizontal_AvoidTriple_all_clear.gif:水平戦略"
  "imgs/strategy_gifs/Diagonal_AvoidTriple_all_clear.gif:斜め戦略"
  "imgs/strategy_gifs/Corner_AvoidTriple_all_clear.gif:四隅戦略"
  "imgs/strategy_gifs/Bidirectional_AvoidTriple_all_clear.gif:斜め双方向戦略"
)

INDEX=0
for ITEM in "${INPUTS[@]}"; do
    GIFPATH="${ITEM%%:*}"
    TEXT="${ITEM#*:}"

    OUTGIF="$WORKDIR/gif_$INDEX.mp4"
    /mnt/c/Users/hirok/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.0-full_build/bin/ffmpeg.exe -y -i "$GIFPATH" -movflags faststart -pix_fmt yuv420p "$OUTGIF"

    INDEX=$((INDEX+1))
done

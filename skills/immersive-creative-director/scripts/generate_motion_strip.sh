#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 3 ]]; then
  echo "usage: generate_motion_strip.sh <frame-dir> <comma-separated-frame-numbers> <output.jpg>" >&2
  exit 2
fi

frame_dir=$1
frame_numbers=$2
output_path=$3
IFS=',' read -r -a selected_frames <<< "$frame_numbers"

if [[ ${#selected_frames[@]} -lt 5 || ${#selected_frames[@]} -gt 12 ]]; then
  echo "select 5-12 chronological frames" >&2
  exit 2
fi

mkdir -p "$(dirname "$output_path")"
ffmpeg_args=()
filter_parts=()
layout_parts=()

for frame_index in "${!selected_frames[@]}"; do
  frame_number=${selected_frames[$frame_index]}
  frame_path=$(printf "%s/frame-%03d.jpg" "$frame_dir" "$frame_number")
  [[ -f "$frame_path" ]] || { echo "missing $frame_path" >&2; exit 1; }
  ffmpeg_args+=( -i "$frame_path" )
  filter_parts+=( "[$frame_index:v]scale=480:270:force_original_aspect_ratio=decrease,pad=480:270:(ow-iw)/2:(oh-ih)/2:black[v$frame_index]" )
  column=$((frame_index % 4))
  row=$((frame_index / 4))
  layout_parts+=( "$((column * 480))_$((row * 270))" )
done

inputs=""
for frame_index in "${!selected_frames[@]}"; do inputs+="[v$frame_index]"; done
filter=$(IFS=';'; echo "${filter_parts[*]};${inputs}xstack=inputs=${#selected_frames[@]}:layout=$(IFS='|'; echo "${layout_parts[*]}"):fill=black[out]")

ffmpeg -hide_banner -loglevel error "${ffmpeg_args[@]}" -filter_complex "$filter" -map "[out]" -frames:v 1 -q:v 3 -y "$output_path"

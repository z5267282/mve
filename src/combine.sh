ls -1 -tr hsieh/* | sed -E 's/^/file /' > clips.txt
# taken from: https://medium.com/@3valuedlogic/how-to-concatenate-video-clips-with-ffmpeg-db77ac797913
ffmpeg -f concat -i clips.txt ffmpeg.mp4

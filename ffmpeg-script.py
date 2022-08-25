import subprocess

name = 'jisoo.mp4'
# start, end  = '00:00:02', '00:00:08'
# start, end = '60', '63'
start, end = '00:00:57', '00:01:09'
out = 'dog.mp4'

args = ['ffmpeg', '-y', '-i', name, '-ss', start, '-to', end, out]

# last n seconds
# args = ['ffmpeg', '-y', '-sseof', '-10', '-i', name,  out]

subprocess.run(args)


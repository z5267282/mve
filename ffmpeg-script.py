import subprocess

name = 'Cirstea vs Watson.mp4'
# start, end  = '00:00:02', '00:00:08'
start, end = '00:00:00', '63'
out = 'fish.mp4'

args = ['ffmpeg', '-ss', start, '-i', name, '-to', end, '-codec', 'copy', '-copyts', '-y', out]

subprocess.run(args)


import subprocess

name = 'Cirstea vs Watson.mp4'
start = '00:00:02'
end = '00:00:08'
out = 'fish.mp4'

args = ['ffmpeg', '-ss', start, '-i', name, '-to', end, '-codec', 'copy', '-copyts', '-y', out]

subprocess.run(args)

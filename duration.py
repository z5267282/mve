import subprocess

name = 'Cirstea vs Watson.mp4'

args = [
    'ffprobe',
    '-i',
    name,
    '-v',
    'quiet',
    '-show_entries',
    'format=duration',
    '-hide_banner',
    '-of',
    'default=noprint_wrappers=1:nokey=1'
]

result = subprocess.run(args, capture_output=True, text=True)
# note that there is a newline at the end of stdout
print(result.stdout.strip())
print(result.returncode)

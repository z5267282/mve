import moviepy.editor as mvp
import os.path

def editvideo(oldname, newname, start, end=None):
    with mvp.VideoFileClip(oldname) as full:
        clip = full.subclip(t_start=start, t_end=end)
       
        numthreads = 8
        frames = 60
        vcodec = "libx264"
        compression = "slower"
        acodec = 'aac' 

        clip.write_videofile(
            newname, threads=numthreads, fps=frames, codec=vcodec, preset=compression, audio_codec=acodec
        )

editvideo(
    # "D:\Videos\Team Fortress 2\Team Fortress 2 2022.05.10 - 22.39.04.06.DVR.mp4",

    os.path.expanduser(os.path.join('~', 'Downloads', 'jisoo fancam.mp4')),
    "testing.mp4",
    -5
)

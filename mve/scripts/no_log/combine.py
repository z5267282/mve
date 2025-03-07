
import argparse
import contextlib
import os

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips


import mve.src.constants.video_editing as video_editing

from mve.scripts.script import NotLoggedScript
from mve.scripts.script_option import ScriptOption


class Combine(NotLoggedScript):
    '''Combine multiple clips from a given folder into a single video file.'''

    def __init__(self):
        super().__init__(str(ScriptOption.COMBINE))

    def main(self, argv: list[str]) -> None:
        parser = argparse.ArgumentParser(prog=self.generate_usage_name())
        parser.add_argument(
            'source', type=str, help='the absolute file path of the folder with the clips')
        parser.add_argument(
            'title', type=str, help='the raw base filename of the combined montage without a file suffix')
        args = parser.parse_args(argv)

        # we should order by clip creation time
        video_files = sorted([os.path.join(args.source, f)
                              for f in os.listdir(args.source)], key=lambda f: os.stat(f).st_birthtime)
        with contextlib.ExitStack() as videos:
            # there is no audio, I think because of the configuration of VideoFileClip?
            clips = [videos.enter_context(VideoFileClip(v, audio=True))
                     for v in video_files]

            combined = concatenate_videoclips(clips, method='compose')
            # these are needed to make audio available
            # alternatively, the video can be opened using VLC
            # https://stackoverflow.com/questions/40445885/no-audio-when-adding-mp3-to-videofileclip-moviepy
            combined.write_videofile(f'{args.title}.{video_editing.SUFFIX}',
                                     codec=video_editing.VCODEC,
                                     audio_codec='aac',
                                     temp_audiofile='temp-audio.m4a',
                                     remove_temp=True)

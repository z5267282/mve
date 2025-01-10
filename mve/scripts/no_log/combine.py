
import argparse
import contextlib
import os

import moviepy.editor as mvp

import mve.src.constants.video_editing as video_editing

from mve.scripts.script import Script


class Combine(Script):
    '''Combine multiple clips from a given folder into a single video file.'''

    def main(self, argv: list[str]) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument('source', type=str)
        parser.add_argument(
            'title', type=str, help='the raw base filename of the combined montage without a file suffix')
        args = parser.parse_args(argv)

        # we should order by clip creation time
        video_files = sorted([os.path.join(args.source, f)
                              for f in os.listdir(args.source)], key=lambda f: os.stat(f).st_birthtime)
        with contextlib.ExitStack() as videos:
            # there is no audio, I think because of the configuration of VideoFileClip?
            clips = [videos.enter_context(mvp.VideoFileClip(v, audio=True))
                     for v in video_files]

            combined = mvp.concatenate_videoclips(clips, method='compose')
            # these are needed to make audio available
            # alternatively, the video can be opened using VLC
            # https://stackoverflow.com/questions/40445885/no-audio-when-adding-mp3-to-videofileclip-moviepy
            combined.write_videofile(f'{args.title}.{video_editing.SUFFIX}',
                                     codec=video_editing.VCODEC,
                                     audio_codec='aac',
                                     temp_audiofile='temp-audio.m4a',
                                     remove_temp=True)

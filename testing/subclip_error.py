import moviepy.editor as mvp

def handle_clip(src_full_path, success_handler, start, end):
    error = None
    with mvp.VideoFileClip(src_full_path) as file:
        try:
            clip = file.subclip(t_start=start, t_end=end)
            success_handler(clip)
        except IOError as e:
            error = str(e)

    return error

def main():
    y = handle_clip('../jisoo.mp4', print, 0, '59:00')
    print('\n')
    print(f'error:\n{y}')

if __name__ == '__main__':
    main()

import os

def ls(paths_list):
    path = os.path.join(*paths_list)
    return os.listdir(path)

def main():
    cwd = ['D:', 'Videos', 'Batches', '1']

    items = sorted(ls(cwd), key=lambda f: os.path.getctime(os.path.join(*(cwd + [f]))))
    for i in items:
        print(i)

if __name__ == '__main__':
    main()

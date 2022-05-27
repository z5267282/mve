import os

def ls(paths_list):
    path = os.path.join(*paths_list)
    return os.listdir(path)

def main():
    cwd = [
        "Users",
        "sunny",
        "OneDrive - UNSW",
        "Code",
        "Projects",
        "mve",
        "src"
    ]

    print(ls(cwd))

if __name__ == '__main__':
    main()

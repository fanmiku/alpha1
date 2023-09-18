__all__ = ["makedirs_if_not_exists","walk_files"]
import os

def makedirs_if_not_exists(dir_):
    if not os.path.exists(dir_):
        os.makedirs(dir_)

def walk_files(root, extension):
    for path, dirs, files in os.walk(root):
        for file in files:
            if file.endswith(extension):
                yield os.path.join(path, file)

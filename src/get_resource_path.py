import os
import sys


# https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741
def get_resource_path(relative_path):
    dir = os.path.dirname(os.path.abspath(__file__))
    base = getattr(sys, "_MEIPASS", dir)
    return os.path.join(base, relative_path)

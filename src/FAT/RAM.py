# yes you heard it... RAM. #
# RAM.py #
# UNUSED LOLOLOL [not anymore!]

import os, pickle
from FAT.fs import getRoot, getCwd

IMG_PATH = os.path.join(os.path.dirname(__file__), "../deuteric.img")
root = getRoot()
cwd = getCwd()

def load_fs():
    global root, cwd
    if os.path.exists(IMG_PATH):
        with open(IMG_PATH, "rb") as f:
            root = pickle.load(f)
            cwd = root
        print(f"FS loaded from image, length: {os.path.getsize(IMG_PATH)} bytes")
    else:
        print("No FS image found, starting fresh")

def save_fs():
    with open(IMG_PATH, "wb") as f:
        pickle.dump(root, f)
    print("FS saved to image, length:", os.path.getsize(IMG_PATH))

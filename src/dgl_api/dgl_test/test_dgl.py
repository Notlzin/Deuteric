# test_dgl.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from dgl_api.dgl import dGL


def main(gfx):
    gfx.dglDrawRect(100, 100, 150, 80, (255, 100, 0))
    gfx.dglDrawCircle(300, 200, 60, (0, 150, 255))

if __name__ == "__main__":
    gfx = dGL(640, 480, "dGL:GPU_edition")
    gfx.dglRun(main)

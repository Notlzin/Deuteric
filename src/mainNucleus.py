# main_nucleus.py #
# this runs the bootloader then kernel #
import sys
import os
sys.path.insert(0,os.getcwd())

# main loop #
if __name__ == "__main__":
    from bootloader_package.bootloader import Boot # type: ignore #
    Boot()

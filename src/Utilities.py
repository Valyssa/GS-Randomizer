import sys
import os

# Load hack using either python or pyinstaller
def open_bin(relative_path):
    if os.path.isfile(relative_path):
        filename = relative_path
    else:
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        filename = os.path.join(base_path, relative_path)

    with open(filename, 'rb') as file:
        binfile = bytearray(file.read())

    return binfile

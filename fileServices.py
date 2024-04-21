import os
import subprocess

# Func: Open File
def open_file(file_path):
    try:
        # subprocess.run(["xdg-open", file_path])
        os.startfile(file_path)
    except Exception:
        return 0
    return 1

# Func: Delete File
def delete_file(path):
    try:
        os.remove(path)
    except Exception:
        return 0
    return 1
    
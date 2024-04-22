import os
import subprocess

def clean_path(file_path):
    return file_path.replace("\\","\\\\").strip("\n")

# Func: Open File
def open_file(file_path):
    file_path = clean_path(file_path)
    try:
        subprocess.run(["xdg-open", file_path])
    except Exception:
        try:
            os.startfile(file_path)
        except Exception:    
            return 0
    return 1

# Func: Delete File
def delete_file(file_path):
    file_path = clean_path(file_path)
    try:
        os.remove(file_path)
    except Exception:
        return 0
    return 1
    
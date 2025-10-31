import os
from config import FS_ROOT

def _to_os_path(user_path: str) -> str:
    # normalize user path
    rel = user_path.lstrip("/")  # "/docs/a.txt" -> "docs/a.txt"
    full = os.path.join(FS_ROOT, rel)
    # prevent ../../ escape
    full = os.path.abspath(full)
    root = os.path.abspath(FS_ROOT)
    if not full.startswith(root):
        raise ValueError("path escape detected")
    return full

def fs_list(path: str):
    os_path = _to_os_path(path)
    if not os.path.isdir(os_path):
        raise FileNotFoundError(f"{path} is not a directory")
    return os.listdir(os_path)

def fs_read(path: str) -> str:
    os_path = _to_os_path(path)
    with open(os_path, "r", encoding="utf-8") as f:
        return f.read()

def fs_write(path: str, data: str):
    os_path = _to_os_path(path)
    # ensure parent exists
    parent = os.path.dirname(os_path)
    os.makedirs(parent, exist_ok=True)
    with open(os_path, "w", encoding="utf-8") as f:
        f.write(data)

def fs_mkdir(path: str):
    os_path = _to_os_path(path)
    os.makedirs(os_path, exist_ok=True)

def fs_delete(path: str):
    os_path = _to_os_path(path)
    if os.path.isdir(os_path):
        # simple: only delete empty dirs
        os.rmdir(os_path)
    else:
        os.remove(os_path)

def fs_stat(path: str):
    os_path = _to_os_path(path)
    st = os.stat(os_path)
    return {
        "size": st.st_size,
        "is_dir": os.path.isdir(os_path),
    }

import sys
from fs import fs_write, fs_read, fs_list, fs_mkdir
from config import FS_ROOT
import os

HELP = """Usage:
  python demo.py write <path> <text>
  python demo.py read  <path> <k_user_hex>
  python demo.py ls    <path>
  python demo.py mkdir <path>

Examples:
  python demo.py write /docs/hello.txt "hello zero trust"
  # (copy the printed key)
  python demo.py read /docs/hello.txt <that-key>
"""

def main():
    if len(sys.argv) < 2:
        print(HELP)
        return

    cmd = sys.argv[1]

    if cmd == "write":
        if len(sys.argv) < 4:
            print("need path and text")
            return
        path = sys.argv[2]
        text = " ".join(sys.argv[3:])
        k_user_hex = fs_write(path, text)
        print("File written.")
        print("Your user key (SAVE THIS):")
        print(k_user_hex)

    elif cmd == "read":
        if len(sys.argv) != 4:
            print("need path and k_user_hex")
            return
        path = sys.argv[2]
        k_user_hex = sys.argv[3]
        plaintext = fs_read(path, k_user_hex)
        print("Decrypted contents:")
        print(plaintext)

    elif cmd == "ls":
        if len(sys.argv) != 3:
            print("need path to list")
            return
        path = sys.argv[2]
        items = fs_list(path)
        for name in items:
            print(name)

    elif cmd == "mkdir":
        if len(sys.argv) != 3:
            print("need path to create")
            return
        path = sys.argv[2]
        fs_mkdir(path)
        print("directory created")

    else:
        print(HELP)


if __name__ == "__main__":
    # just sanity: show where FS_ROOT is
    if not os.path.exists(FS_ROOT):
        os.makedirs(FS_ROOT, exist_ok=True)
    main()
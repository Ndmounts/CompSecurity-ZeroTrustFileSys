import sys
import os
from fs import create_file, fs_write, fs_read, fs_list, fs_mkdir
from config import FS_ROOT

HELP = """Usage:
  python demo.py create <path> <text>
  python demo.py write  <path> <k_user_hex> <text>
  python demo.py read   <path> <k_user_hex>
  python demo.py ls     <path>
  python demo.py mkdir  <path>

Examples:
  # create a brand new encrypted file (server entry + new user key)
  python demo.py create /docs/hello.txt "hello zero trust"

  # copy the printed key, then later update the same file:
  python demo.py write /docs/hello.txt <that-key> "new contents"

  # read it back
  python demo.py read /docs/hello.txt <that-key>
"""


def main():
    if len(sys.argv) < 2:
        print(HELP)
        return

    cmd = sys.argv[1]

    if cmd == "create":
        if len(sys.argv) < 4:
            print("need path and text")
            return
        path = sys.argv[2]
        text = " ".join(sys.argv[3:])
        k_user_hex = touch_request(path, text)
        print("File created.")
        print("Your user key (SAVE THIS):")
        print(k_user_hex)

    elif cmd == "write":
        # write to an existing encrypted file
        if len(sys.argv) < 5:
            print("need path, k_user_hex, and text")
            return
        path = sys.argv[2]
        k_user_hex = sys.argv[3]
        text = " ".join(sys.argv[4:])
        write_request(path, text, k_user_hex)
        print("File updated.")

    elif cmd == "read":
        if len(sys.argv) != 4:
            print("need path and k_user_hex")
            return
        path = sys.argv[2]
        k_user_hex = sys.argv[3]
        plaintext = view_request(path, k_user_hex)
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
        mkdir_request(path)
        print("directory created")

    else:
        print(HELP)


if __name__ == "__main__":
    # make sure FS_ROOT exists
    if not os.path.exists(FS_ROOT):
        os.makedirs(FS_ROOT, exist_ok=True)
    main()

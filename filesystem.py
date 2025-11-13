import os
from config import FS_ROOT

from encryptions import (
    server_register_file,
    server_store_encrypted,
    server_retrieve,
    client_encrypt_file,
    client_encrypt_file_with_user_key,
    client_decrypt_file,
)

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

def create_file(path: str, data: str) -> str:
    """
    Create a new encrypted file.
    - Registers a new file_id on the server
    - Generates a new user key (K_user)
    - Encrypts data and uploads ciphertext
    - Writes .meta with file_id
    Returns the user's key (hex string)
    """
    os_path = _to_os_path(path)
    parent = os.path.dirname(os_path)
    os.makedirs(parent, exist_ok=True)

    # Register new file on the server
    file_id, k_server_hex = server_register_file()

    # Encrypt with a new user key
    file_id, k_user_hex, enc, nonce = client_encrypt_file(
        data.encode("utf-8"), k_server_hex
    )

    # Upload encrypted file to the server
    server_store_encrypted(file_id, enc, nonce)

    # Store metadata locally
    with open(os_path + ".meta", "w") as meta:
        meta.write(file_id)

    # Save encrypted file locally
    with open(os_path, "wb") as f:
        f.write(enc)

    return k_user_hex

def fs_write(path: str, data: str, k_user_hex: str):
    """
    Write to an existing encrypted file.
    - Reads .meta to get the file_id
    - Uses the provided user key to encrypt new content
    - Updates ciphertext on both local and server sides
    """
    os_path = _to_os_path(path)
    meta_path = os_path + ".meta"

    if not os.path.exists(meta_path):
        raise FileNotFoundError("No existing file metadata found. Use create_file().")

    # Retrieve existing server info
    with open(meta_path, "r") as meta:
        file_id = meta.read().strip()

    k_server_hex, _, _ = server_retrieve(file_id)

    # Encrypt new content
    file_id, enc, nonce = client_encrypt_file_with_user_key(
        data.encode("utf-8"), k_server_hex, k_user_hex
    )

    # Upload to server and update local storage
    server_store_encrypted(file_id, enc, nonce)

    with open(os_path, "wb") as f:
        f.write(enc)

    print(f"File '{path}' updated successfully.")

def fs_read(path: str, k_user_hex: str) -> str:
    """
    Read and decrypt an encrypted file.
    Requires user's key share (k_user_hex).
    """
    os_path = _to_os_path(path)
    meta_path = os_path + ".meta"

    if not os.path.exists(meta_path):
        raise FileNotFoundError("Missing metadata for encrypted file")

    # Retrieve the server metadata
    with open(meta_path, "r") as meta:
        file_id = meta.read().strip()

    k_server_hex, enc, nonce = server_retrieve(file_id)

    # Client performs decryption locally
    plaintext = client_decrypt_file(k_user_hex, k_server_hex, enc, nonce)
    return plaintext.decode("utf-8")

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

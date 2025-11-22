import secrets
import hashlib
import pickle
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Server-side persistent storage
DB_FILE = Path("server_db.pkl")

def load_db() -> dict:
    """Load the database from disk, or create an empty one."""
    if DB_FILE.exists():
        with DB_FILE.open("rb") as f:
            return pickle.load(f)
    return {}

def save_db(db: dict):
    """Save the database back to disk."""
    with DB_FILE.open("wb") as f:
        pickle.dump(db, f)

DB = load_db()

# Utility functions
def xor_bytes(a: bytes, b: bytes) -> bytes:
    """XOR two byte strings of equal length."""
    return bytes(x ^ y for x, y in zip(a, b))

def _hash_file_id(data: bytes) -> str:
    """Generate a unique file ID for lookup."""
    return hashlib.sha256(data).hexdigest()


# Server Functions
def server_register_file() -> tuple[str, str]:
    """
    Simulate server registering a new file.
    Generates a K_server, returns it to the client.
    """
    K_server = secrets.token_bytes(32)
    file_id = _hash_file_id(K_server)
    DB[file_id] = {
        "k_server_hex": K_server.hex(),
        "nonce": None,
        "enc": None,
    }
    save_db(DB)
    return file_id, K_server.hex()


def server_store_encrypted(file_id: str, enc: bytes, nonce: bytes):
    """Store the ciphertext and nonce uploaded by the client."""
    if file_id not in DB:
        raise ValueError("File not registered on server")
    DB[file_id]["enc"] = enc
    DB[file_id]["nonce"] = nonce
    save_db(DB)

def server_retrieve(file_id: str):
    """Return the server’s key share and encrypted file for a valid file_id."""
    record = DB.get(file_id)
    if not record:
        raise ValueError("No record found for that file ID")
    return record["k_server_hex"], record["enc"], record["nonce"]

# Client Functions (local encryption/decryption)
def client_encrypt_file_with_user_key(
    plaintext: bytes,
    k_server_hex: str,
    k_user_hex: str,
) -> tuple[str, bytes, bytes]:
    """
    Same as client_encrypt_file but caller supplies k_user_hex.
    Returns (file_id, enc, nonce)
    """
    K_user = bytes.fromhex(k_user_hex)
    K_server = bytes.fromhex(k_server_hex)
    K = xor_bytes(K_user, K_server)

    nonce = secrets.token_bytes(12)
    enc = AESGCM(K).encrypt(nonce, plaintext, None)
    file_id = _hash_file_id(K_server)
    return file_id, enc, nonce

def client_encrypt_file(plaintext: bytes, k_server_hex: str) -> tuple[str, str, bytes, bytes]:
    """
    Perform local (client-side) encryption.
    - Generates K_user
    - Combines K_user and K_server -> K
    - Encrypts plaintext locally
    - Returns (file_id, K_user_hex, enc, nonce)
    """
    K_user = secrets.token_bytes(32)
    K_server = bytes.fromhex(k_server_hex)
    K = xor_bytes(K_user, K_server)

    nonce = secrets.token_bytes(12)
    enc = AESGCM(K).encrypt(nonce, plaintext, None)
    file_id = _hash_file_id(K_server)

    return file_id, K_user.hex(), enc, nonce


def client_decrypt_file(k_user_hex: str, k_server_hex: str, enc: bytes, nonce: bytes) -> bytes:
    """Client-side decryption (server never sees plaintext)."""
    K_user = bytes.fromhex(k_user_hex)
    K_server = bytes.fromhex(k_server_hex)
    K = xor_bytes(K_user, K_server)
    return AESGCM(K).decrypt(nonce, enc, None)

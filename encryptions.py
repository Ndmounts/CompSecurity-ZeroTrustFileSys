import secrets
import hashlib
import pickle
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ------------------------------------------------------------
# Server-side storage (persistent)
# ------------------------------------------------------------
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

DB = load_db()  # global dictionary (user_key_hash -> metadata)

# ------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------
def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def _hash_user_key(k_user: bytes) -> str:
    """Stable identifier for this user's file key."""
    return hashlib.sha256(k_user).hexdigest()

# ------------------------------------------------------------
# Core functions
# ------------------------------------------------------------
def create_encrypted_file(plaintext: bytes) -> str:
    """Simulates server creating an encrypted file."""
    K_user = secrets.token_bytes(32)    # given to user
    K_server = secrets.token_bytes(32)  # kept by server
    K = xor_bytes(K_user, K_server)

    nonce = secrets.token_bytes(12)
    enc = AESGCM(K).encrypt(nonce, plaintext, None)

    user_key_hash = _hash_user_key(K_user)

    DB[user_key_hash] = {
        "k_server_hex": K_server.hex(),
        "nonce": nonce,
        "enc": enc,
    }

    save_db(DB)  # persist changes
    return K_user.hex()  # return only the user key

def retrieve_for_user(k_user_hex: str) -> bytes:
    """Simulates server retrieving and decrypting a file."""
    K_user = bytes.fromhex(k_user_hex)
    user_key_hash = _hash_user_key(K_user)

    record = DB.get(user_key_hash)
    if not record:
        raise ValueError("No record found for this user key")

    K_server = bytes.fromhex(record["k_server_hex"])
    K = xor_bytes(K_user, K_server)

    pt = AESGCM(K).decrypt(record["nonce"], record["enc"], None)
    return pt
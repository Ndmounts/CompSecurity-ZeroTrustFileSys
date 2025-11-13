import sys
import json
import pickle
from pathlib import Path

DB_FILE = Path("server_db.pkl")


def load_db() -> dict:
    """Load the database from disk."""
    if not DB_FILE.exists():
        raise FileNotFoundError(f"{DB_FILE} not found")
    with DB_FILE.open("rb") as f:
        return pickle.load(f)


def record_to_export(file_id: str, record: dict) -> dict:
    """
    Convert an internal record to a simple export format that can be used
    with other libraries (e.g., OpenSSL bindings in another language).
    """
    return {
        "file_id": file_id,
        "k_server_hex": record["k_server_hex"],        # hex string
        "nonce_hex": record["nonce"].hex(),            # bytes -> hex
        "enc_hex": record["enc"].hex(),                # bytes -> hex
    }


def main():
    """
    Usage:
      python export_for_openssl.py             # dump all records as JSON lines
      python export_for_openssl.py <file_id>   # dump only one record
    """
    db = load_db()

    if len(sys.argv) == 2:
        # Specific file_id
        file_id = sys.argv[1]
        record = db.get(file_id)
        if not record:
            print(f"No record found for file_id: {file_id}")
            sys.exit(1)
        export = record_to_export(file_id, record)
        print(json.dumps(export, indent=2))
    else:
        # Dump all records as one JSON array
        exports = [record_to_export(fid, rec) for fid, rec in db.items()]
        print(json.dumps(exports, indent=2))


if __name__ == "__main__":
    main()
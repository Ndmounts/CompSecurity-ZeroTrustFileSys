import json
import fnmatch
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID


def user_from_cert(): # also verifies cert
    leaf_cert_path = "certs/curent.csr"
    try:
        with open(leaf_cert_path, "rb") as f:
            leaf_cert_data = f.read()
            leaf_cert = x509.load_pem_x509_certificate(leaf_cert_data, default_backend())

        with open(root_ca_path, "rb") as f:
            root_ca_data = f.read()
            root_ca_cert = x509.load_pem_x509_certificate(root_ca_data, default_backend())

        store = Store([root_ca_cert])
        policy = PolicyBuilder().build_server_verifier(leaf_cert.subject)
        verifier = store.get_server_verifier(policy)
        
        verifier.verify(leaf_cert, [])
        return(leaf_cert_data.cn_attributes[0].value)

    except VerificationError as e:
        print(f"Certificate verification failed: {e}")
        return "-1"

    except Exception as e:
        print(f"An error occurred: {e}")
        return "-1"

import json
import fnmatch
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import padding
import traceback


def user_from_cert(): # also verifies cert
    leaf_cert_path = "certs/curent.crt"
    root_ca_path = "certs/curent_root.crt"
    try:
        with open(leaf_cert_path, "rb") as f:
            leaf_cert_data = f.read()
            leaf_cert = x509.load_pem_x509_certificate(leaf_cert_data, default_backend())

        with open(root_ca_path, "rb") as f:
            root_ca_data = f.read()
            root_ca_cert = x509.load_pem_x509_certificate(root_ca_data, default_backend())

        root_ca_cert.public_key().verify(
            leaf_cert.signature,
            leaf_cert.tbs_certificate_bytes,
            padding.PKCS1v15(),  
            leaf_cert.signature_hash_algorithm,
        )

        return(leaf_cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value)


    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return "-1"




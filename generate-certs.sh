mkdir certs

cd certs

# CA key (keep private)
openssl genrsa -out curent_root.key 2048

# Root CA certificate (self-signed)
openssl req -x509 -new -nodes -key curent_root.key -sha256 -days 3650 \
  -subj "/C=US/ST=CO/L=Denver/O=ZTFS/OU=Server/CN=server" \
  -out curent_root.crt

user_cert_gen() {
	local CN="$1"

    echo "Generating certificate for user: $CN"

    # User key
    openssl genrsa -out "${CN}.key" 2048

    # User CSR
    openssl req -new -key "${CN}.key" \
      -subj "/C=US/ST=CO/L=Denver/O=ZTFS/OU=User/CN=${CN}" \
      -out "${CN}.csr"

    # Sign user cert with root CA
    openssl x509 -req -in "${CN}.csr" -CA curent_root.crt -CAkey curent_root.key \
      -CAcreateserial -out "${CN}.crt" -days 825 -sha256
}

user_cert_gen "user1"

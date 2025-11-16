

cd certs

# CA key (keep private)
openssl genrsa -out ca.key 4096

# CA cert (self-signed)
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 \
  -subj "/C=US/ST=CO/L=Denver/O=ZTFS/OU=CA/CN=ztfs-root" \
  -out ca.crt

# server key
openssl genrsa -out server.key 2048

user_cert_gen "user1"

user_cert_gen()
	# csr
	local CN="$1"
	openssl req -new -key server.key \
	-subj "/C=US/ST=CO/L=Denver/O=ZTFS/OU=Server/CN=${CN}" \
		-out server.csr


	# sign with CA
	openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
		-out server.crt -days 825 -sha256

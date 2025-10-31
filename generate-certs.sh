mkdir -p certs
cd certs

# CA key (keep private)
openssl genrsa -out ca.key 4096

# CA cert (self-signed)
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 \
  -subj "/C=US/ST=CO/L=Denver/O=ZTFS/OU=CA/CN=ztfs-root" \
  -out ca.crt

# server key
openssl genrsa -out server.key 2048

# csr
openssl req -new -key server.key \
  -subj "/C=US/ST=CO/L=Denver/O=ZTFS/OU=Server/CN=localhost" \ 
  -out server.csr
#CN=localhost since we're only running the server locally for this

# sign with CA
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out server.crt -days 825 -sha256

# client key
openssl genrsa -out nick.key 2048

# csr
openssl req -new -key nick.key \
  -subj "/C=US/ST=CO/L=Denver/O=ZTFS/OU=Clients/CN=admin" \
  -out nick.csr

# sign
openssl x509 -req -in nick.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out nick.crt -days 825 -sha256
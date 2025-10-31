# server.py

import json
import ssl
from http.server import HTTPServer, BaseHTTPRequestHandler

from config import HOST, PORT, SERVER_CERT, SERVER_KEY, CA_CERT
from auth import user_from_cert, policy_allows
import fs

class ZTFSHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # read JSON body
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len).decode("utf-8")
        try:
            req = json.loads(body)
        except json.JSONDecodeError:
            self.send_error(400, "invalid json")
            return

        # extract peer cert from TLS layer
        # self.connection is an SSLSocket
        peercert = self.connection.getpeercert()
        try:
            user = user_from_cert(peercert)
        except Exception as e:
            self.send_error(401, f"authn failed: {e}")
            return

        op = req.get("op")
        path = req.get("path", "/")
        data = req.get("data", "")

        # authz
        if not policy_allows(user, op, path):
            self.send_error(403, f"forbidden for {user} on {op} {path}")
            return

        # dispatch ops
        try:
            if op == "LIST":
                result = fs.fs_list(path)
            elif op == "READ":
                result = fs.fs_read(path)
            elif op == "WRITE":
                fs.fs_write(path, data)
                result = "ok"
            elif op == "MKDIR":
                fs.fs_mkdir(path)
                result = "ok"
            elif op == "DELETE":
                fs.fs_delete(path)
                result = "ok"
            elif op == "STAT":
                result = fs.fs_stat(path)
            else:
                self.send_error(400, f"unknown op {op}")
                return
        except FileNotFoundError as e:
            self.send_error(404, str(e))
            return
        except Exception as e:
            self.send_error(500, f"server error: {e}")
            return

        # send JSON response
        resp = json.dumps({"user": user, "op": op, "path": path, "result": result})
        resp_bytes = resp.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(resp_bytes)))
        self.end_headers()
        self.wfile.write(resp_bytes)


def run():
    httpd = HTTPServer((HOST, PORT), ZTFSHandler)

    # wrap in TLS with client auth
    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ctx.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
    ctx.load_verify_locations(CA_CERT)
    ctx.verify_mode = ssl.CERT_REQUIRED  # ← require client cert

    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)

    print(f"Zero-Trust FS listening on https://{HOST}:{PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
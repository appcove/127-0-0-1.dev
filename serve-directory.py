#!/usr/bin/env python3

import argparse
import http.server
import ssl
import os

this_dir = os.path.dirname(os.path.abspath(__file__))


def main():
    parser = argparse.ArgumentParser()
    # add host
    parser.add_argument('--port', '-p', type=int, default=8443, help='Port to serve on')
    parser.add_argument('directory', help='Directory to serve')
    args = parser.parse_args()

    port = args.port
    document_root = os.path.abspath(args.directory)
    cert_file = os.path.join(this_dir, 'cert.pem')
    key_file = os.path.join(this_dir, 'key.pem')

    del args

    os.chdir(document_root)
    handler = http.server.SimpleHTTPRequestHandler
    httpd = http.server.HTTPServer(("127.0.0.1", port), handler)

    # Create an SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=cert_file, keyfile=key_file)

    # Wrap the server socket
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print(f"Visit https://127-0-0-1.dev:{port} to see files from {document_root}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Shutting down...")

if __name__ == '__main__':
    main()

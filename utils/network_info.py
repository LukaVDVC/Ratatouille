import platform
import subprocess

class NetworkInfo:
    @staticmethod
    def get_ipconfig():
        # Exécute ipconfig pour Windows et ip a pour Linux
        if platform.system() == "Windows":
            return subprocess.check_output("ipconfig", shell=True).decode()
        else:
            return subprocess.check_output("ip a", shell=True).decode()

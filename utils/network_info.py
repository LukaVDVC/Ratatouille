import os
import platform
import subprocess

class NetworkInfo:
    @staticmethod
    def get_ipconfig():
        if platform.system() == "Windows":
            return subprocess.check_output("ipconfig", shell=True).decode()
        else:
            return subprocess.check_output("ip a", shell=True).decode()
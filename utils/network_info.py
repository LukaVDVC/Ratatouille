import os
import platform
import subprocess

class NetworkInfo:
    @staticmethod
    def get_ipconfig():
        # Vérification du système d'exploitation pour déterminer la commande à exécuter
        if platform.system() == "Windows":
            # Exécution de la commande 'ipconfig' pour Windows
            return subprocess.check_output("ipconfig", shell=True).decode()
        else:
            # Exécution de la commande 'ip a' pour les systèmes Unix/Linux pour être sûr de son fonctionnement au lieu de ifconfig
            return subprocess.check_output("ip a", shell=True).decode()

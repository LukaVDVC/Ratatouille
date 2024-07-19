import subprocess
import platform

class Shell:
    @staticmethod
    def execute_command(command):
        try:
            # Exécution de la commande shell en fonction du système d'exploitation
            if platform.system() == "Windows":
                # Utilisation de cmd pour Windows
                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            else:
                # Utilisation de bash pour Linux et autres systèmes Unix
                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, executable='/bin/bash', universal_newlines=True)
            # Retourne le résultat de la commande
            return result
        except subprocess.CalledProcessError as e:
            # Retourne l'erreur si la commande échoue
            return str(e)

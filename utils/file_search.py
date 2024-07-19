import os
import platform

class FileSearch:
    @staticmethod
    def search(filename, search_path=None):
        # Définis le chemin de recherche par défaut en fonction du système d'exploitation
        if search_path is None:
            search_path = "C:\\" if platform.system() == "Windows" else "/"
        
        result = []
        # Parcoure les fichiers et dossiers pour trouver le fichier spécifié
        for root, dirs, files in os.walk(search_path):
            if filename in files:
                result.append(os.path.join(root, filename))
        return result

    @staticmethod
    def search_file(filename):
        # Retourne les chemins des fichiers trouvés
        return "\n".join(FileSearch.search(filename))

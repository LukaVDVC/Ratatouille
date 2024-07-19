import pyscreenshot
import io

class Screenshot:
    def get_screenshot(self):
        # Capture de l'écran
        screenshot = pyscreenshot.grab()
        # Création d'un buffer en mémoire
        buffer = io.BytesIO()
        # Sauvegarde de la capture d'écran dans le buffer au format PNG
        screenshot.save(buffer, format='PNG')
        # Repositionnement du curseur de lecture au début du buffer
        buffer.seek(0)
        # Retourne les données de la capture d'écran
        return buffer.getvalue()

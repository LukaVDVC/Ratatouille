#!/bin/bash

# Vérifie si Python3 est installé
if ! command -v python3 &> /dev/null
then
    echo "Python3 n'est pas installé. Veuillez installer Python3 et réessayer."
    exit 1
fi

# Crée un environnement virtuel nommé 'venv'
echo "Création de l'environnement virtuel 'venv'..."
python3 -m venv venv

# Vérifie si la création de l'environnement virtuel a réussi
if [ $? -ne 0 ]; then
    echo "La création de l'environnement virtuel a échoué."
    exit 1
fi

# Active l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source venv/bin/activate

# Vérifie si l'activation de l'environnement virtuel a réussi
if [ $? -ne 0 ]; then
    echo "L'activation de l'environnement virtuel a échoué."
    exit 1
fi

# Installe les dépendances à partir du fichier requirements.txt
echo "Installation des dépendances à partir de requirements.txt..."
pip install -r requirements.txt

# Vérifie si l'installation des dépendances a réussi
if [ $? -ne 0 ]; then
    echo "L'installation des dépendances a échoué."
    exit 1
fi

echo "Le setup est terminé avec succès. Vous pouvez désormais lancer le serveur !"

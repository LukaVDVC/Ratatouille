# README

## Introduction

Ce projet est une Remote Administration Tool (RAT) développée en Python, capable de fonctionner sur les systèmes Windows et Linux. Le système se compose d'un serveur et d'un client qui communiquent via une socket TCP chiffrée et sécurisée. Ce projet répond aux exigences définies dans le cahier des charges du projet final.

## Fonctionnalités

### Client
Le client dispose des fonctionnalités suivantes :
- `help` : Affiche la liste des commandes disponibles.
- `download <filepath>` : Télécharge un fichier depuis la machine victime vers le serveur.
- `upload <filepath> <destination>` : Télécharge un fichier depuis le serveur vers la machine victime.
- `shell <command>` : Ouvre un shell interactif (bash pour Linux, cmd pour Windows).
- `ipconfig` : Affiche la configuration réseau de la machine victime.
- `screenshot` : Prend une capture d'écran de la machine victime.
- `search <filename>` : Recherche un fichier sur la machine victime.
- `hashdump` : Récupère la base SAM (Windows) ou le fichier shadow (Linux).

### Serveur
Le serveur écoute les connexions entrantes des clients et offre une interface interactive pour exécuter des commandes. Il supporte également la gestion de plusieurs sessions clients simultanément.

## Prérequis

### Général
- Python 3.x
- pip (Python package installer)

### Librairies Python
Les librairies nécessaires sont listées dans le fichier `requirements.txt` et incluent :
- `pyscreenshot`
- `psutil`
- `tabulate`
- `pynput`
- `pillow`

### Setup pour Linux

1. Cloner le dépôt du projet :
    ```sh
    git clone https://github.com/LukaVDVC/Ratatouille.git
    cd Ratatouille
    ```

2. Créer et activer un environnement virtuel :
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Installer les dépendances :
    ```sh
    pip install -r requirements.txt
    ```

### Setup pour Windows

1. Cloner le dépôt du projet :
    ```cmd
    git clone https://github.com/LukaVDVC/Ratatouille.git
    cd Ratatouille
    ```

2. Créer et activer un environnement virtuel :
    ```cmd
    python -m venv venv
    venv\Scripts\activate
    ```

3. Installer les dépendances :
    ```cmd
    pip install -r requirements.txt
    ```

## Utilisation

### Démarrage du Serveur

Lancer le serveur en exécutant la commande suivante :
```sh
python server.py
```
Le serveur écoute sur le port spécifié et attend les connexions des clients. Une fois connecté, il fournit une interface interactive pour exécuter des commandes sur les machines victimes.

### Connexion du Client

Lancer le client en exécutant la commande suivante :
```sh
sudo python client.py
```
Le client se connecte au serveur spécifié et attend les commandes à exécuter.

Pour Windows il faut juste l'exécutez

## Exigences du Projet

Le projet doit répondre aux exigences suivantes :
- Fonctionner sur Windows et Linux.
- Utiliser une communication TCP chiffrée et sécurisée.
- Implémenter les fonctionnalités décrites ci-dessus.

## Vidéo de Démonstration

https://youtu.be/D7d9pAU22rw

## Auteurs

Ce projet a été développé par LukaVDVC et Matthis dans le cadre du projet final.

from flask import Blueprint, render_template
import random
import os
import itertools
from functools import lru_cache

# Initialisation du blueprint
zombie_app = Blueprint('zombie_app', __name__)

# Répertoire des parties du corps des zombies
DIRECTORIES = {
    "head": "static/images/head",
    "body": "static/images/body",
    "L_leg": "static/images/L_leg",
    "R_leg": "static/images/R_leg",
    "L_arm": "static/images/L_arm",
    "R_arm": "static/images/R_arm",
}

# Fonction utilitaire pour charger les images des répertoires avec mise en cache
@lru_cache(maxsize=None)
def load_images():
    """Charge et met en cache les fichiers disponibles dans chaque répertoire."""
    return {key: os.listdir(directory) for key, directory in DIRECTORIES.items()}

# Fonction pour récupérer une image aléatoire pour chaque partie du corps
def get_random_images():
    """Utilise les fichiers des répertoires pour sélectionner une image aléatoire par partie."""
    images = load_images()
    return {part: f"/{DIRECTORIES[part]}/{random.choice(images[part])}" for part in DIRECTORIES}

# Fonction pour générer une liste de zombies aléatoires
def generate_random_zombies(nbr_zombies):
    """Génère un certain nombre de zombies aléatoires."""
    images = load_images()
    return [
        {
            part: f"/{DIRECTORIES[part]}/{random.choice(images[part])}" if part == "body" or random.random() < 0.6 else None
            for part in DIRECTORIES
        }
        for _ in range(nbr_zombies)
    ]

# Fonction pour générer toutes les combinaisons possibles
def generate_all_combinations():
    """Utilise itertools pour générer toutes les combinaisons possibles."""
    images = load_images()
    return [
        {part: f"/{DIRECTORIES[part]}/{image}" for part, image in zip(DIRECTORIES.keys(), combination)}
        for combination in itertools.product(*images.values())
    ]

# Route pour générer des zombies aléatoires
@zombie_app.route('/zombies/<int:nbr_zombies>', defaults={'rotate': False})
@zombie_app.route('/zombie', defaults={'nbr_zombies': 1, 'rotate': False})
@zombie_app.route('/zombietourne', defaults={'nbr_zombies': 1, 'rotate': True})
def generate_zombies(nbr_zombies, rotate):
    zombies = generate_random_zombies(nbr_zombies)
    return render_template(
        'zombies.jinja',
        zombies=zombies,
        nbr_zombies=nbr_zombies,
        rotate=rotate,
    )

# Route pour générer tous les zombies possibles
@zombie_app.route('/zombiesall')
def zombiesall():
    zombies = generate_all_combinations()
    return render_template(
        'zombies.jinja',
        zombies=zombies,
        nbr_zombies=len(zombies),
        rotate=False,
    )

from flask import Blueprint, render_template
import random
import os

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

# Fonction utilitaire pour charger les images des répertoires
def load_images():
    """Charge les fichiers disponibles dans chaque répertoire."""
    return {key: os.listdir(directory) for key, directory in DIRECTORIES.items()}

# Fonction pour récupérer une image aléatoire pour chaque partie du corps
def get_random_images():
    """Sélectionne une image aléatoire pour chaque partie du zombie."""
    return {part: f"/{DIRECTORIES[part]}/{random.choice(os.listdir(DIRECTORIES[part]))}" for part in DIRECTORIES}

# Fonction pour générer une liste de zombies aléatoires
def generate_random_zombies(nbr_zombies):
    """Génère un nombre donné de zombies avec des membres aléatoires (et parfois manquants)."""
    zombies = []
    for _ in range(nbr_zombies):
        zombie = get_random_images()
        # Simuler des membres manquants
        for key in zombie.keys():
            if key != "body" and random.randint(1, 10) > 6:  # 40% de chances d'avoir un membre manquant
                zombie[key] = None
        zombies.append(zombie)
    return zombies

# Fonction utilitaire pour générer toutes les combinaisons possibles
def generate_all_combinations(parts_images):
    """Génère toutes les combinaisons possibles des parties du corps."""
    parts_keys = list(parts_images.keys())
    zombies = []

    def recursive_combinations(current_zombie, depth):
        """Génère les combinaisons récursivement."""
        if depth == len(parts_keys):
            zombies.append(current_zombie.copy())
            return
        part = parts_keys[depth]
        for image in parts_images[part]:
            current_zombie[part] = f"/{DIRECTORIES[part]}/{image}"
            recursive_combinations(current_zombie, depth + 1)

    recursive_combinations({}, 0)
    return zombies

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
    parts_images = load_images()
    zombies = generate_all_combinations(parts_images)
    return render_template(
        'zombies.jinja',
        zombies=zombies,
        nbr_zombies=len(zombies),
        rotate=False,
    )

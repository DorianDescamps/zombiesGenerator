from flask import Blueprint, render_template
import random
import os

# Initialisation du blueprint
zombie_app = Blueprint('zombie_app', __name__)

# Route vers un zombie aléatoire
@zombie_app.route('/zombie')
def zombie():

    # Récupération d'une image aléatoire pour chaque partie du corps
    random_head_file, random_body_file, random_Lleg_file, random_Rleg_file, random_Larm_file, random_Rarm_file = get_random_images()
    
    # Envoi des données au template
    return render_template('zombie.jinja', random_head_file=random_head_file, random_body_file=random_body_file, random_Lleg_file=random_Lleg_file, random_Rleg_file=random_Rleg_file, random_Larm_file=random_Larm_file, random_Rarm_file=random_Rarm_file, simple=True)

# Route vers un zombie qui tourne
@zombie_app.route('/zombietourne')
def zombietourne():
    random_head_file, random_body_file, random_Lleg_file, random_Rleg_file, random_Larm_file, random_Rarm_file = get_random_images()

    return render_template('zombie.jinja', random_head_file=random_head_file, random_body_file=random_body_file, random_Lleg_file=random_Lleg_file, random_Rleg_file=random_Rleg_file, random_Larm_file=random_Larm_file, random_Rarm_file=random_Rarm_file, simple=True, rotate=True)

# Route vers un nombre de zombies passé en argument dans l'url avec des membres manquants
@zombie_app.route('/zombies/<int:nbr_zombies>')
def zombies(nbr_zombies):
    # Création de listes pour chaque partie du corps
    random_head_files = []
    random_body_files = []
    random_Lleg_files = []
    random_Rleg_files = []
    random_Larm_files = []
    random_Rarm_files = []

    # Génération d'un nombre de zombies égal à nbr_zombies
    for _ in range(nbr_zombies):
        random_head_file, random_body_file, random_Lleg_file, random_Rleg_file, random_Larm_file, random_Rarm_file = get_random_images()

        # Sélectionner une image aléatoire pour chaque partie du corps hormis le body si le nombre aléatoire est inférieur ou égal à 6
        random_head_files.append(random_head_file if random.randint(1, 10) <= 6 else 'None'' style="visibility: hidden;"')
        random_body_files.append(random_body_file)
        random_Lleg_files.append(random_Lleg_file if random.randint(1, 10) <= 6 else 'None'' style="visibility: hidden;"')
        random_Rleg_files.append(random_Rleg_file if random.randint(1, 10) <= 6 else 'None'' style="visibility: hidden;"')
        random_Larm_files.append(random_Larm_file if random.randint(1, 10) <= 6 else 'None'' style="visibility: hidden;"')
        random_Rarm_files.append(random_Rarm_file if random.randint(1, 10) <= 6 else 'None'' style="visibility: hidden;"')

    return render_template('zombies.jinja', random_head_files=random_head_files, random_body_files=random_body_files, random_Lleg_files=random_Lleg_files, random_Rleg_files=random_Rleg_files, random_Larm_files=random_Larm_files, random_Rarm_files=random_Rarm_files, nbr_zombies=nbr_zombies, number=True)

# Route vers tous les zombies possibles (Uniquement des zombies complets, pas de membres manquants car la génération prendrait trop de temps et de ressources)
@zombie_app.route('/zombiesall')
def zombiesall():
    random_head_files = []
    random_body_files = []
    random_Lleg_files = []
    random_Rleg_files = []
    random_Larm_files = []
    random_Rarm_files = []

    # Récupération de toutes les images pour chaque partie du corps
    head_images = os.listdir("static/images/head")
    body_images = os.listdir("static/images/body")
    Lleg_images = os.listdir("static/images/L_leg")
    Rleg_images = os.listdir("static/images/R_leg")
    Larm_images = os.listdir("static/images/L_arm")
    Rarm_images = os.listdir("static/images/R_arm")

    # Génération de tous les zombies possibles
    for head_image in head_images:
        for body_image in body_images:
            for Lleg_image in Lleg_images:
                for Rleg_image in Rleg_images:
                    for Larm_image in Larm_images:
                        for Rarm_image in Rarm_images:
                            # Ajout des images dans les listes
                            random_head_files.append("/static/images/head/" + head_image)
                            random_body_files.append("/static/images/body/" + body_image)
                            random_Lleg_files.append("/static/images/L_leg/" + Lleg_image)
                            random_Rleg_files.append("/static/images/R_leg/" + Rleg_image)
                            random_Larm_files.append("/static/images/L_arm/" + Larm_image)
                            random_Rarm_files.append("/static/images/R_arm/" + Rarm_image)

    return render_template('zombies.jinja', random_head_files=random_head_files, random_body_files=random_body_files, random_Lleg_files=random_Lleg_files, random_Rleg_files=random_Rleg_files, random_Larm_files=random_Larm_files, random_Rarm_files=random_Rarm_files, nbr_zombies=len(random_head_files))

# Fonction pour récupérer une image aléatoirement dans chaque dossier
def get_random_images():
    head_images = os.listdir("static/images/head")
    body_images = os.listdir("static/images/body")
    Lleg_images = os.listdir("static/images/L_leg")
    Rleg_images = os.listdir("static/images/R_leg")
    Larm_images = os.listdir("static/images/L_arm")
    Rarm_images = os.listdir("static/images/R_arm")
    return (
        "/static/images/head/" + random.choice(head_images),
        "/static/images/body/" + random.choice(body_images),
        "/static/images/L_leg/" + random.choice(Lleg_images),
        "/static/images/R_leg/" + random.choice(Rleg_images),
        "/static/images/L_arm/" + random.choice(Larm_images),
        "/static/images/R_arm/" + random.choice(Rarm_images)
    )
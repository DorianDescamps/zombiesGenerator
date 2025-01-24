from flask import Flask, render_template
from http import HTTPStatus
import random
import os

app = Flask(__name__)

from blueprints.Zombies import zombie_app
app.register_blueprint(zombie_app)

@app.route('/')
def index():
    return render_template('socle/base.jinja')

@app.errorhandler(404)
def page_not_found(e):
    return 'Erreur !!! /!\ Page Inexistante /!\ seul /zombie , /zombietourne , /zombies/"nb" , /zombiesall existe !', HTTPStatus.NOT_FOUND
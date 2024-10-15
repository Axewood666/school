from flask import Blueprint, render_template

pages = Blueprint('pages', __name__)

@pages.route("/")
def Main():
    return render_template('index.html', context="/")
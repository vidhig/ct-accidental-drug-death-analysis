from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template
#from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask import Markup
from dataprocessing import *
from maprenderer import *
from analysis import *


app = Flask(__name__)



@app.route('/')
def index():
    #define all variables to pass to the page here
    card_1_title = "CT Drug Deaths"
    card_2_title = ""
    card_3_title = ""
    card_4_title = ""
    return render_template('index.html', card_1_title = card_1_title, 
        card_2_title=card_2_title,card_3_title=card_3_title,card_4_title = card_4_title )


@app.route("/map")
def map():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
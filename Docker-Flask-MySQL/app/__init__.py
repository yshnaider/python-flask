from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, render_template, request
from flask_login import LoginManager
import string
import random

from werkzeug.utils import redirect

from config import app_config

base_url = 'http://127.0.0.1:8000/'

db = SQLAlchemy()
login_manager = LoginManager()

#app.config.from_object(app_config[config_name])
app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@db_1/insta_db"
app.config.from_pyfile('config.py')
db.init_app(app)

from app.models import Table

#generates random 6 string
def id_generator(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#returns database row with the required tinyURL, url or
#creating this row in db and then returns
def create_get_tinyURL(url):
    if Table.query.filter_by(url='url').first() != None:
        ret = Table.query.filter_by(url='url').first()
        return ret
    else:
        tinyURL = base_url + str(id_generator())
        db.session.add(Table(tinyURL, url))
        db.session.commit()
        ret = Table.query.filter_by(url='url').first()
        return ret

#returns the appropriate row from db containing url for
#the tinyURL required
def get_url(tinyPart):
    tinyURL = base_url + str(tinyPart)
    ret = Table.query.filter_by(tinyURL='tinyURL').first()
    return ret


def create_app(config_name):

    @app.route("/", methods=["GET", "POST"])
    def home():

        if request.method == "POST":
            userDetails = request.form
            url = userDetails["url"]
            ret = create_get_tinyURL(url)

            return render_template('home.html', post=ret.tinyURL, pist=ret.url)
        return render_template("home.html")

    @app.route("/<tinyPart>")
    def redir(tinyPart):
        ret = get_url(tinyPart)
        return redirect(str(ret.url))

    login_manager.init_app(app)
    login_manager.login_message = 'You must be logged in to access this page'
    login_manager.login_view = 'auth.login'

    migrate = Migrate(app, db)

    from app import models

    return app

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from sqlalchemy.ext.declarative import declarative_base


class Table(db.Model):
    """
    Create an URL table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True)
    tinyURL = db.Column(db.String(100), unique=True, nullable=False)
    url = db.Column(db.String(200), unique=True, nullable=False)

    def __init__(self, tinyURL, url):
        self.tinyURL = tinyURL
        self.url = url

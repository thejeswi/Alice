from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from . import app
from urllib import quote

db = SQLAlchemy(app)

class Page(db.Model):
    __tablename__ = 'pages'
    id = db.Column('page_id', db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=True)
    text = db.Column(db.String)
    path = db.Column(db.String)
    style = db.Column(db.String)
    color = db.Column(db.String(8))

class Config(db.Model):
    __tablename__ = 'config'
    id = db.Column('config_id', db.Integer, primary_key=True)
    config = db.Column(db.String(60), unique=True)
    value = db.Column(db.String)
    def __init__(self,config,value):
        self.config = config
        self.value = value

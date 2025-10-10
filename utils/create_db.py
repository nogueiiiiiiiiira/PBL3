from flask import Flask
from modelos.db import db

def create_db(app: Flask):
    with app.app_context():
        db.drop_all()
        db.create_all()
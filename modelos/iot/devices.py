from modelos.db import db

class Dispositivo(db.Model):
    __tablename__ = 'dispositivos'
    id = db.Column('id', db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=False)
    sensores = db.relationship('Sensor', backref='dispositivo', lazy=True)
    atuadores = db.relationship('Atuador', backref='dispositivo', lazy=True)
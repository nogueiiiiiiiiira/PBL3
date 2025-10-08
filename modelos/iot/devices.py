"""
Módulo que define o modelo Dispositivo base para o sistema IoT.
Este modelo representa dispositivos genéricos que podem ser sensores ou atuadores.
"""
from modelos.db import db

class Dispositivo(db.Model):
    """
    Modelo base que representa um dispositivo no sistema IoT.
    Todos os dispositivos (sensores e atuadores) herdam desta classe base.
    """
    __tablename__ = 'dispositivos'
    id = db.Column('id', db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=False)

    # Relacionamentos com sensores e atuadores
    sensores = db.relationship('Sensor', backref='dispositivo', lazy=True)
    atuadores = db.relationship('Atuador', backref='dispositivo', lazy=True)

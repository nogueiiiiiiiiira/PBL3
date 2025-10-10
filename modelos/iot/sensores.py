from modelos.db import db
from modelos.iot.devices import Dispositivo

class Sensor(db.Model):
    __tablename__ = 'sensores'
    id = db.Column('id', db.Integer, primary_key=True)
    dispositivos_id = db.Column(db.Integer, db.ForeignKey(Dispositivo.id))
    unidade = db.Column(db.String(50))
    topico = db.Column(db.String(50))

    @classmethod
    def salvar_sensor(cls, nome, marca, modelo, topico, unidade, ativo):
        dispositivo = Dispositivo(nome=nome, marca=marca, modelo=modelo, ativo=ativo)
        db.session.add(dispositivo)
        db.session.commit()
        sensor = cls(dispositivos_id=dispositivo.id, topico=topico, unidade=unidade)
        db.session.add(sensor)
        db.session.commit()
        return sensor

    @staticmethod
    def obter_sensores():
        return Sensor.query.order_by(Sensor.id).all()

    @staticmethod
    def obter_sensor_por_id(id_sensor):
        return Sensor.query.get(id_sensor)

    @classmethod
    def atualizar_sensor(cls, id_sensor, nome=None, marca=None, modelo=None, topico=None, unidade=None, ativo=None):
        sensor = cls.query.get(id_sensor)
        if sensor:
            dispositivo = Dispositivo.query.get(sensor.dispositivos_id)
            if dispositivo:
                if nome is not None:
                    dispositivo.nome = nome
                if marca is not None:
                    dispositivo.marca = marca
                if modelo is not None:
                    dispositivo.modelo = modelo
                if ativo is not None:
                    dispositivo.ativo = ativo
            if topico is not None:
                sensor.topico = topico
            if unidade is not None:
                sensor.unidade = unidade
            db.session.commit()
        return sensor

    @staticmethod
    def deletar_sensor(id_sensor):
        sensor = Sensor.query.get(id_sensor)
        if sensor:
            dispositivo = Dispositivo.query.get(sensor.dispositivos_id)
            db.session.delete(sensor)
            if dispositivo:
                db.session.delete(dispositivo)
            db.session.commit()
            return True
        return False
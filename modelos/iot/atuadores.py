from modelos.db import db
from modelos.iot.devices import Dispositivo

class Atuador(db.Model):
    __tablename__ = 'atuadores'
    id = db.Column('id', db.Integer, primary_key=True)
    dispositivos_id = db.Column(db.Integer, db.ForeignKey(Dispositivo.id))
    unidade = db.Column(db.String(50))
    topico = db.Column(db.String(50))

    @classmethod
    def salvar_atuador(cls, nome, marca, modelo, topico, unidade, ativo):
        dispositivo = Dispositivo(nome=nome, marca=marca, modelo=modelo, ativo=ativo)
        db.session.add(dispositivo)
        db.session.commit()
        atuador = cls(dispositivos_id=dispositivo.id, topico=topico, unidade=unidade)
        db.session.add(atuador)
        db.session.commit()
        return atuador

    @staticmethod
    def obter_atuadores():
        return Atuador.query.order_by(Atuador.id).all()

    @staticmethod
    def obter_atuador_por_id(id_atuador):
        return Atuador.query.get(id_atuador)

    @classmethod
    def atualizar_atuador(cls, id_atuador, nome=None, marca=None, modelo=None, topico=None, unidade=None, ativo=None):
        atuador = cls.query.get(id_atuador)
        if atuador:
            dispositivo = Dispositivo.query.get(atuador.dispositivos_id)
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
                atuador.topico = topico
            if unidade is not None:
                atuador.unidade = unidade
            db.session.commit()
        return atuador

    @staticmethod
    def deletar_atuador(id_atuador):
        atuador = Atuador.query.get(id_atuador)
        if atuador:
            dispositivo = Dispositivo.query.get(atuador.dispositivos_id)
            db.session.delete(atuador)
            if dispositivo:
                db.session.delete(dispositivo)
            db.session.commit()
            return True
        return False
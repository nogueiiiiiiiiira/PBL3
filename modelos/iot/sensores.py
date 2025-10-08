"""
Módulo que define o modelo Sensor para o sistema IoT.
Um sensor é um dispositivo que coleta dados do ambiente.
"""
from modelos.db import db
from modelos.iot.devices import Dispositivo

class Sensor(db.Model):
    """
    Modelo que representa um sensor no sistema IoT.
    Cada sensor está associado a um dispositivo e possui tópico MQTT e unidade de medida.
    """
    __tablename__ = 'sensores'
    id = db.Column('id', db.Integer, primary_key=True)
    dispositivos_id = db.Column(db.Integer, db.ForeignKey(Dispositivo.id))
    unidade = db.Column(db.String(50))
    topico = db.Column(db.String(50))

    @classmethod
    def salvar_sensor(cls, nome, marca, modelo, topico, unidade, ativo):
        """
        Salva um novo sensor no banco de dados.
        Cria tanto o dispositivo quanto o sensor associado.

        Args:
            nome (str): Nome do dispositivo sensor
            marca (str): Marca do dispositivo
            modelo (str): Modelo do dispositivo
            topico (str): Tópico MQTT para comunicação
            unidade (str): Unidade de medida do sensor
            ativo (bool): Status do dispositivo

        Returns:
            Sensor: Instância do sensor criado
        """
        dispositivo = Dispositivo(nome=nome, marca=marca, modelo=modelo, ativo=ativo)
        db.session.add(dispositivo)
        db.session.commit()
        sensor = cls(dispositivos_id=dispositivo.id, topico=topico, unidade=unidade)
        db.session.add(sensor)
        db.session.commit()
        return sensor

    @staticmethod
    def obter_sensores():
        """
        Obtém todos os sensores cadastrados com informações do dispositivo.

        Returns:
            list: Lista de sensores com dados dos dispositivos associados
        """
        sensores = Sensor.query.join(Dispositivo, Dispositivo.id == Sensor.dispositivos_id)\
        .add_columns(Dispositivo.id, Dispositivo.nome,
        Dispositivo.marca, Dispositivo.modelo,
        Dispositivo.ativo, Sensor.topico,
        Sensor.unidade).all()

        return sensores

    @staticmethod
    def obter_sensor_por_id(id_sensor):
        """
        Obtém um sensor específico pelo ID.

        Args:
            id_sensor (int): ID do sensor

        Returns:
            Sensor or None: Sensor encontrado ou None se não existir
        """
        return Sensor.query.get(id_sensor)

    @classmethod
    def atualizar_sensor(cls, id_sensor, nome=None, marca=None, modelo=None, topico=None, unidade=None, ativo=None):
        """
        Atualiza os dados de um sensor existente.

        Args:
            id_sensor (int): ID do sensor a ser atualizado
            nome (str, optional): Novo nome do dispositivo
            marca (str, optional): Nova marca
            modelo (str, optional): Novo modelo
            topico (str, optional): Novo tópico MQTT
            unidade (str, optional): Nova unidade de medida
            ativo (bool, optional): Novo status

        Returns:
            Sensor or None: Sensor atualizado ou None se não encontrado
        """
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
        """
        Remove um sensor do banco de dados.
        Também remove o dispositivo associado.

        Args:
            id_sensor (int): ID do sensor a ser deletado

        Returns:
            bool: True se deletado com sucesso, False se não encontrado
        """
        sensor = Sensor.query.get(id_sensor)
        if sensor:
            dispositivo = Dispositivo.query.get(sensor.dispositivos_id)
            db.session.delete(sensor)
            if dispositivo:
                db.session.delete(dispositivo)
            db.session.commit()
            return True
        return False




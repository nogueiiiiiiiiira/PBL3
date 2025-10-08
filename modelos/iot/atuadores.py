"""
Módulo que define o modelo Atuador para o sistema IoT.
Um atuador é um dispositivo que executa ações no ambiente.
"""
from modelos.db import db
from modelos.iot.devices import Dispositivo

class Atuador(db.Model):
    """
    Modelo que representa um atuador no sistema IoT.
    Cada atuador está associado a um dispositivo e possui tópico MQTT e unidade de controle.
    """
    __tablename__ = 'atuadores'
    id = db.Column('id', db.Integer, primary_key=True)
    dispositivos_id = db.Column(db.Integer, db.ForeignKey(Dispositivo.id))
    unidade = db.Column(db.String(50))
    topico = db.Column(db.String(50))

    @classmethod
    def salvar_atuador(cls, nome, marca, modelo, topico, unidade, ativo):
        """
        Salva um novo atuador no banco de dados.
        Cria tanto o dispositivo quanto o atuador associado.

        Args:
            nome (str): Nome do dispositivo atuador
            marca (str): Marca do dispositivo
            modelo (str): Modelo do dispositivo
            topico (str): Tópico MQTT para comunicação
            unidade (str): Unidade de controle do atuador
            ativo (bool): Status do dispositivo

        Returns:
            Atuador: Instância do atuador criado
        """
        dispositivo = Dispositivo(nome=nome, marca=marca, modelo=modelo, ativo=ativo)
        db.session.add(dispositivo)
        db.session.commit()
        atuador = cls(dispositivos_id=dispositivo.id, topico=topico, unidade=unidade)
        db.session.add(atuador)
        db.session.commit()
        return atuador

    @staticmethod
    def obter_atuadores():
        """
        Obtém todos os atuadores cadastrados com informações do dispositivo.

        Returns:
            list: Lista de atuadores com dados dos dispositivos associados
        """
        atuadores = Atuador.query.join(Dispositivo, Dispositivo.id == Atuador.dispositivos_id)\
        .add_columns(Dispositivo.id, Dispositivo.nome,
        Dispositivo.marca, Dispositivo.modelo,
        Dispositivo.ativo, Atuador.topico,
        Atuador.unidade).all()

        return atuadores

    @staticmethod
    def obter_atuador_por_id(id_atuador):
        """
        Obtém um atuador específico pelo ID.

        Args:
            id_atuador (int): ID do atuador

        Returns:
            Atuador or None: Atuador encontrado ou None se não existir
        """
        return Atuador.query.get(id_atuador)

    @classmethod
    def atualizar_atuador(cls, id_atuador, nome=None, marca=None, modelo=None, topico=None, unidade=None, ativo=None):
        """
        Atualiza os dados de um atuador existente.

        Args:
            id_atuador (int): ID do atuador a ser atualizado
            nome (str, optional): Novo nome do dispositivo
            marca (str, optional): Nova marca
            modelo (str, optional): Novo modelo
            topico (str, optional): Novo tópico MQTT
            unidade (str, optional): Nova unidade de controle
            ativo (bool, optional): Novo status

        Returns:
            Atuador or None: Atuador atualizado ou None se não encontrado
        """
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
        """
        Remove um atuador do banco de dados.
        Também remove o dispositivo associado.

        Args:
            id_atuador (int): ID do atuador a ser deletado

        Returns:
            bool: True se deletado com sucesso, False se não encontrado
        """
        atuador = Atuador.query.get(id_atuador)
        if atuador:
            dispositivo = Dispositivo.query.get(atuador.dispositivos_id)
            db.session.delete(atuador)
            if dispositivo:
                db.session.delete(dispositivo)
            db.session.commit()
            return True
        return False

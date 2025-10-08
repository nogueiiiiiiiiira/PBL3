from modelos.db import db

class Usuario(db.Model):
    """
    Modelo que representa um usuário no sistema IoT.
    Armazena informações básicas do usuário para autenticação e gerenciamento.
    """
    __tablename__ = 'usuarios'
    id = db.Column('id', db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    @classmethod
    def salvar_usuario(cls, nome, email, senha, ativo=True):
        """
        Salva um novo usuário no banco de dados.

        Args:
            nome (str): Nome completo do usuário
            email (str): Email único do usuário
            senha (str): Senha do usuário (deve ser hashada)
            ativo (bool): Status do usuário (padrão: True)

        Returns:
            Usuario: Instância do usuário criado
        """
        usuario = cls(nome=nome, email=email, senha=senha, ativo=ativo)
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def obter_usuarios():
        """
        Obtém todos os usuários cadastrados.

        Returns:
            list: Lista de todos os usuários
        """
        return Usuario.query.all()

    @staticmethod
    def obter_usuario_por_id(id_usuario):
        """
        Obtém um usuário específico pelo ID.

        Args:
            id_usuario (int): ID do usuário

        Returns:
            Usuario or None: Usuário encontrado ou None se não existir
        """
        return Usuario.query.get(id_usuario)

    @staticmethod
    def obter_usuario_por_email(email):
        """
        Obtém um usuário específico pelo email.

        Args:
            email (str): Email do usuário

        Returns:
            Usuario or None: Usuário encontrado ou None se não existir
        """
        return Usuario.query.filter_by(email=email).first()

    @classmethod
    def atualizar_usuario(cls, id_usuario, nome=None, email=None, senha=None, ativo=None):
        """
        Atualiza os dados de um usuário existente.

        Args:
            id_usuario (int): ID do usuário a ser atualizado
            nome (str, optional): Novo nome
            email (str, optional): Novo email
            senha (str, optional): Nova senha
            ativo (bool, optional): Novo status

        Returns:
            Usuario or None: Usuário atualizado ou None se não encontrado
        """
        usuario = cls.query.get(id_usuario)
        if usuario:
            if nome is not None:
                usuario.nome = nome
            if email is not None:
                usuario.email = email
            if senha is not None:
                usuario.senha = senha
            if ativo is not None:
                usuario.ativo = ativo
            db.session.commit()
        return usuario

    @staticmethod
    def deletar_usuario(id_usuario):
        """
        Remove um usuário do banco de dados.

        Args:
            id_usuario (int): ID do usuário a ser deletado

        Returns:
            bool: True se deletado com sucesso, False se não encontrado
        """
        usuario = Usuario.query.get(id_usuario)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return True
        return False

from modelos.db import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column('id', db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    @classmethod
    def salvar_usuario(cls, nome, email, senha, ativo=True):
        usuario = cls(nome=nome, email=email, senha=senha, ativo=ativo)
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def obter_usuarios():
        return Usuario.query.all()

    @staticmethod
    def obter_usuario_por_id(id_usuario):
        return Usuario.query.get(id_usuario)

    @staticmethod
    def obter_usuario_por_email(email):
        return Usuario.query.filter_by(email=email).first()

    @classmethod
    def atualizar_usuario(cls, id_usuario, nome=None, email=None, senha=None, ativo=None):
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
        usuario = Usuario.query.get(id_usuario)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return True
        return False
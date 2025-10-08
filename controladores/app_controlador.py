#app_controlador.py
from flask import Flask, render_template, request, redirect, flash, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from modelos.db import db, instance
from controladores.sensores_controlador import sensor_
from controladores.atuadores_controlador import atuador_
from modelos.iot.devices import Dispositivo
from modelos.iot.sensores import Sensor
from modelos.iot.atuadores import Atuador
from modelos.user.user import Usuario

def create_app():
    app = Flask(__name__,
                template_folder="./views/",
                static_folder="./static/",
                root_path="./")
    
    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    db.init_app(app)
        
    app.register_blueprint(sensor_, url_prefix='/')
    app.register_blueprint(atuador_, url_prefix='/')
    
    @app.route('/')
    def indice():
        """
        Página inicial da aplicação IoT.
        Redireciona para a página principal do sistema.
        """
        return render_template("home.html")

    @app.route('/home')
    def inicio():
        """
        Página principal do sistema IoT.
        Exibe o dashboard principal com navegação para outras funcionalidades.
        """
        return render_template("home.html")

    @app.route('/cadastrar_usuario')
    def cadastrar_usuario():
        """
        Página para cadastro de novos usuários no sistema.
        """
        return render_template("registrar_usuario.html")

    @app.route('/cadastrar_sensor')
    def cadastrar_sensor():
        """
        Página para cadastro de novos sensores IoT.
        """
        return render_template("registrar_sensor.html")

    @app.route('/cadastrar_atuador')
    def cadastrar_atuador():
        """
        Página para cadastro de novos atuadores IoT.
        """
        return render_template("registrar_atuador.html")

    @app.route('/listar_usuarios')
    def listar_usuarios():
        """
        Página que lista todos os usuários cadastrados no sistema.
        """
        usuarios = Usuario.obter_usuarios()
        return render_template("users.html", usuarios=usuarios)

    @app.route('/sensores')
    def sensores():
        """
        Página que exibe todos os sensores cadastrados no sistema IoT.
        """
        return render_template("sensores.html")

    @app.route('/atuadores')
    def atuadores():
        """
        Página que exibe todos os atuadores cadastrados no sistema IoT.
        """
        return render_template("atuadores.html")

    @app.route('/tempo_real')
    def tempo_real():
        """
        Página que exibe dados em tempo real dos sensores.
        Mostra valores atuais de temperatura e umidade.
        """
        valores = {'temperatura': 25, 'umidade': 60}
        return render_template("tr.html", values=valores)

    @app.route('/publicar')
    def publicar():
        """
        Página para publicar comandos aos atuadores do sistema IoT.
        """
        return render_template("publish.html")

    @app.route('/historico_sensores')
    def historico_sensores():
        """
        Página que exibe o histórico de dados dos sensores.
        Permite consultar dados históricos de sensores específicos.
        """
        sensores = [{'id': 1}, {'id': 2}, {'id': 3}]
        return render_template("historico_sensores.html", sensores=sensores)

    @app.route('/historico_atuadores')
    def historico_atuadores():
        """
        Página que exibe o histórico de comandos enviados aos atuadores.
        Permite consultar ações históricas dos atuadores.
        """
        atuadores = [{'id': 1}, {'id': 2}, {'id': 3}]
        return render_template("historico_atuadores.html", atuadores=atuadores)

    @app.route('/obter_dados', methods=['POST'])
    def obter_dados():
        """
        Processa requisição POST para obter histórico de dados de um sensor.
        Recebe ID do sensor e período (início/fim) para filtrar dados.
        """
        id_sensor = request.form['id']
        inicio = request.form['start']
        fim = request.form['end']
        sensores = [{'id': 1}, {'id': 2}, {'id': 3}]
        dado = [
            {'sensores_id': id_sensor, 'value': 25.5, 'read_datetime': '2023-01-01 12:00:00'},
            {'sensores_id': id_sensor, 'value': 26.0, 'read_datetime': '2023-01-01 13:00:00'},
        ]
        return render_template("historico_atuadores.html", sensores=sensores, read=dado)

    @app.route('/obter_comando', methods=['POST'])
    def obter_comando():
        """
        Processa requisição POST para obter histórico de comandos de um atuador.
        Recebe ID do atuador e período (início/fim) para filtrar dados.
        """
        id_atuador = request.form['id']
        inicio = request.form['start']
        fim = request.form['end']
        atuadores = [{'id': 1}, {'id': 2}, {'id': 3}]
        escrita = [
            {'atuadores_id': id_atuador, 'value': 1, 'write_datetime': '2023-01-01 12:00:00'},
            {'atuadores_id': id_atuador, 'value': 0, 'write_datetime': '2023-01-01 13:00:00'},
        ]
        return render_template("historico_atuadores.html", atuadores=atuadores, write=escrita)

    # Rota antiga removida - substituída pela nova implementação abaixo

    # Rota antiga removida - substituída pela nova implementação abaixo

    @app.route('/login')
    def login():
        """
        Página de autenticação do usuário no sistema IoT.
        """
        return render_template("login.html")

    @app.route('/tabelas')
    def tabelas():
        """
        Página que exibe todas as tabelas do sistema em uma visão consolidada.
        Mostra dispositivos, sensores e atuadores cadastrados.
        """
        dispositivos = Dispositivo.query.all()
        sensores = Sensor.obter_sensores()
        atuadores = Atuador.obter_atuadores()
        return render_template("tables.html", devices=dispositivos, sensores=sensores, atuadores=atuadores)

    # ===== ROTAS CRUD PARA USUÁRIOS =====

    @app.route('/adicionar_usuario', methods=['POST'])
    def adicionar_usuario():
        """
        Processa o cadastro de um novo usuário no sistema.
        """
        try:
            nome = request.form['nome']
            email = request.form['email']
            senha = request.form['senha']
            ativo = True if request.form.get('ativo') == 'on' else False

            # Verificar se email já existe
            usuario_existente = Usuario.obter_usuario_por_email(email)
            if usuario_existente:
                flash('Email já cadastrado no sistema', 'error')
                return redirect(url_for('cadastrar_usuario'))

            # Hash da senha
            senha_hash = generate_password_hash(senha)

            # Salvar usuário
            usuario = Usuario.salvar_usuario(nome, email, senha_hash, ativo)
            flash('Usuário cadastrado com sucesso!', 'success')
            return redirect(url_for('listar_usuarios'))

        except Exception as e:
            flash(f'Erro ao cadastrar usuário: {str(e)}', 'error')
            return redirect(url_for('cadastrar_usuario'))

    @app.route('/atualizar_usuario/<int:id_usuario>', methods=['POST'])
    def atualizar_usuario(id_usuario):
        """
        Processa a atualização de dados de um usuário existente.
        """
        try:
            nome = request.form.get('nome')
            email = request.form.get('email')
            senha = request.form.get('senha')
            ativo = True if request.form.get('ativo') == 'on' else False

            # Preparar dados para atualização
            dados_atualizacao = {}
            if nome:
                dados_atualizacao['nome'] = nome
            if email:
                dados_atualizacao['email'] = email
            if senha:
                dados_atualizacao['senha'] = generate_password_hash(senha)
            dados_atualizacao['ativo'] = ativo

            usuario = Usuario.atualizar_usuario(id_usuario, **dados_atualizacao)
            if usuario:
                flash('Usuário atualizado com sucesso!', 'success')
            else:
                flash('Usuário não encontrado', 'error')
            return redirect(url_for('listar_usuarios'))

        except Exception as e:
            flash(f'Erro ao atualizar usuário: {str(e)}', 'error')
            return redirect(url_for('listar_usuarios'))

    @app.route('/deletar_usuario/<int:id_usuario>')
    def deletar_usuario(id_usuario):
        """
        Remove um usuário do sistema.
        """
        try:
            if Usuario.deletar_usuario(id_usuario):
                flash('Usuário removido com sucesso!', 'success')
            else:
                flash('Usuário não encontrado', 'error')
            return redirect(url_for('listar_usuarios'))

        except Exception as e:
            flash(f'Erro ao remover usuário: {str(e)}', 'error')
            return redirect(url_for('listar_usuarios'))

    # ===== AUTENTICAÇÃO =====

    @app.route('/validar_usuario', methods=['POST'])
    def validar_usuario():
        """
        Processa login do usuário no sistema.
        Valida credenciais usando o modelo de usuário.
        """
        email = request.form['email']
        senha = request.form['password']

        usuario = Usuario.obter_usuario_por_email(email)
        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            session['usuario_email'] = usuario.email
            flash(f'Bem-vindo, {usuario.nome}!', 'success')
            return redirect(url_for('inicio'))
        else:
            flash('Credenciais inválidas. Verifique seu email e senha.', 'error')
            return redirect(url_for('login'))

    @app.route('/desconectar')
    def desconectar():
        """
        Realiza logout do usuário do sistema.
        """
        session.clear()
        flash('Você foi desconectado com sucesso.', 'info')
        return redirect(url_for('login'))

    return app


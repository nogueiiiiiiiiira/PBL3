from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from modelos.db import db, instance
from controladores.sensores_controlador import sensor_
from controladores.atuadores_controlador import atuador_
from controladores.usuarios_controlador import usuarios_bp
from controladores.auth_controlador import auth_bp
from modelos.iot.devices import Dispositivo
from modelos.iot.sensores import Sensor
from modelos.iot.atuadores import Atuador
from modelos.user.user import Usuario

def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def create_app():
    app = Flask(__name__, template_folder='./views/', static_folder='./static/', root_path='./')
    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    db.init_app(app)
    app.register_blueprint(sensor_, url_prefix='/')
    app.register_blueprint(atuador_, url_prefix='/')
    app.register_blueprint(usuarios_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/')

    @app.route('/')
    def indice():
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        return render_template('home.html')

    @app.route('/home')
    def inicio():
        return render_template('home.html')

    @app.route('/cadastrar_usuario')
    @login_required
    def cadastrar_usuario():
        return render_template('registrar_usuario.html')

    @app.route('/cadastrar_sensor')
    @login_required
    def cadastrar_sensor():
        return render_template('registrar_sensor.html')

    @app.route('/cadastrar_atuador')
    @login_required
    def cadastrar_atuador():
        return render_template('registrar_atuador.html')

    @app.route('/listar_usuarios')
    @login_required
    def listar_usuarios():
        usuarios = Usuario.obter_usuarios()
        return render_template('users.html', usuarios=usuarios)

    @app.route('/sensores')
    @login_required
    def sensores():
        return render_template('sensores.html')

    @app.route('/atuadores')
    @login_required
    def atuadores():
        return render_template('atuadores.html')

    @app.route('/tempo_real')
    def tempo_real():
        valores = {'temperatura': 25, 'umidade': 60}
        return render_template('tr.html', values=valores)

    @app.route('/publicar')
    @login_required
    def publicar():
        return render_template('publicar.html')

    @app.route('/publicar_mensagem', methods=['POST'])
    @login_required
    def publicar_mensagem():
        data = request.get_json()
        message = data.get('message')
        topic = data.get('topic')
        return {'status': 'Mensagem publicada com sucesso', 'message': message, 'topic': topic}

    @app.route('/historico_sensores')
    @login_required
    def historico_sensores():
        read = []
        return render_template('historico_sensores.html', read=read)

    @app.route('/historico_atuadores')
    @login_required
    def historico_atuadores():
        write = []
        return render_template('historico_atuadores.html', write=write)

    @app.route('/obter_dados', methods=['POST'])
    def obter_dados():
        id_sensor = request.form['id']
        inicio = request.form['start']
        fim = request.form['end']
        sensores = [{'id': 1}, {'id': 2}, {'id': 3}]
        dado = [{'sensores_id': id_sensor, 'value': 25.5, 'read_datetime': '2023-01-01 12:00:00'}, {'sensores_id': id_sensor, 'value': 26.0, 'read_datetime': '2023-01-01 13:00:00'}]
        return render_template('historico_atuadores.html', sensores=sensores, read=dado)

    @app.route('/obter_comando', methods=['POST'])
    def obter_comando():
        id_atuador = request.form['id']
        inicio = request.form['start']
        fim = request.form['end']
        atuadores = [{'id': 1}, {'id': 2}, {'id': 3}]
        escrita = [{'atuadores_id': id_atuador, 'value': 1, 'write_datetime': '2023-01-01 12:00:00'}, {'atuadores_id': id_atuador, 'value': 0, 'write_datetime': '2023-01-01 13:00:00'}]
        return render_template('historico_atuadores.html', atuadores=atuadores, write=escrita)

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/tabelas')
    def tabelas():
        dispositivos = Dispositivo.query.all()
        sensores = Sensor.obter_sensores()
        atuadores = Atuador.obter_atuadores()
        return render_template('tables.html', devices=dispositivos, sensores=sensores, atuadores=atuadores)



    @app.route('/validar_usuario', methods=['POST'])
    def validar_usuario():
        email = request.form['email']
        senha = request.form['password']
        hardcoded_email = 'admin@gmail.com'
        hardcoded_senha = '1234'
        if email == hardcoded_email and senha == hardcoded_senha:
            session['usuario_id'] = 0
            session['usuario_nome'] = 'Admin'
            session['usuario_email'] = hardcoded_email
            return jsonify({'success': True, 'redirect': url_for('inicio')})
        usuario = Usuario.obter_usuario_por_email(email)
        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            session['usuario_email'] = usuario.email
            return jsonify({'success': True, 'redirect': url_for('inicio')})
        else:
            return jsonify({'success': False, 'message': 'Credenciais inválidas. Verifique seu email e senha.'})

    @app.route('/desconectar')
    def desconectar():
        session.clear()
        return jsonify({'message': 'Você foi desconectado com sucesso.', 'redirect': url_for('auth.login')})
    return app
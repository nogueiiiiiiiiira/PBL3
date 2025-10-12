from flask import Blueprint, render_template, request, redirect, session, url_for, jsonify
from werkzeug.security import check_password_hash
from modelos.user.user import Usuario
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return render_template('login.html')

@auth_bp.route('/validar_usuario', methods=['POST'])
def validar_usuario():
    email = request.form.get('email')
    senha = request.form.get('password')
    hardcoded_email = 'admin@gmail.com'
    hardcoded_senha = '1234'
    if email == hardcoded_email and senha == hardcoded_senha:
        session['usuario_id'] = 0
        session['usuario_nome'] = 'Admin'
        session['usuario_email'] = hardcoded_email
        return jsonify({'success': True, 'message': 'Login realizado com sucesso!', 'redirect': url_for('inicio')})
    usuario = Usuario.obter_usuario_por_email(email)
    if usuario and check_password_hash(usuario.senha, senha):
        session['usuario_id'] = usuario.id
        session['usuario_nome'] = usuario.nome
        session['usuario_email'] = usuario.email
        return jsonify({'success': True, 'message': 'Login realizado com sucesso!', 'redirect': url_for('inicio')})
    else:
        return jsonify({'success': False, 'message': 'Credenciais inválidas. Verifique seu email e senha.'})

@auth_bp.route('/desconectar')
def desconectar():
    session.clear()
    return jsonify({'message': 'Você foi desconectado com sucesso.', 'redirect': url_for('auth.login')})

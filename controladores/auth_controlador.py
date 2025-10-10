from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from werkzeug.security import check_password_hash
from modelos.user.user import Usuario
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return render_template('login.html')

@auth_bp.route('/validar_usuario', methods=['POST'])
def validar_usuario():
    email = request.form['email']
    senha = request.form['password']
    hardcoded_email = 'admin@gmail.com'
    hardcoded_senha = '1234'
    if email == hardcoded_email and senha == hardcoded_senha:
        session['usuario_id'] = 0
        session['usuario_nome'] = 'Admin'
        session['usuario_email'] = hardcoded_email
        return redirect(url_for('inicio'))
    usuario = Usuario.obter_usuario_por_email(email)
    if usuario and check_password_hash(usuario.senha, senha):
        session['usuario_id'] = usuario.id
        session['usuario_nome'] = usuario.nome
        session['usuario_email'] = usuario.email
        return redirect(url_for('inicio'))
    else:
        flash('Credenciais inválidas. Verifique seu email e senha.', 'error')
        return redirect(url_for('auth.login'))

@auth_bp.route('/desconectar')
def desconectar():
    session.clear()
    flash('Você foi desconectado com sucesso.', 'info')
    return redirect(url_for('auth.login'))
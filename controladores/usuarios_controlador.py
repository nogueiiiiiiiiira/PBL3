from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from werkzeug.security import generate_password_hash
from functools import wraps
from modelos.user.user import Usuario
usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/cadastrar_usuario')
def cadastrar_usuario():
    return render_template('registrar_usuario.html')

@usuarios_bp.route('/listar_usuarios')
def listar_usuarios():
    usuarios = Usuario.obter_usuarios()
    return render_template('users.html', usuarios=usuarios)

@usuarios_bp.route('/atualizar_usuario/<int:id_usuario>')
def atualizar_usuario(id_usuario):
    usuario = Usuario.obter_usuario_por_id(id_usuario)
    roles = [{'name': 'admin'}, {'name': 'user'}]
    return render_template('atualizar_usuario.html', user=usuario, roles=roles)

@usuarios_bp.route('/deletar_usuario_form')
def deletar_usuario_form():
    devices = Usuario.obter_usuarios_dict()
    return render_template('remover_usuario.html', devices=devices)

@usuarios_bp.route('/adicionar_usuario', methods=['POST'])
def adicionar_usuario():
    try:
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        ativo = True if request.form.get('ativo') == 'on' else False
        usuario_existente = Usuario.obter_usuario_por_email(email)
        if usuario_existente:
            flash('Email já cadastrado no sistema', 'error')
            return redirect(url_for('usuarios.cadastrar_usuario'))
        senha_hash = generate_password_hash(senha)
        usuario = Usuario.salvar_usuario(nome, email, senha_hash, ativo)
        return redirect(url_for('usuarios.listar_usuarios'))
    except Exception as e:
        flash(f'Erro ao cadastrar usuário: {str(e)}', 'error')
        return redirect(url_for('usuarios.cadastrar_usuario'))

@usuarios_bp.route('/atualizar_usuario/<int:id_usuario>', methods=['POST'])
def atualizar_usuario_post(id_usuario):
    try:
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        ativo = True if request.form.get('ativo') == 'on' else False
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
        return redirect(url_for('usuarios.listar_usuarios'))
    except Exception as e:
        flash(f'Erro ao atualizar usuário: {str(e)}', 'error')
        return redirect(url_for('usuarios.listar_usuarios'))

@usuarios_bp.route('/deletar_usuario/<int:id_usuario>')
def deletar_usuario(id_usuario):
    try:
        if Usuario.deletar_usuario(id_usuario):
            flash('Usuário removido com sucesso!', 'success')
        else:
            flash('Usuário não encontrado', 'error')
        return redirect(url_for('usuarios.listar_usuarios'))
    except Exception as e:
        flash(f'Erro ao remover usuário: {str(e)}', 'error')
        return redirect(url_for('usuarios.listar_usuarios'))
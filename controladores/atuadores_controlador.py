"""
Controlador para operações relacionadas aos atuadores do sistema IoT.
Gerencia o cadastro, listagem, atualização e remoção de atuadores.
"""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from modelos.iot.atuadores import Atuador

# Criação do blueprint para as rotas de atuadores
atuador_ = Blueprint("atuador_", __name__, template_folder="views")

@atuador_.route('/cadastrar_atuador')
def registrar_atuador():
    """
    Exibe o formulário de cadastro de novo atuador.
    """
    return render_template("registrar_atuador.html")

@atuador_.route('/adicionar_atuador', methods=['POST'])
def adicionar_atuador():
    """
    Processa o formulário de cadastro e salva um novo atuador no banco.
    Redireciona para a página inicial após o cadastro.
    """
    try:
        nome = request.form.get("name")
        marca = request.form.get("brand")
        modelo = request.form.get("model")
        topico = request.form.get("topic")
        unidade = request.form.get("unit")
        ativo = True if request.form.get("is_active") == "on" else False

        Atuador.salvar_atuador(nome, marca, modelo, topico, unidade, ativo)
        flash('Atuador cadastrado com sucesso!', 'success')
        return redirect(url_for('atuador_.listar_atuadores'))
    except Exception as erro:
        flash(f'Erro ao cadastrar atuador: {str(erro)}', 'error')
        return redirect(url_for('atuador_.registrar_atuador'))

@atuador_.route('/atuadores')
def listar_atuadores():
    """
    Lista todos os atuadores cadastrados no sistema.
    """
    try:
        atuadores = Atuador.obter_atuadores()
        return render_template("atuadores.html", atuadores=atuadores)
    except Exception as erro:
        flash(f'Erro ao carregar atuadores: {str(erro)}', 'error')
        return render_template("atuadores.html", atuadores=[])

@atuador_.route('/update_atuador/<int:id_atuador>', methods=['GET', 'POST'])
def atualizar_atuador(id_atuador):
    """
    Exibe formulário de atualização ou processa a atualização de um atuador.

    Args:
        id_atuador (int): ID do atuador a ser atualizado
    """
    if request.method == 'POST':
        try:
            nome = request.form.get("name")
            marca = request.form.get("brand")
            modelo = request.form.get("model")
            topico = request.form.get("topic")
            unidade = request.form.get("unit")
            ativo = True if request.form.get("is_active") == "on" else False

            atuador = Atuador.atualizar_atuador(id_atuador, nome, marca, modelo, topico, unidade, ativo)
            if atuador:
                flash('Atuador atualizado com sucesso!', 'success')
            else:
                flash('Atuador não encontrado.', 'error')
            return redirect(url_for('atuador_.listar_atuadores'))
        except Exception as erro:
            flash(f'Erro ao atualizar atuador: {str(erro)}', 'error')
            return redirect(url_for('atuador_.atualizar_atuador', id_atuador=id_atuador))
    else:
        # GET request - mostrar formulário
        atuador = Atuador.obter_atuador_por_id(id_atuador)
        if atuador:
            return render_template("update_atuador.html", atuador=atuador)
        else:
            flash('Atuador não encontrado.', 'error')
            return redirect(url_for('atuador_.listar_atuadores'))

@atuador_.route('/delete_atuador/<int:id_atuador>', methods=['POST'])
def deletar_atuador(id_atuador):
    """
    Remove um atuador do sistema.

    Args:
        id_atuador (int): ID do atuador a ser removido
    """
    try:
        if Atuador.deletar_atuador(id_atuador):
            flash('Atuador removido com sucesso!', 'success')
        else:
            flash('Atuador não encontrado.', 'error')
    except Exception as erro:
        flash(f'Erro ao remover atuador: {str(erro)}', 'error')

    return redirect(url_for('atuador_.listar_atuadores'))


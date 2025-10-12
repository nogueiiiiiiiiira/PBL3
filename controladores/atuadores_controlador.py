from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from modelos.iot.atuadores import Atuador
atuador_ = Blueprint('atuador_', __name__, template_folder='views')

@atuador_.route('/cadastrar_atuador')
def registrar_atuador():
    return render_template('registrar_atuador.html')

@atuador_.route('/adicionar_atuador', methods=['POST'])
def adicionar_atuador():
    try:
        nome = request.form.get('name')
        marca = request.form.get('brand')
        modelo = request.form.get('model')
        topico = request.form.get('topic')
        unidade = request.form.get('unit')
        ativo = True if request.form.get('is_active') == 'on' else False
        Atuador.salvar_atuador(nome, marca, modelo, topico, unidade, ativo)
        return jsonify({'message': 'Atuador cadastrado com sucesso!', 'redirect': url_for('atuador_.listar_atuadores')})
    except Exception as erro:
        return jsonify({'message': f'Erro ao cadastrar atuador: {str(erro)}'})

@atuador_.route('/atuadores')
def listar_atuadores():
    try:
        atuadores = Atuador.obter_atuadores()
        return render_template('atuadores.html', atuadores=atuadores)
    except Exception as erro:
        return render_template('atuadores.html', atuadores=[])

@atuador_.route('/update_atuador/<int:id_atuador>', methods=['GET', 'POST'])
def atualizar_atuador(id_atuador):
    if request.method == 'POST':
        try:
            nome = request.form.get('name')
            marca = request.form.get('brand')
            modelo = request.form.get('model')
            topico = request.form.get('topic')
            unidade = request.form.get('unit')
            ativo = True if request.form.get('is_active') == 'on' else False
            atuador = Atuador.atualizar_atuador(id_atuador, nome, marca, modelo, topico, unidade, ativo)
            if atuador:
                return jsonify({'message': 'Atuador atualizado com sucesso!', 'redirect': url_for('atuador_.listar_atuadores')})
            else:
                return jsonify({'message': 'Atuador não encontrado.'})
        except Exception as erro:
            return jsonify({'message': f'Erro ao atualizar atuador: {str(erro)}'})
    else:
        atuador = Atuador.obter_atuador_por_id(id_atuador)
        if atuador:
            return render_template('update_atuador.html', atuador=atuador)
        else:
            return jsonify({'message': 'Atuador não encontrado.'})

@atuador_.route('/delete_atuador/<int:id_atuador>')
def deletar_atuador(id_atuador):
    try:
        if Atuador.deletar_atuador(id_atuador):
            return jsonify({'message': 'Atuador removido com sucesso!', 'redirect': url_for('atuador_.listar_atuadores')})
        else:
            return jsonify({'message': 'Atuador não encontrado.'})
    except Exception as erro:
        return jsonify({'message': f'Erro ao remover atuador: {str(erro)}'})

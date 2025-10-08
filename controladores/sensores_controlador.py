"""
Controlador para operações relacionadas aos sensores do sistema IoT.
Gerencia o cadastro, listagem, atualização e remoção de sensores.
"""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from modelos.iot.sensores import Sensor

# Criação do blueprint para as rotas de sensores
sensor_ = Blueprint("sensor_", __name__, template_folder="views")

@sensor_.route('/cadastrar_sensor')
def registrar_sensor():
    """
    Exibe o formulário de cadastro de novo sensor.
    """
    return render_template("registrar_sensor.html")

@sensor_.route('/adicionar_sensor', methods=['POST'])
def adicionar_sensor():
    """
    Processa o formulário de cadastro e salva um novo sensor no banco.
    Redireciona para a página inicial após o cadastro.
    """
    try:
        nome = request.form.get("name")
        marca = request.form.get("brand")
        modelo = request.form.get("model")
        topico = request.form.get("topic")
        unidade = request.form.get("unit")
        ativo = True if request.form.get("is_active") == "on" else False

        Sensor.salvar_sensor(nome, marca, modelo, topico, unidade, ativo)
        flash('Sensor cadastrado com sucesso!', 'success')
        return redirect(url_for('sensor_.listar_sensores'))
    except Exception as erro:
        flash(f'Erro ao cadastrar sensor: {str(erro)}', 'error')
        return redirect(url_for('sensor_.registrar_sensor'))

@sensor_.route('/sensores')
def listar_sensores():
    """
    Lista todos os sensores cadastrados no sistema.
    """
    try:
        sensores = Sensor.obter_sensores()
        return render_template("sensores.html", sensores=sensores)
    except Exception as erro:
        flash(f'Erro ao carregar sensores: {str(erro)}', 'error')
        return render_template("sensores.html", sensores=[])

@sensor_.route('/atualizar_sensor/<int:id_sensor>', methods=['GET', 'POST'])
def atualizar_sensor(id_sensor):
    """
    Exibe formulário de atualização ou processa a atualização de um sensor.

    Args:
        id_sensor (int): ID do sensor a ser atualizado
    """
    if request.method == 'POST':
        try:
            nome = request.form.get("name")
            marca = request.form.get("brand")
            modelo = request.form.get("model")
            topico = request.form.get("topic")
            unidade = request.form.get("unit")
            ativo = True if request.form.get("is_active") == "on" else False

            sensor = Sensor.atualizar_sensor(id_sensor, nome, marca, modelo, topico, unidade, ativo)
            if sensor:
                flash('Sensor atualizado com sucesso!', 'success')
            else:
                flash('Sensor não encontrado.', 'error')
            return redirect(url_for('sensor_.listar_sensores'))
        except Exception as erro:
            flash(f'Erro ao atualizar sensor: {str(erro)}', 'error')
            return redirect(url_for('sensor_.atualizar_sensor', id_sensor=id_sensor))
    else:
        # GET request - mostrar formulário
        sensor = Sensor.obter_sensor_por_id(id_sensor)
        if sensor:
            return render_template("atualizar_sensor.html", sensor=sensor)
        else:
            flash('Sensor não encontrado.', 'error')
            return redirect(url_for('sensor_.listar_sensores'))

@sensor_.route('/deletar_sensor/<int:id_sensor>', methods=['POST'])
def deletar_sensor(id_sensor):
    """
    Remove um sensor do sistema.

    Args:
        id_sensor (int): ID do sensor a ser removido
    """
    try:
        if Sensor.deletar_sensor(id_sensor):
            flash('Sensor removido com sucesso!', 'success')
        else:
            flash('Sensor não encontrado.', 'error')
    except Exception as erro:
        flash(f'Erro ao remover sensor: {str(erro)}', 'error')

    return redirect(url_for('sensor_.listar_sensores'))

function validar_senha() {
    const senha = document.getElementById('senha');
    const confirmar_senha = document.getElementById('confirmar_senha');

    if (senha && confirmar_senha) {
        confirmar_senha.addEventListener('input', function() {
            if (senha.value !== this.value) {
                this.setCustomValidity('As senhas não coincidem');
            } else {
                this.setCustomValidity('');
            }
        });
    }
}

function validar_topico() {
    const entrada_topico = document.getElementById('topic');
    if (entrada_topico) {
        entrada_topico.addEventListener('input', function() {
            const topico = this.value;
            const regex = /^[a-zA-Z0-9/_-]+$/;

            if (!regex.test(topico)) {
                this.setCustomValidity('O tópico deve conter apenas letras, números, barras e underscores');
            } else {
                this.setCustomValidity('');
            }
        });
    }
}

function lidar_com_clique(cb, id) {
    var topico = "";
    if (id == "control") {
        topico = "/atuador";
    }
    var dados = cb.checked ? "1" : "0";
    fetch('/publicar_mensagem', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: dados,
            topic: topico
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        alert('Mensagem enviada com sucesso!');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Erro ao enviar mensagem.');
    });
}

function lidar_com_resposta_ajax(data) {
    if (data.success === false) {
        alert(data.message);
    } else if (data.message) {
        alert(data.message);
        if (data.redirect) {
            window.location.href = data.redirect;
        }
    } else if (data.redirect) {
        window.location.href = data.redirect;
    }
}

function enviar_formulario_ajax(id_formulario) {
    const formulario = document.getElementById(id_formulario);
    if (formulario) {
        formulario.addEventListener('submit', function(e) {
            e.preventDefault();
            const dados_formulario = new FormData(this);
            const url = this.getAttribute('data-url');
            fetch(url, {
                method: 'POST',
                body: dados_formulario
            })
            .then(response => response.json())
            .then(data => lidar_com_resposta_ajax(data))
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
}

function deletar_usuario(id_usuario) {
    if (confirm('Tem certeza que deseja deletar este usuário?')) {
        fetch(`/deletar_usuario/${id_usuario}`, {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => lidar_com_resposta_ajax(data))
        .catch(error => {
            console.error('Error:', error);
            alert('Erro ao deletar usuário.');
        });
    }
}

function deletar_sensor(id_sensor) {
    if (confirm('Tem certeza que deseja deletar este sensor?')) {
        fetch(`/deletar_sensor/${id_sensor}`, {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => lidar_com_resposta_ajax(data))
        .catch(error => {
            console.error('Error:', error);
            alert('Erro ao deletar sensor.');
        });
    }
}

function deletar_atuador(id_atuador) {
    if (confirm('Tem certeza que deseja deletar este atuador?')) {
        fetch(`/delete_atuador/${id_atuador}`, {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => lidar_com_resposta_ajax(data))
        .catch(error => {
            console.error('Error:', error);
            alert('Erro ao deletar atuador.');
        });
    }
}

function desconectar_usuario(event) {
    event.preventDefault();
    if (confirm('Tem certeza que deseja desconectar?')) {
        fetch('/desconectar', {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => lidar_com_resposta_ajax(data))
        .catch(error => {
            console.error('Error:', error);
            alert('Erro ao desconectar.');
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    validar_senha();
    validar_topico();

    // Inicializar formulários AJAX
    enviar_formulario_ajax('registerForm');
    enviar_formulario_ajax('updateForm');
    enviar_formulario_ajax('registerSensorForm');
    enviar_formulario_ajax('updateSensorForm');
    enviar_formulario_ajax('registerAtuadorForm');
    enviar_formulario_ajax('updateAtuadorForm');
    enviar_formulario_ajax('loginForm');

    const data_inicio = document.getElementById('start_date');
    const data_fim = document.getElementById('end_date');
    if (data_inicio && data_fim) {
        const agora = new Date();
        const ontem = new Date(agora.getTime() - (24 * 60 * 60 * 1000));
        const formatar_data_hora = (data) => data.toISOString().slice(0, 16);
        data_inicio.value = formatar_data_hora(ontem);
        data_fim.value = formatar_data_hora(agora);
    }

    const controle = document.getElementById('control');
    if (controle) {
        controle.addEventListener('click', function() {
            lidar_com_clique(this, this.id);
        });
    }

    const link_dropdown = document.getElementById('navbarDropdownMenuLink');
    if (link_dropdown) {
        link_dropdown.addEventListener('click', function(e) {
            e.preventDefault();
            const dropdown = this.nextElementSibling;
            dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
        });
    }
});

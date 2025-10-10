function validatePassword() {
    const senha = document.getElementById('senha');
    const confirmarSenha = document.getElementById('confirmar_senha');

    if (senha && confirmarSenha) {
        confirmarSenha.addEventListener('input', function() {
            if (senha.value !== this.value) {
                this.setCustomValidity('As senhas não coincidem');
            } else {
                this.setCustomValidity('');
            }
        });
    }
}

function validateTopic() {
    const topicInput = document.getElementById('topic');
    if (topicInput) {
        topicInput.addEventListener('input', function() {
            const topic = this.value;
            const regex = /^[a-zA-Z0-9/_-]+$/;

            if (!regex.test(topic)) {
                this.setCustomValidity('O tópico deve conter apenas letras, números, barras e underscores');
            } else {
                this.setCustomValidity('');
            }
        });
    }
}

function handleClick(cb, id) {
    var topic = "";
    if (id == "control") {
        topic = "/atuador";
    }
    var data = cb.checked ? "1" : "0";
    fetch('/publicar_mensagem', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: data,
            topic: topic
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

document.addEventListener('DOMContentLoaded', function() {
    validatePassword();
    validateTopic();

    const startDate = document.getElementById('start_date');
    const endDate = document.getElementById('end_date');
    if (startDate && endDate) {
        const now = new Date();
        const yesterday = new Date(now.getTime() - (24 * 60 * 60 * 1000));
        const formatDateTime = (date) => date.toISOString().slice(0, 16);
        startDate.value = formatDateTime(yesterday);
        endDate.value = formatDateTime(now);
    }

    const control = document.getElementById('control');
    if (control) {
        control.addEventListener('click', function() {
            handleClick(this, this.id);
        });
    }

    const dropdownLink = document.getElementById('navbarDropdownMenuLink');
    if (dropdownLink) {
        dropdownLink.addEventListener('click', function(e) {
            e.preventDefault();
            const dropdown = this.nextElementSibling;
            dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
        });
    }
});

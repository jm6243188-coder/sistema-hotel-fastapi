const BotaoFazerReserva = document.getElementById("BotaoFazerReserva")
BotaoFazerReserva.addEventListener("click", async function (event) {
    event.preventDefault();

    const campoNumero = document.getElementById("Numero");

    const campoHospede = document.getElementById("Hospede");

    const campoQuantidadeDeDiarias = document.getElementById("Quantidade_diarias");

    const numero = Number(campoNumero.value);

    const url = `http://127.0.0.1:8000/quartos/${numero}/reserva`;

    const reserva = {
        hospede: campoHospede.value,
        quantidade_diarias: Number(campoQuantidadeDeDiarias.value)
    }

    const opcoes = {
        method: "PATCH",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(reserva)
    };

    const response = await fetch(url, opcoes);

    const dados = await response.json();

    const Mensagem = document.getElementById("Mensagem");

    if (response.ok) {
        Mensagem.textContent = dados.mensagem;
    }

    else {
        Mensagem.textContent = dados.detail;
    }
    
});

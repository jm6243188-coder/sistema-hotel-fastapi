const ButtonCancelarReserva = document.getElementById("ButtonCancelarReserva");
ButtonCancelarReserva.addEventListener("click", async function (event) {
    event.preventDefault();

    const campoNumero = document.getElementById("Numero");

    const numero = Number(campoNumero.value);

    const url = `http://127.0.0.1:8000/quartos/${numero}/cancelar_reserva`;

    const opcoes = {
        method: "PATCH"
    };

    const response = await fetch(url, opcoes);

    const dados = await response.json();

    const MensagemCancelarReserva = document.getElementById("MensagemCancelarReserva");

    const NumeroCancelarReserva = document.getElementById("NumeroCancelarReserva");

    if (response.ok) {
        MensagemCancelarReserva.textContent = dados.mensagem;
        NumeroCancelarReserva.textContent = `Numero do quarto: ${dados.numero}`;
    }

    else {
        MensagemCancelarReserva.textContent = dados.detail;
        NumeroCancelarReserva.textContent = "";
    }
    
    
});
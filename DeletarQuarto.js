const ButtonDeletarQuarto = document.getElementById("ButtonDeletarQuarto");
ButtonDeletarQuarto.addEventListener("click", async function (event) {
    event.preventDefault();

    const campoNumero = document.getElementById("Numero");

    const numero = Number(campoNumero.value);

    const url = `http://127.0.0.1:8000/quartos/${numero}`;

    const opcoes = {
        method: "DELETE"
    };

    const response = await fetch(url, opcoes);

    const dados = await response.json();

    const MensagemDeletarQuarto = document.getElementById("MensagemDeletarQuarto");

    const NumeroDeletarQuarto = document.getElementById("NumeroDeletarQuarto");

    if (response.ok) {
        MensagemDeletarQuarto.textContent = dados.mensagem;
        NumeroDeletarQuarto.textContent = `Numero do quarto: ${dados.numero}`;
    }

    else {
        MensagemDeletarQuarto.textContent = dados.detail;
        NumeroDeletarQuarto.textContent = "";
    }

    
});
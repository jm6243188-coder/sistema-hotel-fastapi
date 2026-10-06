const ButtonCriarQuarto = document.getElementById("ButtonCriarQuarto");
ButtonCriarQuarto.addEventListener("click", async function (event) {
    event.preventDefault();

    const campoNumero = document.getElementById("numero");

    const CampoValorDiaria = document.getElementById("valor_diaria");

    const url = "http://127.0.0.1:8000/quartos";

    const body = {
        numero: Number(campoNumero.value),
        valor_diaria: Number(CampoValorDiaria.value)
    }

    const opcoes = {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(body)
    };

    const response = await fetch(url, opcoes);

    const dados = await response.json();

    const mensagemCriarQuarto = document.getElementById("mensagemCriarQuarto");

    const numeroCriarQuarto = document.getElementById("numeroCriarQuarto");

    if (response.ok) {
        mensagemCriarQuarto.textContent = dados.mensagem;
        numeroCriarQuarto.textContent = `Numero: ${dados.numero}`;
    }

    else {
        mensagemCriarQuarto.textContent = dados.detail;
        numeroCriarQuarto.textContent = "";
    }
    
    
});
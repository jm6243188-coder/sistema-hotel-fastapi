async function carregarTodosOsQuartos() {
    const urlQuartos = "http://127.0.0.1:8000/quartos";

    const response = await fetch(urlQuartos);

    const quartos = await response.json();

    const ListarTodosOsQuartos = document.getElementById("ListarTodosOsQuartos");

    ListarTodosOsQuartos.innerHTML = "";

    for (const quarto of quartos) {

        const itemQuarto = document.createElement("p");

        let statusQuarto;

        let campoHospede;

        if (quarto.disponivel === 1) {
            statusQuarto = "Disponivel";
            campoHospede = "";
        }

        else {
            statusQuarto = "Ocupado";
            campoHospede = `Hospede: ${quarto.hospede}`;
        }

        itemQuarto.textContent = `Quarto: ${quarto.numero} Valor diaria: ${quarto.valor_diaria}
        Status: ${statusQuarto} ${campoHospede}`;

        ListarTodosOsQuartos.appendChild(itemQuarto);
    }
}

carregarTodosOsQuartos();
# Sistema de Hotel com FastAPI

Projeto desenvolvido para praticar desenvolvimento Backend utilizando Python, FastAPI e SQLite.

O sistema permite gerenciar quartos de um hotel, realizar reservas e cancelar reservas.

## Tecnologias utilizadas

- Python
- FastAPI
- SQLite
- HTML
- CSS
- JavaScript

- ## Funcionalidades

- Criar quartos
- Listar todos os quartos
- Listar quartos disponíveis
- Listar quartos ocupados
- Buscar um quarto específico
- Fazer reserva
- Cancelar reserva
- Deletar quarto

- ## Rotas da API

### Quartos

- `GET /quartos` - Lista todos os quartos
- `GET /quartos/disponiveis` - Lista apenas os quartos disponíveis
- `GET /quarto/especifico{numero}` - Busca um quarto específico
- `POST /quartos` - Cria um novo quarto
- `DELETE /quartos/{numero}` - Deleta um quarto

### Reservas

- `PATCH /quartos/{numero}/reserva` - Faz uma reserva
- `PATCH /quartos/{numero}/cancelar_reserva` - Cancela uma reserva

## Como executar o projeto

1. Clone o repositório:

```bash
git clone https://github.com/jm6243188-coder/sistema-hotel-fastapi.git

cd sistema-hotel-fastapi

pip install fastapi uvicorn

python -m uvicorn api:app --reload

http://127.0.0.1:8000/docs


Essa seção mostra que você sabe não só programar, mas também explicar como outro desenvolvedor consegue executar seu projeto.

Faça essa parte agora. Depois vamos adicionar uma seção curta sobre a **estrutura do projeto** e, por fim, vamos salvar tudo no Git com `add`, `commit` e `push`.

## Estrutura do projeto

```text
sistema-hotel-fastapi/
├── api.py
├── banco.py
├── index.html
├── FazerReserva.html
├── FazerReserva.js
├── CancelarReserva.html
├── CancelarReserva.js
├── CriarQuarto.html
├── CriarQuarto.js
├── DeletarQuarto.html
├── DeletarQuarto.js
├── GerenciarQuartos.html
├── GerenciarQuartos.js
├── style.css
└── README.md


Essa parte ajuda quem abrir seu repositório a entender rapidamente onde está cada coisa:

```text
api.py
→ rotas e regras da API

banco.py
→ conexão e criação do banco

.html
→ páginas

.js
→ comunicação do Frontend com a API

style.css
→ aparência das páginas

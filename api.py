import sqlite3

from fastapi import FastAPI, HTTPException, Path
from banco import conectar_banco, criar_tabela_quartos
from pydantic import BaseModel, Field

app = FastAPI()

conexao = conectar_banco()
criar_tabela_quartos(conexao)
conexao.close()

class EntradaCriarQuarto(BaseModel):
    numero: int
    valor_diaria: float
class SaidaListarQuarto(BaseModel):
    numero: int
    valor_diaria: float
    disponivel: int
    hospede: str | None
class SaidaCriarQuarto(BaseModel):
    mensagem: str
    numero: int
    valor_diaria: float
class SaidaDeletarQuarto(BaseModel):
    mensagem: str
    numero: int
class EntradaFazerReserva(BaseModel):
    hospede: str
    quantidade_diarias: int
class SaidaFazerReserva(BaseModel):
    mensagem: str
    numero: int
    valor_total: float
    quantidade_diarias: int
    hospede: str
class SaidaCancelarReserva(BaseModel):
    mensagem: str
    numero: int

@app.get("/quartos", response_model=list[SaidaListarQuarto])
def listar_quartos():
    conexao = conectar_banco()

    try:
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM quartos")

        quartos_encontrados = cursor.fetchall()
        if quartos_encontrados == []:

            raise HTTPException(
                status_code=404,
                detail="Nenhum quarto encontrado"
            )

        resultado = []


        for quarto in quartos_encontrados:
            resultado.append({
                "numero": quarto[0],
                "valor_diaria": quarto[1],
                "disponivel": quarto[2],
                "hospede": quarto[3]
            })

        return resultado

    except sqlite3.Error as erro:

        print(f"Erro no listar quarto: {erro}")

        raise HTTPException(
            status_code=500,
            detail="Erro interno no SQLITE"
        )

    finally:
        conexao.close()

@app.get("/quartos/disponiveis", response_model=list[SaidaListarQuarto])
def listar_quartos_disponiveis():
    conexao = conectar_banco()

    try:
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT * FROM quartos WHERE disponivel = ?",
            (1,)
        )

        quartos_encontrados = cursor.fetchall()
        if quartos_encontrados == []:

            raise HTTPException(
                status_code=404,
                detail="Nenhum quarto encontrado"
            )

        resultado = []

        for quarto in quartos_encontrados:
            resultado.append({
                "numero": quarto[0],
                "valor_diaria": quarto[1],
                "disponivel": quarto[2],
                "hospede": quarto[3]
            })

        return resultado

    except sqlite3.Error as erro:

        print(f"Erro no listar quartos disponiveis: {erro}")

        raise HTTPException(
            status_code=500,
            detail="Erro interno no SQLITE"
        )

    finally:
        conexao.close()

@app.post("/quartos", response_model=SaidaCriarQuarto)
def criar_quarto(quarto: EntradaCriarQuarto):
    conexao = conectar_banco()

    try:
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT * FROM quartos WHERE numero = ?",
            (quarto.numero,)
        )

        quarto_encontrado = cursor.fetchone()
        if quarto_encontrado is not None:

            raise HTTPException(
                status_code=409,
                detail="Ja existe um quarto neste numero"
            )

        cursor.execute("""
            INSERT INTO quartos (numero, valor_diaria, disponivel, hospede)
            VALUES (?, ?, ?, ?)
            """, (quarto.numero, quarto.valor_diaria, 1, None)
        )

        conexao.commit()

        return {
            "mensagem": "Quarto criado com sucesso",
            "numero": quarto.numero,
            "valor_diaria": quarto.valor_diaria
        }

    except sqlite3.Error as erro:
        conexao.rollback()

        print(f"Erro no criar quarto: {erro}")

        raise HTTPException(
            status_code=500,
            detail="Erro interno no SQLITE"
        )

    finally:
        conexao.close()  

@app.get("/quarto/especifico{numero}", response_model=SaidaListarQuarto)
def listar_quarto_especifico(numero: int = Path(gt=0)):
    conexao = conectar_banco()

    try:
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT * FROM quartos WHERE numero = ?",
            (numero,)
        )

        quarto_encontrado = cursor.fetchone()
        if quarto_encontrado is None:

            raise HTTPException(
                status_code=404,
                detail="Nenhum quarto encontrado"
            )

        return {
            "numero": quarto_encontrado[0],
            "valor_diaria": quarto_encontrado[1],
            "disponivel": quarto_encontrado[2],
            "hospede": quarto_encontrado[3]
        }

    except sqlite3.Error as erro:

        print(f"Erro no listar quarto especifico: {erro}")

        raise HTTPException(
            status_code=500,
            detail="Erro interno no SQLITE"
        )

    finally:
        conexao.close()

@app.delete("/quartos/{numero}", response_model=SaidaDeletarQuarto)
def deletar_quarto(numero: int = Path(gt=0)):
    conexao = conectar_banco()

    try:
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT * FROM quartos WHERE numero = ?",
            (numero,)
        )

        quarto_encontrado = cursor.fetchone()
        if quarto_encontrado is None:

            raise HTTPException(
                status_code=404,
                detail="Nenhum quarto encontrado"
            )

        elif quarto_encontrado[2] == 0:

            raise HTTPException(
                status_code=409,
                detail="O quarto ja esta ocupado, não é possivel deletar."
            )

        cursor.execute(
            "DELETE FROM quartos WHERE numero = ?",
            (numero,)
        )

        conexao.commit()


        return {
            "mensagem": "Quarto deletado com sucesso",
            "numero": numero
        }

    except sqlite3.Error as erro:
        conexao.rollback()

        print(f"Erro no deletar quarto: {erro}")

        raise HTTPException(
            status_code=500,
            detail="Erro interno no SQLITE"
        )

    finally:
        conexao.close()

@app.patch("/quartos/{numero}/reserva", response_model=SaidaFazerReserva)
def fazer_reserva(quarto: EntradaFazerReserva, numero: int = Path(gt=0)):
    conexao = conectar_banco()

    try:
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT * FROM quartos WHERE numero = ?",
            (numero,)
        )

        quarto_encontrado = cursor.fetchone()
        if quarto_encontrado is None:

            raise HTTPException(
                status_code=404,
                detail="Nenhum quarto encontrado"
            )

        elif quarto_encontrado[2] == 0:

            raise HTTPException(
                status_code=409,
                detail="Este quarto ja esta ocupado, não é possivel fazer reserva."
            )

        valor_total = quarto_encontrado[1] * quarto.quantidade_diarias

        cursor.execute("""
        UPDATE quartos
        SET disponivel = ?, hospede = ?
        WHERE numero = ?
        """, (0, quarto.hospede, numero)
        )

        conexao.commit()

        return {
            "mensagem": "Reserva realizada com sucesso",
            "numero": numero,
            "quantidade_diarias": quarto.quantidade_diarias,
            "hospede": quarto.hospede,
            "valor_total": valor_total
        }

    except sqlite3.Error as erro:
        conexao.rollback()

        print(f"Erro no fazer reserva: {erro}")

        raise HTTPException(
            status_code=500,
            detail="Erro interno no SQLITE"
        )

    finally:
        conexao.close()

@app.patch("/quartos/{numero}/cancelar_reserva", response_model=SaidaCancelarReserva)
def cancelar_reserva(numero: int = Path(gt=0)):
    conexao = conectar_banco()

    try:
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT * FROM quartos WHERE numero = ?",
            (numero,)
        )

        quarto_encontrado = cursor.fetchone()
        if quarto_encontrado is None:

            raise HTTPException(
                status_code=404,
                detail="Nenhum quarto encontrado"
            )

        elif quarto_encontrado[2] == 1:

            raise HTTPException(
                status_code=409,
                detail="Para cancelar uma reserva, escolha um quarto ocupado."
            )

        cursor.execute("""
        UPDATE quartos
        SET disponivel = ?, hospede = ?
        WHERE numero = ?
        """, (1, None, numero)
        )

        conexao.commit()

        return {
            "mensagem": "Reserva cancelada",
            "numero": numero
        }

    except sqlite3.Error as erro:
        conexao.rollback()

        print(f"Erro no cancelar reserva: {erro}")

        raise HTTPException(
            status_code=500,
            detail="Erro interno no SQLITE"
        )

    finally:
        conexao.close()
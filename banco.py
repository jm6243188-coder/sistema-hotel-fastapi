import sqlite3

def conectar_banco():
    conexao = sqlite3.connect("BancoDados.db")

    return conexao

def criar_tabela_quartos(conexao: sqlite3.Connection):
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quartos (
    numero INTEGER PRIMARY KEY,
    valor_diaria REAL,
    disponivel INTEGER,
    hospede TEXT
    )
    """)

    conexao.commit()



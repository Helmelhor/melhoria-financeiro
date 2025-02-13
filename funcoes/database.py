import sqlite3
from sqlite3 import Error

def criar_tabela_metas():
    banco = sqlite3.connect("banco_melhoria.db")
    #permite executar comandos
    cursor = banco.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Metas_Financeiras (
        metas TEXT, 
        quanto_tenho NUMERIC, 
        valor_meta NUMERIC, 
        contribuicao_mensal NUMERIC
    )
    """)
    banco.commit()
    banco.close()

def adicionar_meta(metas, quanto_tenho, valor_meta, contribuicao_mensal):
    banco = sqlite3.connect("banco_melhoria.db")
    cursor = banco.cursor()
    cursor.execute("""
    INSERT INTO Metas_Financeiras (metas, quanto_tenho, valor_meta, contribuicao_mensal) 
    VALUES (?, ?, ?, ?)
    """, (metas, quanto_tenho, valor_meta, contribuicao_mensal))
    banco.commit()
    banco.close()

def buscar_metas():
    banco = sqlite3.connect("banco_melhoria.db")
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM Metas_Financeiras")
    metas = cursor.fetchall() #recupera todas as querys
    banco.close()
    return metas

def atualizar_progresso(metas, quanto_tenho):
    banco = sqlite3.connect("banco_melhoria.db")
    cursor = banco.cursor()
    cursor.execute("""
    UPDATE Metas_Financeiras 
    SET quanto_tenho = ? 
    WHERE metas = ?
    """, (quanto_tenho, metas))
    banco.commit()
    banco.close()
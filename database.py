import sqlite3
from sqlite3 import Error

# Função para conectar ao banco de dados
def conectar():
    try:
        conn = sqlite3.connect('database.db')  # Cria ou abre o arquivo do banco de dados
        return conn
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para criar a tabela de metas
def criar_tabela_metas():
    conn = conectar()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    valor_total REAL NOT NULL,
                    valor_economizado REAL DEFAULT 0,
                    prazo TEXT NOT NULL,
                    categoria TEXT,
                    status TEXT DEFAULT 'Em andamento'
                )
            ''')
            conn.commit()
            print("Tabela 'metas' criada com sucesso!")
        except Error as e:
            print(f"Erro ao criar tabela: {e}")
        finally:
            conn.close()

# Função para adicionar uma meta
def adicionar_meta(nome, valor_total, prazo, categoria):
    conn = conectar()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO metas (nome, valor_total, prazo, categoria)
                VALUES (?, ?, ?, ?)
            ''', (nome, valor_total, prazo, categoria))
            conn.commit()
            print("Meta adicionada com sucesso!")
        except Error as e:
            print(f"Erro ao adicionar meta: {e}")
        finally:
            conn.close()

# Função para buscar todas as metas
def buscar_metas():
    conn = conectar()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM metas')
            return cursor.fetchall()  # Retorna todas as metas
        except Error as e:
            print(f"Erro ao buscar metas: {e}")
        finally:
            conn.close()
    return []

# Função para atualizar o progresso de uma meta
def atualizar_progresso(id_meta, valor_adicionado):
    conn = conectar()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE metas
                SET valor_economizado = valor_economizado + ?
                WHERE id = ?
            ''', (valor_adicionado, id_meta))
            conn.commit()
            print("Progresso atualizado com sucesso!")
        except Error as e:
            print(f"Erro ao atualizar progresso: {e}")
        finally:
            conn.close()
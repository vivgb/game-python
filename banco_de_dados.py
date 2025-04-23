import sqlite3

def conectar_banco():
    """Conecta ao banco de dados e cria a tabela de usuários, se não existir."""
    conexao = sqlite3.connect("cat.jump")
    db_cursor = conexao.cursor()
    db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        usuario TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
    """)
    conexao.commit()
    return conexao, db_cursor

def cadastrar_usuario(conexao, db_cursor, nome, usuario, senha):
    """
    Cadastra um novo usuário no banco de dados.
    Retorna True se o cadastro for bem-sucedido, False caso contrário.
    """
    try:
        db_cursor.execute("INSERT INTO usuarios (nome, usuario, senha) VALUES (?, ?, ?)", (nome, usuario, senha))
        conexao.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def autenticar_usuario(db_cursor, usuario, senha):
    """
    Verifica se o usuário e a senha correspondem a um registro no banco de dados.
    Retorna o registro do usuário se a autenticação for bem-sucedida, None caso contrário.
    """
    db_cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
    return db_cursor.fetchone()

# Exemplo de uso para interface:
# 1. Conectar ao banco de dados
# conexao, db_cursor = conectar_banco()

# 2. Usar as funções `cadastrar_usuario` e `autenticar_usuario` com os dados fornecidos pela interface
# 3. Não fechar a conexão até finalizar todas as operações

import sqlite3

# Criar ou conectar ao banco de dados
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Criar tabela para armazenar usuários
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
)
''')

conn.commit()
conn.close()

def registrar_usuario(email, senha):
    try:
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (email, senha) VALUES (?, ?)', (email, senha))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False  # Retorna False se o e-mail já existir

def autenticar_usuario(email, senha):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE email = ? AND senha = ?', (email, senha))
    user = cursor.fetchone()
    conn.close()
    return user is not None

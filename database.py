import sqlite3

# Conexão com o banco de dados
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Criar a tabela de usuários, se não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
)
""")
conn.commit()

def registrar_usuario(email, senha):
    try:
        cursor.execute("INSERT INTO usuarios (email, senha) VALUES (?, ?)", (email, senha))
        conn.commit()
        return True  # Sucesso
    except sqlite3.IntegrityError:
        return False  # Email já registrado

def autenticar_usuario(email, senha):
    cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
    return cursor.fetchone() is not None

if start_button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
    if autenticar_usuario(email_text, password_text):
        print("Login bem-sucedido!")  # Aqui você pode redirecionar para outra tela
    else:
        print("E-mail ou senha incorretos.")

if start_button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
    if password_text == confirm_password_text:
        if registrar_usuario(email_text, password_text):
            print("Conta criada com sucesso!")
            running = False  # Fecha a tela de criação de conta
        else:
            print("Erro: E-mail já registrado.")
    else:
        print("As senhas não correspondem.")

conn.close()

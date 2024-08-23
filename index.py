import customtkinter as ctk
from tkinter import Toplevel
from pymongo import MongoClient
import wmi
import socket
from datetime import datetime

# Função para obter o serial da BIOS
def get_bios_serial():
    """Obtém o serial da BIOS da máquina local."""
    c = wmi.WMI()
    bios_serial = c.Win32_BIOS()[0].SerialNumber.strip()
    return bios_serial

# Função para obter a data e hora atual
def get_current_timestamp():
    """Obtém a data e hora atual."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Configuração da conexão com o MongoDB Atlas
client = MongoClient('mongodb+srv://neox:jppaguilar2010@cluster0.zxonb.mongodb.net/')
db = client['logins']
users_collection = db['users']
logs_collection = db['logs']

def log_user_login(username, bios_serial):
    """Registra o login do usuário na coleção de logs."""
    timestamp = get_current_timestamp()
    log_document = {
        "username": username,
        "bios": bios_serial,
        "timestamp": timestamp
    }
    logs_collection.insert_one(log_document)
    print(f"Login registrado para usuário {username}.")

def authenticate_user():
    """Autentica um usuário existente."""
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if not username or not password:
        show_custom_message("Entrada Inválida", "Por favor, preencha todos os campos.", "warning")
        return

    user = users_collection.find_one({'username': username})

    if user and user['password'] == password:
        bios_serial_local = get_bios_serial()
        if user['bios'] == bios_serial_local:
            log_user_login(username, bios_serial_local)
            show_custom_message("Sucesso", f"Usuário {username} autenticado com sucesso.", "info")
        else:
            show_custom_message("Falha na Autenticação", "Acesso negado. BIOS não corresponde.", "error")
    else:
        show_custom_message("Falha na Autenticação", "Nome de usuário ou senha incorretos.", "error")

def show_custom_message(title, message, msg_type):
    """Mostra uma caixa de mensagem personalizada que aparece na frente de todos os programas e bloqueia a janela principal."""
    message_window = Toplevel(app)
    message_window.title(title)
    message_window.geometry("300x150")
    message_window.minsize(300, 150)  # Define o tamanho mínimo da janela de alerta
    message_window.configure(bg="#333333")
    message_window.transient(app)  # Faz a janela modal ficar em cima da janela principal
    message_window.grab_set()  # Impede interação com a janela principal até que a modal seja fechada
    message_window.focus_set()  # Foca na janela modal

    # Mensagem
    msg_label = ctk.CTkLabel(message_window, text=message, text_color="#ffffff", bg_color="#333333")
    msg_label.pack(pady=20, padx=20, fill="both", expand=True)

    if msg_type == "warning":
        msg_label.configure(text_color="#f1c40f")
    elif msg_type == "error":
        msg_label.configure(text_color="#e74c3c")
    elif msg_type == "info":
        msg_label.configure(text_color="#3498db")

    button_ok = ctk.CTkButton(message_window, text="OK", command=message_window.destroy)
    button_ok.pack(pady=(0, 20), padx=10, anchor='s', side='bottom')

# Configuração da Interface Gráfica Principal
app = ctk.CTk()
app.title("Psicos - Login")
app.geometry("600x350")  # Ajusta o tamanho inicial da janela
app.minsize(600, 350)   # Define o tamanho mínimo da janela

# Definindo o tema e o modo de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Barra lateral azul
frame_sidebar = ctk.CTkFrame(app, width=150, corner_radius=0, fg_color="#1e90ff")
frame_sidebar.pack(side="left", fill="y")

# Seção de Autenticação
frame_auth = ctk.CTkFrame(app, corner_radius=20, fg_color="#333333")  # Cor de fundo cinza
frame_auth.pack(side="right", padx=15, pady=25, fill="both", expand=True)

entry_username = ctk.CTkEntry(frame_auth, placeholder_text="Nome de Usuário", corner_radius=10)
entry_username.pack(pady=10, padx=20, fill="x")
entry_username.configure(justify="center")  # Centraliza o texto na caixa de entrada

entry_password = ctk.CTkEntry(frame_auth, placeholder_text="Senha", show='*', corner_radius=10)
entry_password.pack(pady=10, padx=20, fill="x")
entry_password.configure(justify="center")  # Centraliza o texto na caixa de entrada

# Botão de autenticar posicionado centralizado na parte inferior do retângulo cinza
button_authenticate = ctk.CTkButton(frame_auth, text="Autenticar Usuário", command=authenticate_user)
button_authenticate.pack(pady=(10, 10), padx=10, anchor='s', side='bottom', fill='x')

# Iniciar a aplicação
app.mainloop()

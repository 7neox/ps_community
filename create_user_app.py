import customtkinter as ctk
from tkinter import messagebox
from pymongo import MongoClient

# Configuração da conexão com o MongoDB Atlas
client = MongoClient('mongodb+srv://neox:jppaguilar2010@cluster0.zxonb.mongodb.net/')  # Substitua pela URI de conexão do MongoDB Atlas
db = client['logins']
users_collection = db['users']

def create_user():
    """Cria um novo usuário e armazena no banco de dados."""
    username = entry_username.get()
    password = entry_password.get()
    bios_serial = entry_bios.get()

    if not username or not password or not bios_serial:
        messagebox.showwarning("Entrada Inválida", "Por favor, preencha todos os campos.")
        return

    user = {
        'username': username,
        'password': password,
        'bios': bios_serial
    }

    # Adiciona o usuário à coleção no MongoDB
    try:
        users_collection.insert_one(user)
        messagebox.showinfo("Sucesso", f"Usuário {username} criado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao criar o usuário: {e}")

# Configuração da Interface Gráfica Principal
app = ctk.CTk()
app.title("Criar Novo Usuário")
app.geometry("600x400")  # Ajusta o tamanho inicial da janela
app.minsize(400, 300)   # Define o tamanho mínimo da janela

# Definindo o tema e o modo de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Barra Azul Lateral
frame_sidebar = ctk.CTkFrame(app, width=150, corner_radius=0, fg_color="#007BFF")
frame_sidebar.pack(side="left", fill="y")

# Seção de Criação de Usuário
frame_create_user = ctk.CTkFrame(app, corner_radius=20, fg_color="#333333")  # Cor de fundo cinza
frame_create_user.pack(pady=25, padx=25, fill="both", expand=True)

# Usando grid para posicionar os widgets dentro de frame_create_user
frame_create_user.grid_rowconfigure(4, weight=1)
frame_create_user.grid_columnconfigure(0, weight=1)

entry_username = ctk.CTkEntry(frame_create_user, placeholder_text="Nome de Usuário", corner_radius=10)
entry_username.grid(row=0, column=0, pady=10, padx=10, sticky="ew")
entry_username.configure(justify="center")

entry_password = ctk.CTkEntry(frame_create_user, placeholder_text="Senha", show='*', corner_radius=10)
entry_password.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
entry_password.configure(justify="center")

entry_bios = ctk.CTkEntry(frame_create_user, placeholder_text="Serial da BIOS", corner_radius=10)
entry_bios.grid(row=2, column=0, pady=10, padx=10, sticky="ew")
entry_bios.configure(justify="center")

# Frame para o botão
frame_button = ctk.CTkFrame(frame_create_user, corner_radius=0, fg_color="#333333")
frame_button.grid(row=3, column=0, pady=(10, 10), padx=10, sticky="se")

# Botão para criar o usuário
button_create_user = ctk.CTkButton(frame_button, text="Criar Usuário", command=create_user)
button_create_user.pack()

# Iniciar a aplicação
app.mainloop()

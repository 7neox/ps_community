import customtkinter as ctk
import wmi
import pyperclip

class BiosApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Código da BIOS")
        self.geometry("400x300")
        self.minsize(300, 200)
        
        # Definindo o tema e o modo de aparência
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configuração do layout
        self.create_widgets()

    def create_widgets(self):
        """Cria e posiciona todos os widgets da interface gráfica."""
        frame_main = ctk.CTkFrame(self, corner_radius=20, fg_color="#333333")
        frame_main.pack(pady=25, padx=25, fill="both", expand=True)

        self.button_show_bios = ctk.CTkButton(frame_main, text="Mostrar Código da BIOS", command=self.display_bios_serial)
        self.button_show_bios.pack(pady=10, padx=20, fill="x")

        self.label_bios_serial = ctk.CTkLabel(frame_main, text="", text_color="#ffffff", bg_color="#333333")
        self.label_bios_serial.pack(pady=10, padx=20)

        self.button_copy = ctk.CTkButton(frame_main, text="Copiar Código", command=self.copy_to_clipboard, state="disabled")
        self.button_copy.pack(pady=10, padx=20)

    def get_bios_serial(self):
        """Obtém o serial da BIOS da máquina local."""
        try:
            c = wmi.WMI()
            bios_serial = c.Win32_BIOS()[0].SerialNumber.strip()
        except Exception as e:
            bios_serial = f"Erro ao obter serial: {e}"
        return bios_serial

    def display_bios_serial(self):
        """Mostra o código da BIOS na mesma janela."""
        bios_serial = self.get_bios_serial()
        self.label_bios_serial.configure(text=bios_serial)
        self.button_copy.configure(state="normal")

    def copy_to_clipboard(self):
        """Copia o código da BIOS para a área de transferência."""
        bios_serial = self.label_bios_serial.cget("text")
        if bios_serial:
            pyperclip.copy(bios_serial)
            
    def show_custom_message(self, title, message):
        """Mostra uma caixa de mensagem personalizada."""
        message_window = ctk.CTkToplevel(self)
        message_window.title(title)
        message_window.geometry("250x100")
        message_window.configure(bg="#333333")

        msg_label = ctk.CTkLabel(message_window, text=message, text_color="#ffffff", bg_color="#333333")
        msg_label.pack(pady=20, padx=20)

        button_ok = ctk.CTkButton(message_window, text="OK", command=message_window.destroy)
        button_ok.pack(pady=10, padx=10)

if __name__ == "__main__":
    app = BiosApp()
    app.mainloop()

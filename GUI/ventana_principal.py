import customtkinter as ctk
from Database.conexion_pg import obtener_conexion

class AppCrystal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Crystal - Ecosistema de Defensa Activa")
        self.geometry("700x400")
        ctk.set_appearance_mode("dark")
        # Tema dark mode/cyberpunk
        self.configure(fg_color="#0d0d0d")

        self.label = ctk.CTkLabel(self, text="Visor de Logs de Amenazas - En Tiempo Real", font=("Consolas", 18, "bold"), text_color="#a832a8")
        self.label.pack(pady=15)

        self.textbox = ctk.CTkTextbox(self, width=650, height=300, text_color="#00FF00", fg_color="#1a1a1a", font=("Consolas", 12))
        self.textbox.pack(pady=10)

        self.actualizar_logs()

    def actualizar_logs(self):
        self.textbox.delete("0.0", "end")
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT fecha, ip_atacante, tipo_ataque, estado_bloqueo FROM eventos_amenaza ORDER BY id DESC LIMIT 15")
            filas = cursor.fetchall()
            
            for fila in filas:
                estado = " [ BLOQUEADO EN FIREWALL ]" if fila[3] else " [ DETECTADO - PENDIENTE ]"
                texto = f"> {fila[0].strftime('%H:%M:%S')} | IP: {fila[1]} | {fila[2]} | {estado}\n\n"
                self.textbox.insert("end", texto)
                
            cursor.close()
            conexion.close()
        except Exception as e:
            self.textbox.insert("end", "> Conectando al bus de eventos de PostgreSQL...\n")
        
        self.after(2000, self.actualizar_logs)

def iniciar_gui():
    app = AppCrystal()
    app.mainloop()
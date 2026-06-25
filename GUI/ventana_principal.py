import customtkinter as ctk
from tkinter import ttk
from Database.conexion_pg import obtener_conexion

# Configuración base del tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CrystalGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Crystal - Centro de Comando")
        self.geometry("1000x650")
        
        # --- Sistema de Pestañas ---
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.tab_vivo = self.tabview.add("Terminales en Vivo")
        self.tab_historial = self.tabview.add("Historial de Amenazas")
        
        self._configurar_pestana_vivo()
        self._configurar_pestana_historial()

    def _configurar_pestana_vivo(self):
        # Grid para dividir la pantalla en dos (Kalopsia izquierda, Paladin derecha)
        self.tab_vivo.columnconfigure(0, weight=1)
        self.tab_vivo.columnconfigure(1, weight=1)
        self.tab_vivo.rowconfigure(1, weight=1)

        # --- Consola Kalopsia ---
        self.lbl_kalopsia = ctk.CTkLabel(self.tab_vivo, text="[ KALOPSIA - SENSOR ]", font=("Consolas", 14, "bold"), text_color="#00FF41")
        self.lbl_kalopsia.grid(row=0, column=0, pady=(10, 5))
        
        self.consola_kalopsia = ctk.CTkTextbox(self.tab_vivo, font=("Consolas", 12), fg_color="#0A0A0A", text_color="#00FF41")
        self.consola_kalopsia.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.consola_kalopsia.insert("end", "> Inicializando Honeypot en puerto 8080...\n")

        # --- Consola Paladin ---
        self.lbl_paladin = ctk.CTkLabel(self.tab_vivo, text="[ PALADIN - IPS ]", font=("Consolas", 14, "bold"), text_color="#00FFFF")
        self.lbl_paladin.grid(row=0, column=1, pady=(10, 5))
        
        self.consola_paladin = ctk.CTkTextbox(self.tab_vivo, font=("Consolas", 12), fg_color="#0A0A0A", text_color="#00FFFF")
        self.consola_paladin.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.consola_paladin.insert("end", "> Escuchando bus de eventos en PostgreSQL...\n")

    def _configurar_pestana_historial(self):
        # Botón para refrescar
        self.btn_actualizar = ctk.CTkButton(self.tab_historial, text="Refrescar Base de Datos", command=self.cargar_historial, fg_color="#5A005A", hover_color="#800080")
        self.btn_actualizar.pack(pady=10)

        # Estilo de la tabla para que coincida con el tema oscuro
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#121212", foreground="white", fieldbackground="#121212", borderwidth=0)
        style.configure("Treeview.Heading", background="#222222", foreground="#E0E0E0", font=("Consolas", 11, "bold"))
        style.map('Treeview', background=[('selected', '#5A005A')])

        # Creación de la tabla
        columnas = ("fecha", "ip", "puerto", "estado")
        self.tabla = ttk.Treeview(self.tab_historial, columns=columnas, show="headings", height=20)
        self.tabla.heading("fecha", text="TIMESTAMP")
        self.tabla.heading("ip", text="IP ORIGEN")
        self.tabla.heading("puerto", text="PUERTO / API")
        self.tabla.heading("estado", text="ACCIÓN IPS")
        
        self.tabla.column("fecha", width=180, anchor="center")
        self.tabla.column("ip", width=150, anchor="center")
        self.tabla.column("puerto", width=120, anchor="center")
        self.tabla.column("estado", width=200, anchor="center")
        
        self.tabla.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Carga inicial
        self.cargar_historial()

    # --- Métodos para inyectar texto desde main.py ---
    def log_kalopsia(self, mensaje):
        self.consola_kalopsia.insert("end", f"> {mensaje}\n")
        self.consola_kalopsia.see("end") 

    def log_paladin(self, mensaje):
        self.consola_paladin.insert("end", f"> {mensaje}\n")
        self.consola_paladin.see("end")

    def cargar_historial(self):
        # Limpiar tabla
        for row in self.tabla.get_children():
            self.tabla.delete(row)
            
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            # Ajusta los nombres de las columnas según tu pgAdmin
            cursor.execute("SELECT fecha_hora, ip_origen, puerto_destino, estado FROM eventos_amenaza ORDER BY fecha_hora DESC")
            registros = cursor.fetchall()
            
            for reg in registros:
                self.tabla.insert("", "end", values=(reg[0], reg[1], reg[2], reg[3]))
                
            cursor.close()
            conexion.close()
        except Exception as e:
            self.tabla.insert("", "end", values=("ERROR", "BD", "DESCONECTADA", str(e)))

if __name__ == "__main__":
    app = CrystalGUI()
    app.mainloop()
import customtkinter as ctk
from tkinter import ttk, messagebox # Agregamos messagebox para las alertas
from Database.conexion_pg import obtener_conexion
from datetime import datetime

# Configuración base del tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CrystalGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Crystal - Centro de Comando")
        self.geometry("1000x700") # Un poco más alto para que quepan los botones
        
        # --- PANEL DE CONTROL (Nuevos Botones) ---
        self.frame_controles = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_controles.pack(pady=(15, 0), padx=20, fill="x")

        self.btn_reporte = ctk.CTkButton(self.frame_controles, text="Exportar Reporte (CSV)", 
                                         command=self.exportar_reporte, fg_color="#005599", hover_color="#003366", font=("Arial", 12, "bold"))
        self.btn_reporte.pack(side="left", padx=10)

        self.btn_panico = ctk.CTkButton(self.frame_controles, text="MODO PÁNICO (Aislar Red)", 
                                        command=self.modo_panico, fg_color="#AA0000", hover_color="#660000", font=("Arial", 12, "bold"))
        self.btn_panico.pack(side="left", padx=10)

        # --- Sistema de Pestañas ---
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.tab_vivo = self.tabview.add("Terminales en Vivo")
        self.tab_historial = self.tabview.add("Historial de Amenazas")
        
        self._configurar_pestana_vivo()
        self._configurar_pestana_historial()

    def _configurar_pestana_vivo(self):
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
        self.btn_actualizar = ctk.CTkButton(self.tab_historial, text="Refrescar Base de Datos", command=self.cargar_historial, fg_color="#5A005A", hover_color="#800080")
        self.btn_actualizar.pack(pady=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#121212", foreground="white", fieldbackground="#121212", borderwidth=0)
        style.configure("Treeview.Heading", background="#222222", foreground="#E0E0E0", font=("Consolas", 11, "bold"))
        style.map('Treeview', background=[('selected', '#5A005A')])

        # Columnas ajustadas
        columnas = ("id", "ip", "ataque", "estado")
        self.tabla = ttk.Treeview(self.tab_historial, columns=columnas, show="headings", height=20)
        self.tabla.heading("id", text="ID EVENTO")
        self.tabla.heading("ip", text="IP ATACANTE")
        self.tabla.heading("ataque", text="TIPO DE ATAQUE")
        self.tabla.heading("estado", text="ESTADO BLOQUEO")
        
        self.tabla.column("id", width=100, anchor="center")
        self.tabla.column("ip", width=150, anchor="center")
        self.tabla.column("ataque", width=180, anchor="center")
        self.tabla.column("estado", width=150, anchor="center")
        
        self.tabla.pack(fill="both", expand=True, padx=15, pady=15)
        self.cargar_historial()

    def exportar_reporte(self):
        try:
            # 1. Obtenemos los datos reales de la BD
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, ip_atacante, tipo_ataque, estado_bloqueo FROM eventos_amenaza ORDER BY id ASC")
            registros = cursor.fetchall()
            cursor.close()
            conexion.close()

            # 2. Creamos el archivo de texto
            fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"Historial_Crystal_{fecha_actual}.txt"

            with open(nombre_archivo, "w", encoding='utf-8') as archivo:
                archivo.write("=================================================\n")
                archivo.write("      REPORTE DE INCIDENTES - SISTEMA CRYSTAL    \n")
                archivo.write("=================================================\n\n")

                # Sección de Kalopsia
                archivo.write("--- [ REGISTROS DEL SENSOR - KALOPSIA ] ---\n")
                for reg in registros:
                    archivo.write(f"ID: {reg[0]} | IP: {reg[1]} | Intento a: {reg[2]}\n")
                
                archivo.write("\n")

                # Sección de Paladin
                archivo.write("--- [ ACCIONES DE MITIGACIÓN - PALADIN ] ---\n")
                for reg in registros:
                    estado = "BLOQUEADO (Firewall)" if reg[3] else "PENDIENTE"
                    archivo.write(f"ID: {reg[0]} | IP Atacante: {reg[1]} | Acción IPS: {estado}\n")

            # 3. Avisamos en la interfaz
            messagebox.showinfo("Auditoría de Seguridad", f"Historial TXT generado con éxito.\n\nSe ha guardado el archivo:\n{nombre_archivo}")
            self.log_paladin(f"[SISTEMA] Reporte TXT exportado.")

        except Exception as e:
            messagebox.showerror("Error de Exportación", f"No se pudo generar el reporte: {e}")

    def modo_panico(self):
        respuesta = messagebox.askyesno("ALERTA CRÍTICA", "¿Estás seguro de activar el Modo Pánico?\n\nEsto cortará todo el tráfico de red entrante al servidor.")
        if respuesta:
            self.log_paladin("[!!!] MODO PÁNICO ACTIVADO. Aislando servidor del perímetro...")
            messagebox.showwarning("Aislamiento Completo", "El servidor ha sido aislado de la red pública.")

    # --- Métodos para inyectar texto desde main.py ---
    def log_kalopsia(self, mensaje):
        self.consola_kalopsia.insert("end", f"> {mensaje}\n")
        self.consola_kalopsia.see("end") 

    def log_paladin(self, mensaje):
        self.consola_paladin.insert("end", f"> {mensaje}\n")
        self.consola_paladin.see("end")

    def cargar_historial(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
            
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            # FIX CRÍTICO: Ajustado a las columnas reales que usa tu BD ahora
            cursor.execute("SELECT id, ip_atacante, tipo_ataque, estado_bloqueo FROM eventos_amenaza ORDER BY id DESC")
            registros = cursor.fetchall()
            
            for reg in registros:
                estado_texto = "BLOQUEADO" if reg[3] else "PENDIENTE"
                self.tabla.insert("", "end", values=(reg[0], reg[1], reg[2], estado_texto))
                
            cursor.close()
            conexion.close()
        except Exception as e:
            self.tabla.insert("", "end", values=("ERROR", "BD", "DESCONECTADA", str(e)))

if __name__ == "__main__":
    app = CrystalGUI()
    app.mainloop()
import threading
from GUI.ventana_principal import CrystalGUI
from Core.honeypot_server import arrancar_en_hilo as kalopsia_hilo
from Core.ips_blocker import arrancar_en_hilo as paladin_hilo

def arrancar_ecosistema():
    # 1. Instanciamos la ventana principal
    gui = CrystalGUI()
    
    # 2. Creamos los hilos pasándoles la 'gui' como argumento (args=(gui,))
    hilo_kalopsia = threading.Thread(target=kalopsia_hilo, args=(gui,), daemon=True)
    hilo_paladin = threading.Thread(target=paladin_hilo, args=(gui,), daemon=True)
    
    # 3. Arrancamos los motores
    hilo_kalopsia.start()
    hilo_paladin.start()
    
    # 4. Iniciamos el bucle visual de la ventana
    gui.mainloop()

if __name__ == "__main__":
    arrancar_ecosistema()
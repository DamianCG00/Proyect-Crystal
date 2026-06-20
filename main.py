from Core.honeypot_server import arrancar_en_hilo as kalopsia_hilo
from Core.ips_blocker import arrancar_en_hilo as paladin_hilo
from GUI.ventana_principal import iniciar_gui

if __name__ == "__main__":
    print("Iniciando Ecosistema Crystal...")
    kalopsia_hilo()
    paladin_hilo()
    iniciar_gui()
import tkinter as tk
from thonny import get_workbench

# Noms internes des backends Thonny
PYTHON_3 = "LocalCPython"
ESP32 = "ESP32"

def switch_to_backend(backend_name):
    """Bascule l'interpréteur et force l'application immédiate"""
    wb = get_workbench()
    if wb.get_option("run.backend_name") != backend_name:
        wb.set_option("run.backend_name", backend_name)
        
        # SOLUTION : On détruit l'ancien backend pour forcer Thonny 
        # à charger le nouveau type d'interpréteur immédiatement.
        try:
            wb.get_runner().destroy_backend()
        except:
            pass
            
        # Redémarrage du moteur
        wb.restart_backend()
        wb.update_title()

def load_plugin():
    """Initialise les boutons radio à droite de la barre d'outils"""
    wb = get_workbench()
    toolbar = wb.get_toolbar()
    
    # Création d'un conteneur aligné à l'extrémité droite
    # L'utilisation de side="right" garantit qu'il est à la fin de la barre
    frame = tk.Frame(toolbar)
    frame.pack(side="right", padx=10)
    
    # Valeur initiale basée sur la configuration de Thonny
    current_val = wb.get_option("run.backend_name")
    var = tk.StringVar(value=current_val)
    
    def on_change():
        switch_to_backend(var.get())

    # Style des boutons radio : indicatoron=False les fait ressembler à des boutons poussoirs
    # Un bouton reste 'enfoncé' pour indiquer le mode actif
    rb_py = tk.Radiobutton(
        frame, 
        text="🐍 Python 3", 
        variable=var, 
        value=PYTHON_3, 
        command=on_change,
        indicatoron=False, 
        relief="raised",
        padx=8,
        pady=2
    )
    
    rb_esp = tk.Radiobutton(
        frame, 
        text="⚡ ESP32", 
        variable=var, 
        value=ESP32, 
        command=on_change,
        indicatoron=False,
        relief="raised",
        padx=8,
        pady=2
    )
    
    # Placement côte à côte dans le conteneur de droite
    rb_py.pack(side="left")
    rb_esp.pack(side="left")

    # Synchronisation : si l'utilisateur change via les menus, on met à jour les boutons
    def sync_ui(event=None):
        new_val = wb.get_option("run.backend_name")
        if new_val in [PYTHON_3, ESP32]:
            var.set(new_val)
            
    # Écoute de l'événement de redémarrage pour synchroniser l'UI
    wb.bind("BackendRestarted", sync_ui, True)

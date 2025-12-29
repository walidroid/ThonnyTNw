import tkinter as tk
from thonny import get_workbench

# Noms internes des backends Thonny
PYTHON_3 = "LocalCPython"
ESP32 = "ESP32"

def switch_to_backend(backend_name):
    """Bascule l'interpréteur et force l'application immédiate sans redémarrer Thonny"""
    wb = get_workbench()
    if wb.get_option("run.backend_name") != backend_name:
        wb.set_option("run.backend_name", backend_name)
        
        # SOLUTION pour l'application immédiate : 
        # On détruit le backend actuel (le lien avec Python) pour forcer 
        # Thonny à recréer le bon type d'interpréteur tout de suite.
        try:
            runner = wb.get_runner()
            if runner:
                runner.destroy_backend()
        except Exception:
            pass
            
        # On redémarre le moteur (Backend)
        wb.restart_backend()
        wb.update_title()

def create_radio_buttons():
    """Crée les boutons dans la barre d'outils une fois que l'UI est prête"""
    wb = get_workbench()
    
    # On tente de récupérer la barre d'outils
    try:
        toolbar = wb.get_toolbar()
    except Exception:
        # Sécurité si Thonny n'a pas de barre d'outils dans cette configuration
        return

    # Création d'un conteneur aligné à l'extrémité droite
    # side="right" place les boutons après tous les autres icônes
    frame = tk.Frame(toolbar)
    frame.pack(side="right", padx=10)
    
    # Valeur initiale basée sur la config Thonny
    current_val = wb.get_option("run.backend_name")
    var = tk.StringVar(value=current_val)
    
    def on_change():
        switch_to_backend(var.get())

    # Style des boutons radio comme des "boutons poussoirs" (indicatoron=False)
    # L'un reste enfoncé pour indiquer le mode actif
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
    
    # Placement côte à côte à droite
    rb_py.pack(side="left")
    rb_esp.pack(side="left")

    # Synchronisation : si l'utilisateur change via les menus, on met à jour les boutons
    def sync_ui(event=None):
        new_val = wb.get_option("run.backend_name")
        if new_val in [PYTHON_3, ESP32]:
            var.set(new_val)
            
    wb.bind("BackendRestarted", sync_ui, True)

def load_plugin():
    """Point d'entrée du plugin chargé par Thonny"""
    wb = get_workbench()
    
    # SOLUTION pour l'AttributeError : 
    # On utilise after_idle pour ne lancer create_radio_buttons que lorsque 
    # Thonny a fini de charger son interface et sa toolbar.
    wb.after_idle(create_radio_buttons)

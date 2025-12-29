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
        
        # On détruit le backend actuel pour forcer Thonny à charger 
        # le nouveau type d'interpréteur immédiatement.
        try:
            runner = wb.get_runner()
            if runner:
                runner.destroy_backend()
        except Exception:
            pass
            
        wb.restart_backend()
        wb.update_title()

def create_radio_buttons():
    """Crée les boutons radio à l'extrémité droite de la barre d'outils"""
    wb = get_workbench()
    
    try:
        # On récupère la barre d'outils (toolbar)
        toolbar = wb.get_toolbar()
    except Exception:
        # Si la toolbar n'est pas accessible, on annule pour éviter le crash
        return

    # On utilise un Frame pour grouper nos boutons
    # IMPORTANT : On utilise 'grid' car la toolbar de Thonny utilise grid.
    # On met une colonne très élevée (999) pour être tout à fait à droite.
    frame = tk.Frame(toolbar)
    frame.grid(row=0, column=999, sticky="e", padx=10)
    
    # On configure cette colonne pour qu'elle s'étire et pousse les autres vers la gauche
    toolbar.columnconfigure(999, weight=1)

    # Valeur initiale basée sur la config Thonny
    current_val = wb.get_option("run.backend_name")
    var = tk.StringVar(value=current_val)
    
    def on_change():
        switch_to_backend(var.get())

    # Style des boutons radio : indicatoron=False les transforme en boutons cliquables
    # relief="raised" / "sunken" indique visuellement quel mode est actif
    rb_py = tk.Radiobutton(
        frame, 
        text="🐍 Python 3", 
        variable=var, 
        value=PYTHON_3, 
        command=on_change,
        indicatoron=False, 
        relief="raised",
        padx=10,
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
        padx=10,
        pady=2
    )
    
    # À l'intérieur du Frame, on peut utiliser pack sans risque
    rb_py.pack(side="left")
    rb_esp.pack(side="left")

    # Synchronisation : met à jour les boutons si l'utilisateur change via les menus
    def sync_ui(event=None):
        new_val = wb.get_option("run.backend_name")
        if new_val in [PYTHON_3, ESP32]:
            var.set(new_val)
            
    wb.bind("BackendRestarted", sync_ui, True)

def load_plugin():
    """Point d'entrée du plugin"""
    wb = get_workbench()
    
    # On utilise after_idle pour attendre que l'interface Thonny soit 
    # totalement construite avant d'ajouter nos boutons.
    # Cela évite les erreurs 'AttributeError' et les plantages au lancement.
    wb.after_idle(create_radio_buttons)

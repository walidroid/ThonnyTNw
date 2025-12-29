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
        
        # On détruit le backend actuel pour forcer le changement immédiat
        try:
            runner = wb.get_runner()
            if runner:
                runner.destroy_backend()
        except Exception:
            pass
            
        wb.restart_backend()
        wb.update_title()

def create_radio_buttons():
    """Crée les boutons dans la barre d'outils en utilisant GRID"""
    wb = get_workbench()
    
    try:
        toolbar = wb.get_toolbar()
    except Exception:
        return

    # SOLUTION : Utiliser grid au lieu de pack car la toolbar de Thonny utilise grid
    # On utilise un numéro de colonne très élevé (999) pour être à l'extrémité droite
    # sticky="e" (East) aligne le contenu vers la droite
    frame = tk.Frame(toolbar)
    frame.grid(row=0, column=999, sticky="e", padx=10)
    
    # On demande à la colonne d'occuper l'espace disponible si nécessaire
    toolbar.columnconfigure(999, weight=1)

    current_val = wb.get_option("run.backend_name")
    var = tk.StringVar(value=current_val)
    
    def on_change():
        switch_to_backend(var.get())

    # À l'intérieur du frame, nous pouvons utiliser pack car le frame est vide
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
    
    rb_py.pack(side="left")
    rb_esp.pack(side="left")

    def sync_ui(event=None):
        new_val = wb.get_option("run.backend_name")
        if new_val in [PYTHON_3, ESP32]:
            var.set(new_val)
            
    wb.bind("BackendRestarted", sync_ui, True)

def load_plugin():
    """Charge le plugin après l'initialisation de l'interface"""
    wb = get_workbench()
    # On attend que l'interface soit prête pour éviter l'AttributeError sur la toolbar
    wb.after_idle(create_radio_buttons)
